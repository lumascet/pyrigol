# Python Rigol control and measurement classes

## Supported Devices

### DS1000 class

Ported to work for python 3.10+. See [test_ds.py](test_ds.py) for an example file.

[Credits](https://github.com/charkster/rigol_ds1054z)

[Programming Guide](https://beyondmeasure.rigoltech.com/acton/attachment/1579/f-0386/1/-/-/-/-/DS1000Z_Programming%20Guide_EN.pdf)

### DG900 class

Should support all DG8xx and DG9xx like I used DG992 to test the script, as they are based on the same Hardware. You can connect a cheap USB/LAN adapter to connect via your local network. The USB input should also work.

Added class to apply basic waveforms via the python script. Some advanced features like sync or custom waveforms are still not done yet.
See [test_dg.py](test_dg.py) for an example file.

[Programming Guide](https://beyondmeasure.rigoltech.com/acton/attachment/1579/f-08aa/0/-/-/-/-/DG900_ProgrammingGuide_EN.pdf)

## Installation

Install required pip packages

```shell
 python3 -m pip install -r requirements.txt
```

and then just run

```shell
 python3 test_ds.py
```

or

```shell
 python3 test_dg.py
```

## Combined and automated measurements

See ```test_combined_bode.py``` for a automated bode plot measurement of electric circuits.

Below you can see the bode plots between a modeled low pass filter (blue) and the real measured LPF(R=1MOhm, C=100nF) (orange). The output voltage from the current generator has dropped due to the input impedance of the oscilloscope(1MOhm), resulting in half the measured voltage.

![](screenshots/BodePlot_RC_Lowpass.png)

Below you can see a direct Bode Measurement without DUT. So only the Bandwith of both, the signal generator as well as the oscilloscope were observed. As specified, they have the cutoff frequency at roughly 100MHz. Drawn in blue there is a reference PT1 transfer function with cutoff frequency at 100MHz. Scope and fgen were connected by a standard BNC cable with 50 Ohm termination.

![](screenshots/BodePlot_Hardware_Bandwidth.png)

### Bode sweep measurement

The previous measurement has the disadvantage being really slow, a frequency sweep with a combined waveform capture can greatly inprove the bode plot speed and resolution. TODO: Gain and phase diff calculation.

See ```test_combined_bode_sweep.py```

![](screenshots/raw_sweep.png)
