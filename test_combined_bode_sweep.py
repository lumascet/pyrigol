from math import pi
import os
import time
import numpy as np
from RigolDG900 import RigolDG900
from RigolDS1054Z import RigolDS1054Z
import matplotlib.pyplot as plt
import control
import datetime


def init_scope(scope):

    scope.print_info()
    scope.reset()

    scope.setup_mem_depth(24E6)
    scope.setup_channel(channel=1, on=1, offset_divs=0,
                        volts_per_div=1.5, probe=1)
    scope.setup_channel(channel=2, on=1, offset_divs=0,
                        volts_per_div=1.5, probe=1)
    scope.setup_timebase(time_per_div='1s', delay='5s')
    scope.setup_trigger(channel=1, level='1V')


def init_fgen(fgen):
    fgen.print_info()
    fgen.reset()

    fgen.setup_output(1)
    fgen.setup_source(1, shape=fgen.waveform.SINUSOID, amplitude='10Vpp')
    fgen.setSweep(source=1, starting_frequency=0.1, stop_frequency=1E3, sweep_time=10,
                  trigger_source=fgen.trigger.MANUAL, scale_type=fgen.scale.LOGARITHMIC)


def load_prev_waveforms(datetime):
    with open(f'waveforms/waveform_in_{datetime}.npy', 'rb') as f:
        data_in = np.load(f)
    with open(f'waveforms/waveform_out_{datetime}.npy', 'rb') as f:
        data_out = np.load(f)
    return data_in, data_out


def save_waveforms(data_in, data_out):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    if not os.path.exists('waveforms'):
        os.makedirs('waveforms')

    with open(f'waveforms/waveform_in_{timestamp}.npy', 'wb') as f:
        np.save(f, data_in)
    with open(f'waveforms/waveform_out_{timestamp}.npy', 'wb') as f:
        np.save(f, data_out)


DO_MEASUREMENT_CYCLE = False
PLOT_RESULTS = True
LOAD_MEASUREMENT_TIMESTAMP = '2022-12-09_15-27-09'

if __name__ == '__main__':

    scope = RigolDS1054Z('TCPIP::192.168.0.99::INSTR')
    fgen = RigolDG900('TCPIP::192.168.0.109::INSTR')

    if DO_MEASUREMENT_CYCLE:
        init_scope(scope)
        init_fgen(fgen)

        scope.single_trigger()
        time.sleep(2)
        fgen.output_state(1)
        fgen.triggerSweep(1)
        time.sleep(12)

        data_in = scope.get_waveform_data_uint8(channel=1)
        data_out = scope.get_waveform_data_uint8(channel=2)

        save_waveforms(data_in, data_out)

    else:
        data_in, data_out = load_prev_waveforms(LOAD_MEASUREMENT_TIMESTAMP)

    analog_in = scope.scale_waveform_uint8(data_in)
    analog_out = scope.scale_waveform_uint8(data_out)

    if (PLOT_RESULTS):
        plt.plot(range(len(analog_out)), analog_out)
        plt.plot(range(len(analog_in)), analog_in)
        plt.show()

    # TODO Calculate gain and phase diff

    # R = 1E6
    # C = 100E-9

    # tf = control.tf([1], [R*C, 1])
    # control.bode(tf, Hz=True, dB=True, deg=True)

    # plt.tight_layout()

    # ax1, ax2 = plt.gcf().axes     # get subplot axes

    # plt.sca(ax1)                 # magnitude plot
    # plt.plot(freq_set[g < 10], g[g < 10])

    # plt.sca(ax2)                 # phase plot
    # plt.plot(freq_set[pha < 10E2], pha[pha < 10E2])

    # plt.show()
