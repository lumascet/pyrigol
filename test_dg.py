from math import pi
from Rigol.DG900 import RigolDG992
import time

fgen = RigolDG992('TCPIP::192.168.0.109::INSTR', RigolDG992.loglevel.DEBUG)
fgen.print_info()
# gen.reset()

fgen.query_command(':MMEM:CDIR?')
fgen.query_command(':MMEMory:CATalog?')
fgen.query_command(':MMEM:LOAD:DATA "a.RSF"')

# fgen.write_screen_capture()

# #gen.setup_source(channel=1,shape=fgen.waveform.SQUARE,duty=25.3, period='5ms', offset=fgen.offset.MAXIMUM)
# fgen.setup_output(channel=1, impedance=fgen.limit.INFINITY)
# fgen.setup_source(source=1, shape=fgen.waveform.SINUSOID, frequency='10MHz',
#                   amplitude='500mV', offset='100mV', phase=f'{pi/2}rad')
# fgen.output_state(channel=1, state=1)

# for s in fgen.generic_function_list:
#     fgen.setup_source(source=1, shape=s, frequency='10MHz', offset='-100mV',
#                       amplitude='500mVpp', duty=25, sample_rate='1MSa/s', phase='90deg')
#     fgen.beep()
#     time.sleep(2)

# # gen.setup_source(source=1, shape=fgen.waveform.SEQUENCE, frequency='1MHz', offset='-100mV',
# #                  amplitude='500mVpp', sample_rate='1MSa/s', phase='0deg')

# fgen.setup_source(1, fgen.waveform.ABSSINE,
#                   amplitude='2Vpp', frequency='100kHz', offset='50mV')

# # gen.setup_channel(channel=2,on=0)

# fgen.close()
