from pyplc.sfc import SFC,POU
from pyplc.utils.latch import RS
from pyplc.utils.trig import TRIG,FTRIG,RTRIG
from pyplc.utils.misc import TOF, TON

class Gear(SFC):
    """Базовый класс для конвейеров, норий, сита, барабана"""
    IDLE = 0
    STARTUP = 1
    RUN = 2
    STOP = 3
    
    MAINTENANCE_INTERVAL = 18000
    
    rdy = POU.var(False)
    on  = POU.var(False)
    off = POU.var(False)
    lock = POU.var(False)
    startup_t = POU.var(int(5),persistent=True)
    test = POU.var(False,hidden=True)       #тест нештатной ситуации
    rsn  = POU.var(int(0),hidden=True)      #выбор нештатной ситуации
    manual=POU.var(False,persistent=True) #ручной режим (не учитывать depends)
    
    fault = POU.input(False, hidden = True)
    _lock = POU.input(False,hidden = True)
    q   = POU.output(False, hidden = True)    
    msg = POU.var('Oжидание')
    
    moto = POU.var(int(0), persistent=True)  
    moto_reset = POU.var(False)  # кнопка сброса моточасов
    maintenance_required = POU.var(False)  # требуется ТО
    maintenance_reset = POU.var(False)  # кнопка сброса предупреждения ТО
    last_maintenance = POU.var(int(0), persistent=True)  # моточасы на последнем ТО
    
    def __init__(self, fault: bool|None=None, q: bool|None = None, lock: bool|None = None, depends: 'Gear|None'=None, id: str|None = None, parent: POU|None = None) -> None:
        super().__init__(id, parent)
        self.state = Gear.IDLE
        self.allowed = True
        if callable(fault): self.fault = fault
        self._lock = lock
        self.q = q
        self.depends = depends
        self._ctl = RS(reset = lambda: self.off, set = lambda: self.on, q = self.control )
        self._tst = FTRIG( clk=lambda: self.test, q = self._test)
        
        self._moto_counter = 0
        self._last_update = POU.NOW_MS
        
        self.subtasks = (self._ctl, self._tst)
        self._pass = 0
    
    def _update_moto_hours(self):
        """Обновление моточасов - каждую секунду при работе"""
        current_time = POU.NOW_MS
        if self.state == Gear.RUN:
            if current_time - self._last_update >= 10:  
                self._moto_counter += 1
                self._last_update = current_time
                
                if self._moto_counter >= 600:
                    self.moto += 10
                    self._moto_counter = 0
                    
                    if self.moto - self.last_maintenance >= Gear.MAINTENANCE_INTERVAL:
                        self.maintenance_required = True
    
    def _reset_moto_hours(self):
        """Сброс моточасов по кнопке"""
        if self.moto_reset:
            self.moto = 0
            self._moto_counter = 0
            self.last_maintenance = 0
            self.maintenance_required = False
            self.moto_reset = False
    
    def _reset_maintenance_warning(self):
        """Сброс предупреждения о ТО по кнопке"""
        if self.maintenance_reset:
            self.last_maintenance = self.moto
            self.maintenance_required = False
            self.maintenance_reset = False
    
    def _test(self, on: bool):
        if on:
            if self.rsn==0:
                self.inspect( fault = lambda x: x.force( True if self._pass==0 else None ) )
            elif self.rsn==1:
                self.inspect( _lock = lambda x: x.force( True if self._pass==0 else None) )
        else:
            self._pass = (self._pass + 1) % 2
            
    def _turnon(self):
        self.lock = False
    
    def _turnoff(self):
        self.allowed = True
        
    def _allowed(self)->bool:
        self.allowed = True
        if self.depends is not None and not self.manual:
            if self.depends.state!=Gear.RUN: return False
            if self.depends.fault: self.allowed = False
        else:
            self.allowed = not self._lock
            
        if self._lock: self.allowed = False
        return self.allowed
    
    def control(self,power: bool):
        if power and not self._allowed(): 
            self.lock = True
            return
        self.q = power and not self._lock
        if power and self._lock:
            self.lock = True
        if not power:
            self.lock = False
            
    def _begin(self):
        self.log('entering working mode')
        self.msg = 'Работа'
        
    def _end(self):
        self.log('working working mode')
        self.msg = 'Работа прекращена'
        
    def emergency(self,on: bool):
        self.on = False
        self.off = on
        
    def main(self):
        self.state = Gear.IDLE
        self.rdy = False
        self.busy = False
        
        yield from self.until( lambda: self.q,step='ожидаем запуска' )
        
        self.state = Gear.STARTUP
        self._turnon( )
        self.log('разгоняемся')
        self.msg = 'Разгон'
        T = 0 
        while T<5 and self._allowed():
            yield from self.pause(1000)
            T+=1
            self.rdy = not self.rdy
            self._update_moto_hours()  # Обновление моточасов
            self._reset_moto_hours()   # Проверка сброса моточасов
            self._reset_maintenance_warning()  # Проверка сброса предупреждения ТО
            
        if T<5 or self.fault:
            self.rdy = False
            if self.q and self.fault:
                self.log('аварийный останов при пуске')
                self.msg = 'Авария при пуске'
        else:
            self.rdy = True
            self.state = Gear.RUN        
            self.log('вышли в режим')
            self.msg = 'В режиме'
            self._begin()
            
            while self.q and self._allowed() and not self._lock:
                self._update_moto_hours() 
                self._reset_moto_hours()   
                self._reset_maintenance_warning() 
                yield
                
            self._end( )
            
        self._turnoff( )
        self._ctl.unset( )
        self.state = Gear.STOP
        self.busy = False
        self.rdy = False
        if self._lock: 
            self.log('отключение по блокировке')
            self.msg = 'Отключено по блокировке'
            self.lock = True
            
        self.q = False

class GearROT(Gear):
    rotating = POU.var(False)
    rot = POU.input(False, hidden = True)
    
    def __init__(self, fault: bool = None, q: bool = None, lock: bool = None, rot: bool = None, depends: Gear = None, id: str = None, parent: POU = None) -> None:
        super().__init__(fault=fault, q=q, lock=lock, depends=depends, id=id, parent=parent)
        self.rot = rot
        self._rotating = TOF(clk = TRIG(clk = lambda: self.rot),pt=5000, q = self.monitor)
        self.subtasks += (self._rotating, )

    def monitor(self, rot: bool):
        self.rotating = rot
        if not rot and self.q:
            self.ok = False
            self.log('ошибка: нет вращения')
            self.msg = 'Проверить вращение'

class GearFQ(Gear):
    """Базовый класс для конвейеров c ЧП, сита, барабана с частотным управлением"""
    fq = POU.output(int(0), hidden = False)
    sp = POU.var(int(150), persistent=True)  #пусковая частота
    
    def _turnon(self):
        self.fq = self.sp
        
    def _turnoff(self):
        if self.state==Gear.RUN: self.sp = self.fq
        self.fq = 0
    
    def __init__(self, fq: int|None = None,  fault: bool|None = None, q: bool|None = None, lock: bool|None = None, depends: Gear|None=None, id: str|None = None, parent: POU|None = None) -> None:
        super().__init__(fault=fault, q=q, lock=lock, depends=depends, id=id, parent=parent)
        self.fq = fq
        
class Feeder(GearFQ):
    """Конвейер с частотным управлением"""
    rotating = POU.var(False)
    rot = POU.input(False,hidden=True)
    fail  = POU.var(False)

    def monitor(self, rot: bool):
        self.rotating = rot
        if not rot and self.q:
            self.ok = False
            self.log('ошибка: нет вращения')
            self.msg = 'Проверить вращение'
            
        self.fail = self.fault and self.q
    
    def update_timeout(self):
        #время ожидания изменения сигнала на входе rot зависит от скорости работы. Экспериментально подобрано
        if self.q:
            if self.fq<20:
                self._rotating.pt = 500000
            if self.fq<100:
                self._rotating.pt = 30000
            if self.fq<250:
                self._rotating.pt = 8000
            if self.fq<500:
                self._rotating.pt = 5000
            elif self.fq<1000:
                self._rotating.pt = 3000
            else:
                self._rotating.pt = 10000
        
    def __init__(self, rot: bool|None = None,fq: int|None = None,  fault: bool|None = None, q: bool|None = None, lock: bool|None = None, depends: Gear|None=None, id: str|None = None, parent: POU|None = None) -> None:
        super().__init__(fault=fault, q=q, lock=lock, depends=depends, fq=fq, id=id, parent=parent)
        self.rot = rot
        self._rotating = TOF(clk = TRIG(clk = lambda: self.rot), q = self.monitor)
        self.subtasks += (self._rotating,self.update_timeout )
        
    def _allowed(self) -> bool:
        self.fail = self.fault and self.q
        return super()._allowed()

class GearChain(SFC):
    IDLE = 0
    STARTING = 1
    STOPPING = 2
    UNDEFINED = 3
    
    on  = POU.var(False)
    off = POU.var(False)
    msg = POU.var('ГОТОВ')

    def __init__(self, gears: tuple[Gear], id: str = None, parent: POU = None) -> None:
        super().__init__( id=id, parent=parent)
        self.gears = gears
        self._t_on = FTRIG(clk = lambda: self.on )
        self._t_off= RTRIG(clk = lambda: self.off )
        self.subtasks = (self._t_on, self._t_off )
        self.state = GearChain.IDLE
            
    def _start(self):
        self.state = GearChain.STARTING
        for gear in reversed(self.gears):
            if gear.state == Gear.RUN:
                continue
            self.msg=f'ОТМЕНА'
            if gear.lock:
                gear.off = True
                yield
                gear.off = False
            gear.on = True
            yield
            gear.on = False
            yield from self.till(lambda: gear.state != Gear.RUN and self.state == GearChain.STARTING, max=6000, step=f'ожидаем запуска {gear.id}')
            if gear.state!= Gear.RUN:
                self.msg=f'СТОП'
                self.log(f'неудачная попытка запуска {gear.id}')
                return
            if self.state != GearChain.STARTING:
                break
            yield from self.pause(2000)
        if self.state==GearChain.STARTING: 
            self.state = GearChain.IDLE
            self.msg = 'СТОП'
    
    def _stop(self):
        self.state = GearChain.STOPPING
        for gear in self.gears:
            if gear.state == Gear.IDLE:
                continue
            T = gear.startup_t
            while gear.state == Gear.RUN and self.state==GearChain.STOPPING and T>0:
                yield from self.till(lambda: gear.state == Gear.RUN and self.state==GearChain.STOPPING, max = 1000, step = f'штатный останов {gear.id}')
                T-=1
                self.msg=f'СТОП({T})'            
            gear.off = True
            yield
            gear.off = False
            yield from self.till(lambda: gear.state != Gear.IDLE and self.state==GearChain.STOPPING, step=f'ожидаем остановки {gear.id}',max = 2000)
            if gear.state != Gear.IDLE:
                self.msg=f'СТОП'
                self.log(f'неудачная попытка остановки {gear.id}')
                return
            if self.state != GearChain.STOPPING:break
            yield from self.pause(2000)
        if self.state==GearChain.STOPPING: 
            self.state = GearChain.IDLE
            self.msg = 'СТОП'

    def main(self):
        yield from self.until(lambda: self._t_on.q or self._t_off.q, step='ожидаем пуск/стоп')
        
        if self._t_on.q:
            if self.state!=GearChain.STARTING:
                self.log('последовательный запуск')
                self.exec(self._start())
            else:
                self.state=GearChain.IDLE
        if self._t_off.q:
            if self.state!=GearChain.STOPPING:
                self.log('последовательная остановка')
                self.exec(self._stop() )
            else:
                self.state=GearChain.IDLE

