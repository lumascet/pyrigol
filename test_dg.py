from math import pi
from RigolDG900 import RigolDG900
import time

gen = RigolDG900('TCPIP::192.168.0.109::INSTR')
gen.print_info()
# gen.reset()

#gen.setup_source(channel=1,shape=RigolDG900.waveform.SQUARE,duty=25.3, period='5ms', offset=RigolDG900.offset.MAXIMUM)
gen.setup_output(channel=1, impedance=RigolDG900.limit.INFINITY)
gen.setup_source(source=1, shape=RigolDG900.waveform.SINUSOID, frequency='10MHz',
                 amplitude='500mV', offset='100mV', phase='{0}rad'.format(pi/2))
gen.output_state(channel=1, state=1)

for s in RigolDG900.generic_function_list:
    gen.setup_source(source=1, shape=s, frequency='10MHz', offset='-100mV',
                     amplitude='500mVpp', duty=25, sample_rate='1MSa/s', phase='90deg')
    gen.beep()
    time.sleep(1)

# gen.setup_source(source=1, shape=RigolDG900.waveform.SEQUENCE, frequency='1MHz', offset='-100mV',
#                  amplitude='500mVpp', sample_rate='1MSa/s', phase='0deg')

gen.setup_source(1, RigolDG900.waveform.ABSSINE,
                 amplitude='2Vpp', frequency='100kHz', offset='50mV')


# gen.setup_channel(channel=2,on=0)

gen.close()
