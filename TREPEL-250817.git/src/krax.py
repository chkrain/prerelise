#Ниже идет Ваша программа
from pyplc.platform import plc, plc as hw
from pyplc.utils.trig import RTRIG
from pyplc.utils.misc import TP, BLINK
from sys import platform
from project import name as project_name,version_short as project_version
from gear import Gear as Motor, Feeder,GearFQ,GearROT,GearChain
from mbfqconverters import FQConv
from misc import Factory,ControlPost,ControlStation, GearAny
from pyplc.utils.misc import TON
from pyplc.sfc import SFC,POU

print(f'\tStarting {project_name} {project_version}')

if platform == 'fake':
  from collections import namedtuple
  HW = namedtuple('HW', ['SIREN', 'TE1', 'TE2', 'H1', 'BURNER_SP', 'MOTOR_ON_1', 'MOTOR_ON_2', 'MOTOR_ON_3', 'MOTOR_ON_4', 'MOTOR_ON_5', 'MOTOR_ON_6', 'MOTOR_ON_7', 'MOTOR_ON_8', 'MOTOR_ON_10', 'BURNER_START', 'MOTOR_ON_11', 'MOTOR_ON_12', 'AUGER_ON_13', 'FILTER_START', 'MOTOR_ON_14', 'MOTOR_ON_15', 'MOTOR_ON_16', 'MOTOR_ON_17', 'MOTOR_ON_18', 'VIBRATOR_ON_1', 'MOTOR_ON_101', 'MOTOR_OFF_101', 'MOTOR_ON_20', 'MOTOR_ON_19', 'VIBRATOR_ON_2', 'AUGER_ON_22', 'AUGER_ON_24', 'AUGER_ON_25', 'COMPRESSOR_ON_28', 'AUGER_ON_26', 'FAN_ON_27', 'ROPE_1', 'BELT_1', 'MOTOR_ISON_2', 'ROPE_3', 'BELT_3', 'MOTOR_ISON_4', 'ROPE_5', 'BELT_5', 'MOTOR_ISON_6', 'ROPE_7', 'BELT_7', 'ROPE_8', 'BELT_8', 'OPENED_1', 'ROPE_10', 'BELT_10', 'MOTOR_ISON_11', 'AUGER_ISON_13', 'AUGER_ROT_13', 'ROPE_14', 'BELT_14', 'MOTOR_ISON_15', 'ROPE_16', 'BELT_16', 'MOTOR_ISON_17', 'ROPE_18', 'BELT_18', 'HLEVEL_2', 'ROPE_20', 'BELT_20', 'OPENED_2', 'ROPE_19', 'BELT_19', 'AUGER_ROT_22', 'AUGER_ROT_24', 'AUGER_ISON_25', 'AUGER_ROT_25', 'COMPRESSOR_ISON_28', 'FAN_ISON', 'EMERGENCY', 'PU_START_1', 'PU_STOP_1', 'PU_START_2', 'PU_STOP_2', 'MAN_1', 'START_1', 'STOP_1', 'MAN_2', 'START_2', 'STOP_2', 'MAN_3', 'START_3', 'STOP_3', 'MAN_4', 'START_4', 'STOP_4', 'MAN_5', 'START_5', 'STOP_5', 'MAN_6', 'START_6', 'STOP_6', 'MAN_7', 'START_7', 'STOP_7', 'MAN_8', 'START_8', 'STOP_8', 'MAN_10', 'START_10', 'STOP_10', 'MAN_12', 'START_12', 'STOP_12', 'MAN_13', 'START_13', 'STOP_13', 'MAN_14', 'START_14', 'STOP_14', 'MAN_15', 'START_15', 'STOP_15', 'MAN_16', 'START_16', 'STOP_16', 'MAN_17', 'START_17', 'STOP_17', 'MAN_18', 'START_18', 'STOP_18', 'MAN_19', 'START_19', 'STOP_19', 'MAN_20', 'START_20', 'STOP_20', 'MAN_22', 'START_22', 'STOP_22', 'MAN_24', 'START_24', 'STOP_24', 'MAN_25', 'START_25', 'STOP_25', 'MAN_28', 'START_28', 'STOP_28',
                  'TE1', 'TE2', 'H1', 'BURNER_SP', 'MOTOR_ON_1', 'MOTOR_ON_2', 'MOTOR_ON_3', 'MOTOR_ON_4', 'MOTOR_ON_5', 'MOTOR_ON_6', 'MOTOR_ON_7', 'MOTOR_ON_8', 'MOTOR_ON_10', 'BURNER_START', 'MOTOR_ON_11', 'MOTOR_ON_12', 'AUGER_ON_13', 'FILTER_START', 'MOTOR_ON_14', 'MOTOR_ON_15', 'MOTOR_ON_16', 'MOTOR_ON_17', 'MOTOR_ON_18', 'VIBRATOR_ON_1', 'MOTOR_ON_101', 'MOTOR_OFF_101', 'MOTOR_ON_20', 'MOTOR_ON_19', 'VIBRATOR_ON_2', 'AUGER_ON_22', 'AUGER_ON_24', 'AUGER_ON_25', 'COMPRESSOR_ON_28', 'AUGER_ON_26', 'FAN_ON_27', 'ROPE_1', 'BELT_1', 'MOTOR_ISON_2', 'ROPE_3', 'BELT_3', 'MOTOR_ISON_4', 'ROPE_5', 'BELT_5', 'MOTOR_ISON_6', 'ROPE_7', 'BELT_7', 'ROPE_8', 'BELT_8', 'OPENED_1', 'ROPE_10', 'BELT_10', 'MOTOR_ISON_11', 'AUGER_ISON_13', 'AUGER_ROT_13', 'ROPE_14', 'BELT_14', 'MOTOR_ISON_15', 'ROPE_16', 'BELT_16', 'MOTOR_ISON_17', 'ROPE_18', 'BELT_18', 'HLEVEL_2', 'ROPE_20', 'BELT_20', 'OPENED_2', 'ROPE_19', 'BELT_19', 'AUGER_ROT_22', 'AUGER_ROT_24', 'AUGER_ISON_25', 'AUGER_ROT_25', 'HLEVEL_02', 'LLEVEL_02', 'LLEVEL_38', 'HLEVEL_38', 'COMPRESSOR_ISON_28', 'FAN_ISON', 'EMERGENCY', 'PU_START_1', 'PU_STOP_1', 'PU_START_2', 'PU_STOP_2', 'MAN_1', 'START_1', 'STOP_1', 'MAN_2', 'START_2', 'STOP_2', 'MAN_3', 'START_3', 'STOP_3', 'MAN_4', 'START_4', 'STOP_4', 'MAN_5', 'START_5', 'STOP_5', 'MAN_6', 'START_6', 'STOP_6', 'MAN_7', 'START_7', 'STOP_7', 'MAN_8', 'START_8', 'STOP_8', 'MAN_10', 'START_10', 'STOP_10', 'MAN_12', 'START_12', 'STOP_12', 'MAN_13', 'START_13', 'STOP_13', 'MAN_14', 'START_14', 'STOP_14', 'MAN_15', 'START_15', 'STOP_15', 'MAN_16', 'START_16', 'STOP_16', 'MAN_17', 'START_17', 'STOP_17', 'MAN_18', 'START_18', 'STOP_18', 'MAN_19', 'START_19', 'STOP_19', 'MAN_20', 'START_20', 'STOP_20', 'MAN_22', 'START_22', 'STOP_22', 'MAN_24', 'START_24', 'STOP_24', 'MAN_25', 'START_25', 'STOP_25', 'MAN_28', 'START_28', 'STOP_28'], defaults=[])
  hw = HW()

factory_1 = Factory(emergency=hw.EMERGENCY)
fq_1 = FQConv(addr=1)
fq_3 = FQConv(addr=2) #
fq_5 = FQConv(addr=9)
fq_7 = FQConv(addr=10)
fq_8 = FQConv(addr=11)
fq_10 = FQConv(addr=3)
fq_11 = FQConv(addr=55) # барабан
fq_12 = FQConv(addr=4) #
fq_14 = FQConv(addr=5)
fq_16 = FQConv(addr=6)
fq_18 = FQConv(addr=12) 
fq_19 = FQConv(addr=13)
fq_20 = FQConv(addr=7)
# fq_22 = FQConv(addr=201)
fq_24 = FQConv(addr=202)
fq_25 = FQConv(addr=203)

compressor_28 = Motor(q=hw.COMPRESSOR_ON_28,fault=~hw.COMPRESSOR_ISON_28)
#motor_101 is direct controlled
#ZONE 2
motor_999 = Motor(q=hw.SIREN) # MOTOR_SIREN было, из-за idx = 999
motor_25= Feeder(q=hw.AUGER_ON_25, rot=hw.AUGER_ROT_25,fault=hw.AUGER_ISON_25,fq=fq_25.set_fq)
motor_24= Feeder(q=hw.AUGER_ON_24, rot=hw.AUGER_ROT_24,fq=fq_24.set_fq )
motor_22= GearROT(q=hw.AUGER_ON_25, fault=~hw.AUGER_ISON_25, rot=hw.AUGER_ROT_25) # auger_ison_25 соответствует 22ому, но обр связь взята с 25.
motor_20= Feeder(q=hw.MOTOR_ON_20, fault=fq_20.fault, lock=hw.ROPE_20, rot=hw.BELT_20,fq=fq_20.set_fq)
any_22_or_24 = GearAny(motor_22,motor_24)
motor_19= Feeder(q=hw.MOTOR_ON_19, fault=fq_19.fault, lock=hw.ROPE_19, rot=hw.BELT_19,fq=fq_19.set_fq)
motor_18= Feeder(q=hw.MOTOR_ON_18, fault=fq_18.fault, lock=hw.ROPE_18, rot=hw.BELT_18,fq=fq_18.set_fq)
any_18_or_19 = GearAny(motor_18,motor_19)
motor_17= Motor(q=hw.MOTOR_ON_17,fault=~hw.MOTOR_ISON_17,depends=any_18_or_19)
motor_16= Feeder(q=hw.MOTOR_ON_16, fault=fq_16.fault, lock=hw.ROPE_16, rot=hw.BELT_16,fq=fq_16.set_fq,depends=motor_17)
motor_15= Motor(q=hw.MOTOR_ON_15,fault=~hw.MOTOR_ISON_15,depends=motor_16)
motor_14= Feeder(q=hw.MOTOR_ON_14, fault=fq_14.fault, lock=hw.ROPE_14, rot=hw.BELT_14,fq=fq_14.set_fq,depends=motor_15)
#ZONE 1
motor_13= GearROT(q=hw.AUGER_ON_13,fault=~hw.AUGER_ISON_13, rot=hw.AUGER_ROT_13)
motor_12= GearFQ(q=hw.MOTOR_ON_12, fq=fq_12.set_fq,fault=fq_12.fault)
motor_11= GearFQ(q=hw.MOTOR_ON_11, fq=fq_11.set_fq,fault=fq_11.fault)
motor_10= Feeder(q=hw.MOTOR_ON_10, fault=fq_10.fault, lock=hw.ROPE_10, rot=hw.BELT_10,fq=fq_10.set_fq,depends=motor_11) 
motor_8 = Feeder(q=hw.MOTOR_ON_8, fault=fq_8.fault, lock=hw.ROPE_8, rot=hw.BELT_8,fq=fq_8.set_fq)
motor_7 = Feeder(q=hw.MOTOR_ON_7, fault=fq_7.fault, lock=hw.ROPE_7, rot=hw.BELT_7,fq=fq_7.set_fq,depends=motor_8)
motor_6 = Motor(q=hw.MOTOR_ON_6,depends=motor_10)
motor_5 = Feeder(q=hw.MOTOR_ON_5, fault=fq_5.fault, lock=hw.ROPE_5, rot=hw.BELT_5,fq=fq_5.set_fq,depends=motor_6)
motor_4 = Motor(q=hw.MOTOR_ON_4,depends=motor_5)
motor_3 = Feeder(q=hw.MOTOR_ON_3, fault=fq_3.fault, lock=hw.ROPE_3, rot=hw.BELT_3,fq=fq_3.set_fq,depends=motor_4)
motor_2 = Motor(q=hw.MOTOR_ON_2,depends=motor_3)
motor_1 = Feeder(q=hw.MOTOR_ON_1, fault=fq_1.fault, lock=hw.ROPE_1, rot=hw.BELT_1,fq=fq_1.set_fq,depends=motor_2)

mcompressor_28 = ControlPost(start=hw.START_28,stop=~hw.STOP_28,manual=hw.MAN_28,gear=compressor_28)
mmotor_1 = ControlPost(start=hw.START_1,stop=~hw.STOP_1,manual=hw.MAN_1,gear = motor_1)
mmotor_1a = ControlStation(start=hw.PU_START_1,stop=~hw.PU_STOP_1,gear = motor_1)
mmotor_2 = ControlPost(start=hw.START_2,stop=~hw.STOP_2,manual=hw.MAN_2,gear = motor_2)
mmotor_3 = ControlPost(start=hw.START_3,stop=~hw.STOP_3,manual=hw.MAN_3,gear = motor_3)
mmotor_4 = ControlPost(start=hw.START_4,stop=~hw.STOP_4,manual=hw.MAN_4,gear = motor_4)
mmotor_5 = ControlPost(start=hw.START_5,stop=~hw.STOP_5,manual=hw.MAN_5,gear = motor_5)
mmotor_6 = ControlPost(start=hw.START_6,stop=~hw.STOP_6,manual=hw.MAN_6,gear = motor_6)
mmotor_7 = ControlPost(start=hw.START_7,stop=~hw.STOP_7,manual=hw.MAN_7,gear = motor_7)
mmotor_8 = ControlPost(start=hw.START_8,stop=~hw.STOP_8,manual=hw.MAN_8,gear = motor_8)
mmotor_10 = ControlPost(start=hw.START_10,stop=~hw.STOP_10,manual=hw.MAN_10,gear = motor_10)
mmotor_11 = ControlStation(start=hw.PU_START_2,stop=~hw.PU_STOP_2,gear = motor_11)
mmotor_12 = ControlPost(start=hw.START_12,stop=~hw.STOP_12,manual=hw.MAN_12,gear = motor_12)
mmotor_13 = ControlPost(start=hw.START_13,stop=~hw.STOP_13,manual=hw.MAN_13,gear = motor_13)
mmotor_14 = ControlPost(start=hw.START_14,stop=~hw.STOP_14,manual=hw.MAN_14,gear = motor_14)
mmotor_15 = ControlPost(start=hw.START_15,stop=~hw.STOP_15,manual=hw.MAN_15,gear = motor_15)
mmotor_16 = ControlPost(start=hw.START_16,stop=~hw.STOP_16,manual=hw.MAN_16,gear = motor_16)
mmotor_17 = ControlPost(start=hw.START_17,stop=~hw.STOP_17,manual=hw.MAN_17,gear = motor_17)
mmotor_18 = ControlPost(start=hw.START_18,stop=~hw.STOP_18,manual=hw.MAN_18,gear = motor_18)
mmotor_19 = ControlPost(start=hw.START_19,stop=~hw.STOP_19,manual=hw.MAN_19,gear = motor_19)
mmotor_20 = ControlPost(start=hw.START_20,stop=~hw.STOP_20,manual=hw.MAN_20,gear = motor_20)
mmotor_22 = ControlPost(start=hw.START_25,stop=~hw.STOP_25,manual=hw.MAN_25,gear = motor_22)

chain_drum = GearChain( gears=(motor_11, motor_999) )
chain_8 = GearChain( gears=(motor_1,motor_2,motor_3,motor_4,motor_5,motor_6,motor_7,motor_8, motor_999) )
chain_22 = GearChain( gears=(motor_1,motor_2,motor_3,motor_4,motor_5,motor_6,motor_10,motor_11,motor_14,motor_15,motor_16,motor_17,motor_18,motor_19, motor_999) )

emergency_stoppable = (motor_1,motor_2,motor_3,motor_4,motor_5,motor_6,motor_7,motor_8,motor_10,motor_11,motor_12,motor_13,motor_14,motor_15,motor_16,motor_17,motor_18,motor_19,motor_20,motor_22,motor_24,motor_25)
factory_1.on_emergency = [ g.emergency for g in emergency_stoppable ]

def on_motor_11_run(on: bool):  #фильтр и шнек из него
  motor_12.on = on
  motor_999.off = False
    
def on_motor_19_run(on: bool):  
  motor_999.off = False

def on_motor_18_run(on: bool):  
  motor_999.off = False
  
def on_any_motor(on: bool):   #аспирация вкл если что-то заработало, сирена - выкл
  hw.MOTOR_ON_101 = on
  hw.MOTOR_OFF_101 = False
  
def on_motor_20_run(on:bool):
  compressor_28.on = on
  compressor_28.off = False
  motor_19.off = False

def on_motor_22_run(on:bool):
  motor_18.off = False

def if_opened(on: bool): # концевик открыт
  motor_20.on = on

def if_closed(off: bool):
  motor_20.off = off
  
def if_opened_2(on: bool): # концевик открыт
  motor_22.on = on  

def if_closed_2(off: bool):
  motor_22.off = off

def is_any_running()->bool:
  for g in emergency_stoppable:
    if g.state==Motor.RUN:
      return True
    
  return False

def get_lvl_pt_02():
  T = 300
  T_convert = T * 1000 * 60
  if motor_22.state == Motor.RUN:
    return T_convert
  else:
    return T_convert / 2

def get_lvl_pt_38():
  T = 300
  T_convert = T * 1000 * 60
  if motor_20.state == Motor.RUN:
    return T_convert
  else:
    return T_convert / 2

level_3_monitor = TON(clk=lambda: hw.HLEVEL_38, pt=get_lvl_pt_38, q=lambda timeout: setattr(motor_18, 'off', True) if timeout else None) # 3-8
 
level_4_monitor = TON(clk=lambda: hw.HLEVEL_02, pt=get_lvl_pt_02, q=lambda timeout: setattr(motor_19, 'off', True) if timeout else None) # 0-2

def get_siren_pt():
    if motor_11.state == Motor.RUN and (motor_12.state != Motor.RUN or motor_12.fault):
        return 2000
    else:
        return 10000

siren_stop = TON(clk=lambda: hw.SIREN, pt=get_siren_pt, q=lambda timeout: setattr(motor_999, 'off', True) if timeout else None)

motor_12_fault_siren = BLINK(enable=lambda: motor_11.state==Motor.RUN and (motor_12.state!=Motor.RUN or motor_12.fault), 
                            t_on=2000, t_off=2000, 
                            q=lambda state: setattr(motor_999, 'on', state))

motor_12.sp = 1500
motor_1.sp = 15
motor_3.sp = 150
motor_5.sp = 225
motor_10.sp = 225
motor_11.sp = 450
motor_14.sp = 120
motor_16.sp = 180
motor_18.sp = 225
motor_19.sp = 225
motor_20.sp = 225

instances = (factory_1,
            mcompressor_28, 
            chain_drum, chain_8,chain_22,
            mmotor_1,mmotor_1a,mmotor_2,mmotor_3,mmotor_4,mmotor_5,mmotor_6,mmotor_7,mmotor_8,mmotor_10,mmotor_11,mmotor_12,mmotor_13,
            mmotor_14,mmotor_15,mmotor_15,mmotor_16,mmotor_17,mmotor_18,mmotor_19,mmotor_20,mmotor_22,
            compressor_28, motor_999,
            motor_1,motor_2,motor_3,motor_4,motor_5,motor_6,
            any_18_or_19,any_22_or_24,
            motor_7,motor_8,motor_10,motor_11,motor_12,motor_13,
            motor_14,motor_15,motor_16,motor_17,motor_18,motor_19,motor_20,motor_22,motor_24,motor_25,
            fq_1,fq_3, fq_5,fq_7,fq_8,fq_10, fq_11, fq_12,fq_14,fq_16,fq_18,fq_19,fq_20,
            RTRIG(clk=lambda: hw.OPENED_2==True, q=if_opened),
            RTRIG(clk=lambda: hw.OPENED_2==False, q=if_closed),
            RTRIG(clk=lambda: hw.OPENED_1==True, q=if_opened_2),
            RTRIG(clk=lambda: hw.OPENED_1==False, q=if_closed_2),
            RTRIG(clk=lambda: motor_11.state==Motor.RUN,q=on_motor_11_run),
            RTRIG(clk=lambda: motor_19.state==Motor.RUN,q=on_motor_19_run),
            RTRIG(clk=lambda: motor_18.state==Motor.RUN,q=on_motor_18_run),
            RTRIG(clk=lambda: motor_20.state==Motor.RUN,q=on_motor_20_run),
            RTRIG(clk=lambda: motor_22.state==Motor.RUN,q=on_motor_22_run),
            TP(clk=is_any_running,q=on_any_motor), level_3_monitor, level_4_monitor, siren_stop, motor_12_fault_siren
            #,fq_22,fq_24,fq_25
            )  #tuple быстее than []

if platform == 'linux':
  from imitation import IMotor,IRotation
  icompressor_28 = IMotor( q= hw.COMPRESSOR_ON_28, ison=hw.COMPRESSOR_ISON_28)
  ibelt_1 = IRotation( q = hw.MOTOR_ON_1, rot = hw.BELT_1 )
  ibelt_3 = IRotation( q = hw.MOTOR_ON_3, rot = hw.BELT_3 )
  ibelt_5 = IRotation( q = hw.MOTOR_ON_5, rot = hw.BELT_5 )
  ibelt_7 = IRotation( q = hw.MOTOR_ON_7, rot = hw.BELT_7 )
  ibelt_8 = IRotation( q = hw.MOTOR_ON_8, rot = hw.BELT_8 )
  ibelt_10 = IRotation( q = hw.MOTOR_ON_10, rot = hw.BELT_10 )
  ibelt_14 = IRotation( q = hw.MOTOR_ON_14, rot = hw.BELT_14 )
  ibelt_16 = IRotation( q = hw.MOTOR_ON_16, rot = hw.BELT_16 )
  ibelt_18 = IRotation( q = hw.MOTOR_ON_18, rot = hw.BELT_18 )
  ibelt_19 = IRotation( q = hw.MOTOR_ON_19, rot = hw.BELT_19 )
  ibelt_20 = IRotation( q = hw.MOTOR_ON_20, rot = hw.BELT_20 )
  irot_13 = IRotation( q = hw.AUGER_ON_13, rot = hw.AUGER_ROT_13 )
  irot_22 = IRotation( q = hw.AUGER_ON_22, rot = hw.AUGER_ROT_22 )
  irot_24 = IRotation( q = hw.AUGER_ON_24, rot = hw.AUGER_ROT_24 )
  irot_25 = IRotation( q = hw.AUGER_ON_25, rot = hw.AUGER_ROT_25 )
  imotor_2 = IMotor( q = hw.MOTOR_ON_2, ison = hw.MOTOR_ISON_2)
  imotor_4 = IMotor( q = hw.MOTOR_ON_4, ison = hw.MOTOR_ISON_4)
  imotor_6 = IMotor( q = hw.MOTOR_ON_6, ison = hw.MOTOR_ISON_6)
  imotor_11 = IMotor( q = hw.MOTOR_ON_11, ison = hw.MOTOR_ISON_11)
  imotor_13 = IMotor( q = hw.AUGER_ON_13, ison = hw.AUGER_ISON_13)
  imotor_15 = IMotor( q = hw.MOTOR_ON_15, ison = hw.MOTOR_ISON_15)
  imotor_17 = IMotor( q = hw.MOTOR_ON_17, ison = hw.MOTOR_ISON_17)

  instances += (icompressor_28,
                ibelt_1,ibelt_3,ibelt_5,ibelt_7,ibelt_8,ibelt_10,
                ibelt_14, ibelt_16, ibelt_18, ibelt_19, ibelt_20,
                irot_13,  irot_22, irot_24, irot_25,
                imotor_2,imotor_4,imotor_6,imotor_11,imotor_13,imotor_15,imotor_17)
  
plc.run( instances=instances, ctx=globals() )