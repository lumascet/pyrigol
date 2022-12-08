from math import pi
import time
import numpy as np
from RigolDG900 import RigolDG900
from RigolDS1054Z import RigolDS1054Z
import matplotlib.pyplot as plt
import control


def init_scope():
    scope = RigolDS1054Z('TCPIP::192.168.0.99::INSTR')
    scope.print_info()
    scope.reset()

    scope.setup_channel(channel=1, on=1, offset_divs=0,
                        volts_per_div=1.5, probe=1)
    scope.setup_channel(channel=2, on=1, offset_divs=0,
                        volts_per_div=1.5, probe=1)
    scope.setup_timebase(time_per_div='1ms')

    return scope


def init_fgen():
    fgen = RigolDG900('TCPIP::192.168.0.109::INSTR')
    fgen.print_info()
    fgen.reset()

    fgen.setup_output(1)
    fgen.setup_output(2)
    fgen.setup_source(1, shape=fgen.waveform.SINUSOID, amplitude='10Vpp')
    fgen.setup_source(2, shape=fgen.waveform.SINUSOID, amplitude='10Vpp')
    fgen.output_state(1)
    fgen.output_state(2)

    return fgen


if __name__ == '__main__':

    DATAPOINTS = 20
    freq_set = np.logspace(-1, 1, DATAPOINTS)
    freq_meas = np.empty(DATAPOINTS)
    vpp = np.empty(DATAPOINTS)
    pha = np.empty(DATAPOINTS)

    time_div_decades = 10
    time_div_start = 1
    time_div_array = np.array([])

    for i in range(time_div_start, time_div_start-time_div_decades, -1):
        time_div_array = np.append(
            time_div_array, np.array([5, 2, 1]) * 10**i)

    scope = init_scope()
    fgen = init_fgen()

    for i in range(DATAPOINTS):

        fgen.setFrequency(1, frequency=freq_set[i])
        fgen.setFrequency(2, frequency=freq_set[i])
        fgen.channel_align(1)
        timebase = 1/freq_set[i]/10

        for idx, val in enumerate(time_div_array):
            if val < timebase:
                time_div = time_div_array[idx-1]
                break

        scope.setup_timebase(time_per_div=time_div, delay=time_div*5)
        scope.single_trigger()
        time.sleep(3/freq_set[i])
        freq_meas[i] = scope.get_measurement(
            channel=1, meas_type=scope.frequency)
        vpp[i] = scope.get_measurement(
            channel=1, meas_type=scope.peak_to_peak_voltage)
        pha[i] = scope.get_measurement(
            channel=1, channel_compare=2, meas_type=scope.falling_phase_ratio)

    g = 20 * np.log10(vpp / 10)

    R = 1E6
    C = 100E-9

    tf = control.tf([1], [R*C, 1])
    control.bode(tf, Hz=True, dB=True, deg=True)

    plt.tight_layout()

    ax1, ax2 = plt.gcf().axes     # get subplot axes

    plt.sca(ax1)                 # magnitude plot
    plt.plot(freq_set[g < 10], g[g < 10])

    plt.sca(ax2)                 # phase plot
    plt.plot(freq_set[pha < 10E2], pha[pha < 10E2])

    plt.show()
