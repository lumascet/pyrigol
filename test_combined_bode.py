from math import log10, pi
import time
import numpy as np
from Rigol.DG900 import RigolDG992
from Rigol.DS1000 import RigolDS1054Z
import matplotlib.pyplot as plt
import control

# Script to measure Bode Transfer function
# CH1 is DUT, CH2 is Reference
# Creates #DATAPOINTS single measurements in logarithmic freq_range


VPP_SET = 1
START_FREQ = 1E6
STOP_FREQ = 100E6
DATAPOINTS = 50
freq_range = np.logspace(log10(START_FREQ), log10(STOP_FREQ), DATAPOINTS)

freq_meas = np.empty(DATAPOINTS)
vpp = np.empty(DATAPOINTS)
pha = np.empty(DATAPOINTS)

time_div_decades = 11
time_div_start = 1
time_div_array = np.array([])

for i in range(time_div_start, time_div_start-time_div_decades, -1):
    time_div_array = np.append(
        time_div_array, np.array([5, 2, 1]) * 10**i)

scope = RigolDS1054Z('TCPIP::192.168.0.99::INSTR',
                     loglevel=RigolDS1054Z.loglevel.INFO)
fgen = RigolDG992('TCPIP::192.168.0.109::INSTR',
                  loglevel=RigolDG992.loglevel.INFO)
fgen.print_info()
# fgen.reset()
scope.print_info()
# scope.reset()


scope.setup_channel(channel=1, on=1, offset_divs=0,
                    volts_per_div=VPP_SET/6, probe=1)
scope.setup_channel(channel=2, on=1, offset_divs=0,
                    volts_per_div=VPP_SET/6, probe=1)


fgen.setup_output(1, impedance=50)
fgen.setup_output(2, impedance=50)
fgen.setup_source(1, shape=fgen.waveform.SINUSOID, amplitude=f'{VPP_SET}Vpp')
fgen.setup_source(2, shape=fgen.waveform.SINUSOID, amplitude=f'{VPP_SET}Vpp')
fgen.output_state(1)
fgen.output_state(2)
fgen.setCoupling(source=1, state=1)

for i in range(DATAPOINTS):

    fgen.setFrequency(1, frequency=freq_range[i])
    fgen.setFrequency(2, frequency=freq_range[i])
    timebase = 1/freq_range[i]/10

    for idx, val in enumerate(time_div_array):
        if val < timebase:
            time_div = time_div_array[idx-1]
            break

    scope.setup_timebase(time_per_div=time_div, delay=time_div*5)
    scope.single_trigger()
    time.sleep(3/freq_range[i])
    freq_meas[i] = scope.get_measurement(
        channel=1, meas_type=scope.frequency)
    vpp[i] = scope.get_measurement(
        channel=1, meas_type=scope.peak_to_peak_voltage)
    pha[i] = scope.get_measurement(
        channel=1, channel_compare=2, meas_type=scope.falling_phase_ratio)

g = 20 * np.log10(vpp / VPP_SET)

omega0 = 100E6
T = 1/(2*pi*omega0)  # R*C

tf = control.tf([1], [T, 1])
control.bode(tf, Hz=True, dB=True, deg=True)

plt.tight_layout()

ax1, ax2 = plt.gcf().axes     # get subplot axes

filt_indexes = (g < 10) & (pha < 10E2)

plt.sca(ax1)                 # magnitude plot
plt.plot(freq_range[filt_indexes], g[filt_indexes])

plt.sca(ax2)                 # phase plot
plt.plot(freq_range[filt_indexes], pha[filt_indexes])

plt.show()
