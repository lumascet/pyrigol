from rigol_dg992 import rigol_dg992
import time
#import smbus

# rigol_ds1054z class functions were writen to allow the high-level script
#  to be easy to read. Values with units are passed as strings, where the
#  unit can be stripped and converted to a base-10 value to be multiplied
#  by the value passed with it. This script sets up I2C decoding on the scope
#  to demonstrate triggering on SDA data (you don't need a slave device,
#  the scope is just observing the master write out to the bus)

gen = rigol_dg992('TCPIP::192.168.0.109::INSTR')
gen.print_info()
gen.reset()

gen.setup_channel(channel=1,on=1, impedance=123)
gen.setup_channel(channel=2,on=1)

gen.close()