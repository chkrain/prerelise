from pyplc.pou import POU
from pyplc.sfc import SFC
from pyplc.utils.trig import TRIG
from pyplc.utils.misc import TON,BLINK
from gear import Gear

class Factory(POU):
    HOUR = 3600000
    TRIAL_HOURS = 720  
    # RENEWAL_CODE = ['12345'] продолжить логику
    ACTIVATION_CODE = 798432534

    manual = POU.var(True)
    emergency = POU.var(False)
    heartbeat= POU.output(False)
    scanTime = POU.var(0)
    moto = POU.var(int(0),persistent=True)
    powered = POU.var(int(0),persistent=True)
    hw_emergency = POU.input(False,hidden=True)
    
    activated = POU.var(bool(False),persistent=True)
    trial_over = POU.var(False)
    activation_code = POU.var(0)

    def __init__(self,emergency: bool,*_,id:str = None,parent:POU=None) -> None:
        super().__init__( id,parent )
        self.hw_emergency = emergency
        self.manual = True
        self.emergency = False
        self.powerfail = True
        self.powerack = False
        self.f_manual = TRIG(clk = lambda: self.manual)
        self.f_emergency = TRIG(clk = lambda: self.emergency or self.hw_emergency)
        self.f_powerack = TON(clk = lambda: self.powerack,pt=2000)
        self.hour_timer = TON(pt=Factory.HOUR)  
        self.__sec= BLINK(enable=True)
        self.moto = 0
        self.powered = 0
        self.activated = False
        self.trial_over = False
        self.activation_code = 0
        self.__last_call = POU.NOW_MS
        self.__accumulated_time = 0 
        self.on_mode = [lambda *args: self.log('ручной режим = ',*args)]
        self.on_emergency = [lambda *args: self.log('аварийный режим = ',*args)]

    def check_license(self):
        if self.activated:
            return
            
        self.__accumulated_time += self.scanTime
        
        if self.__accumulated_time >= Factory.HOUR:
            self.moto += 1
            self.__accumulated_time = 0  
            
        if self.moto >= Factory.TRIAL_HOURS:
            self.trial_over = True
            self.emergency = True
            
        if self.activation_code == Factory.ACTIVATION_CODE:
            self.activated = True
            self.trial_over = False
            self.emergency = False
            self.log('Система активирована!')

    def __call__(self) :
        with self:
            current_time = POU.NOW_MS
            self.scanTime = current_time - self.__last_call
            self.__last_call = current_time
            
            self.check_license()  
            self.heartbeat = self.__sec( )
            
            if self.f_manual( ):
                for e in self.on_mode:
                    e( self.manual )
            if self.f_emergency( ) or self.f_emergency.clk:
                for e in self.on_emergency:
                    e( self.f_emergency.clk )
                
            if self.powerfail:
                self.powerfail = False
                self.powered += 1

class ControlStation(POU):
    start = POU.input(False,hidden=True)
    stop  = POU.input(False,hidden=True)
    
    def __init__(self,*_,start:bool,stop:bool,gear: Gear,id: str = None, parent: POU = None,**kwargs) -> None:
        super().__init__(id, parent)
        self.start = start
        self.stop = stop
        self.gear = gear
        self.active = False
        
    def main(self):
        if self.start or self.stop:
            self.active   = True
        if self.active:
            self.gear.on = self.start
            self.gear.off= self.stop
            self.active  = self.start or self.stop
    
    def __call__(self):
        with self:
            self.main()

class ControlPost(ControlStation):
    manual = POU.input(False,hidden=True)
    def __init__(self, *_, manual:bool, start: bool, stop: bool, gear: Gear, id: str = None, parent: POU = None) -> None:
        super().__init__(*_, start=start, stop=stop, gear=gear, id=id, parent=parent)
        self.manual = manual
        
    def main(self):
        if self.manual:
            super().main( )

class GearAny():
    def __init__(self,first: Gear, second: Gear) -> None:
        self.first = first
        self.fault = False
        self.second= second
        self.state = Gear.IDLE
        
    def __call__(self):
        if self.first.state == Gear.RUN and self.second.state == Gear.RUN:
            self.state = Gear.RUN
            self.fault = False         
        else:
            self.state = Gear.IDLE
            self.fault = False