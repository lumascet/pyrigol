import datetime
import time
import pyvisa as visa
import logging
from Rigol.rigol_util import val_and_unit_to_real_val, CustomLogger


class _RigolDG900:

    # Constructor
    def __init__(self, resource, loglevel=logging.INFO):
        self.logger = CustomLogger(self.__class__.__name__, loglevel)

        try:
            resources = visa.ResourceManager('@py')
            self.device = resources.open_resource(resource)
        except visa.Error as error:
            self.logger.critical(error.description)
            exit(-1)

    def send_command(self, command):
        self.logger.debug(f'Sent command: {command}')
        self.device.write(command)

    def read_response(self):
        buffer = self.device.read_raw()
        self.logger.debug(f'Got response: {buffer}')
        return buffer

    def query_command(self, command):
        buffer = self.device.query(command)
        filtered_buffer = buffer.replace("\n", "\\n")
        self.logger.debug(f'Query sent: {command}, got: {filtered_buffer}')
        return buffer

    def getClassVars(self, cl):
        return [val for key, val in cl.__dict__.items() if not key.startswith('__') and not callable(val)]

    def valueIsMemberOfClass(self, cl, value):
        return value in self.getClassVars(cl)

    # CONSTANTS

    class loglevel:
        INFO = logging.INFO
        WARNING = logging.WARNING
        ERROR = logging.ERROR
        CRITICAL = logging.CRITICAL
        DEBUG = logging.DEBUG

    class scale:
        LINEAR = "LIN"
        LOGARITHMIC = "LOG"
        STEP = "STE"

    class trigger:
        INTERNAL = "INT",
        EXTERNAL = "EXT",
        MANUAL = "MAN"

    class waveform:
        SINUSOID = "SIN"
        SQUARE = "SQU"
        RAMP = "RAMP"
        PULSE = "PULSE"
        PULSE = "PULS"
        NOISE = "NOIS"
        USER = "USER"
        HARMONIC = "HARM"
        DC = "DC"
        KAISER = "KAISER"
        ROUNDPM = "ROUNDPM"
        SINC = "SINC"
        NEGRAMP = "NEGRAMP"
        ATTALT = "ATTALT"
        AMPALT = "AMPALT"
        STAIRDN = "STAIRDN"
        STAIRUP = "STAIRUP"
        STAIRUD = "STAIRUD"
        CPULSE = "CPULSE"
        PPULSE = "PPULSE"
        NPULSE = "NPULSE"
        TRAPEZIA = "TRAPEZIA"
        ROUNDHALF = "ROUNDHALF"
        ABSSINE = "ABSSINE"
        ABSSINEHALF = "ABSSINEHALF"
        SINETRA = "SINETRA"
        SINEVER = "SINEVER"
        EXPRISE = "EXPRISE"
        EXPFALL = "EXPFALL"
        TAN = "TAN"
        COT = "COT"
        SQRT = "SQRT"
        X2DATA = "X2DATA"
        GAUSS = "GAUSS"
        HAVERSINE = "HAVERSINE"
        LORENTZ = "LORENTZ"
        DIRICHLET = "DIRICHLET"
        GAUSSPULSE = "GAUSSPULSE"
        AIRY = "AIRY"
        CARDIAC = "CARDIAC"
        QUAKE = "QUAKE"
        GAMMA = "GAMMA"
        VOICE = "VOICE"
        TV = "TV"
        COMBIN = "COMBIN"
        BANDLIMITED = "BANDLIMITED"
        STEPRESP = "STEPRESP"
        BUTTERWORTH = "BUTTERWORTH"
        CHEBYSHEV1 = "CHEBYSHEV1"
        CHEBYSHEV2 = "CHEBYSHEV2"
        BOXCAR = "BOXCAR"
        BARLETT = "BARLETT"
        TRIANG = "TRIANG"
        BLACKMAN = "BLACKMAN"
        HAMMING = "HAMMING"
        HANNING = "HANNING"
        DUALTONE = "DUALTONE"
        ACOS = "ACOS"
        ACOSH = "ACOSH"
        ACOTCON = "ACOTCON"
        ACOTPRO = "ACOTPRO"
        ACOTHCON = "ACOTHCON"
        ACOTHPRO = "ACOTHPRO"
        ACSCCON = "ACSCCON"
        ACSCPRO = "ACSCPRO"
        ACSCHCON = "ACSCHCON"
        ACSCHPRO = "ACSCHPRO"
        ASECCON = "ASECCON"
        ASECPRO = "ASECPRO"
        ASECH = "ASECH"
        ASIN = "ASIN"
        ASINH = "ASINH"
        ATAN = "ATAN"
        ATANH = "ATANH"
        BESSELJ = "BESSELJ"
        BESSELY = "BESSELY"
        CAUCHY = "CAUCHY"
        COSH = "COSH"
        COSINT = "COSINT"
        COTHCON = "COTHCON"
        COTHPRO = "COTHPRO"
        CSCCON = "CSCCON"
        CSCPRO = "CSCPRO"
        CSCHCON = "CSCHCON"
        CSCHPRO = "CSCHPRO"
        CUBIC = "CUBIC"
        ERF = "ERF"
        ERFC = "ERFC"
        ERFCINV = "ERFCINV"
        ERFINV = "ERFINV"
        LAGUERRE = "LAGUERRE"
        LAPLACE = "LAPLACE"
        LEGEND = "LEGEND"
        LOG = "LOG"
        LOGNORMAL = "LOGNORMAL"
        MAXWELL = "MAXWELL"
        RAYLEIGH = "RAYLEIGH"
        RECIPCON = "RECIPCON"
        RECIPPRO = "RECIPPRO"
        SECCON = "SECCON"
        SECPRO = "SECPRO"
        SECH = "SECH"
        SINH = "SINH"
        SININT = "SININT"
        TANH = "TANH"
        VERSIERA = "VERSIERA"
        WEIBULL = "WEIBULL"
        BARTHANN = "BARTHANN"
        BLACKMANH = "BLACKMANH"
        BOHMANWIN = "BOHMANWIN"
        CHEBWIN = "CHEBWIN"
        FLATTOPWIN = "FLATTOPWIN"
        NUTTALLWIN = "NUTTALLWIN"
        PARZENWIN = "PARZENWIN"
        TAYLORWIN = "TAYLORWIN"
        TUKEYWIN = "TUKEYWIN"
        CWPUSLE = "CWPUSLE"
        LFPULSE = "LFPULSE"
        LFMPULSE = "LFMPULSE"
        EOG = "EOG"
        EEG = "EEG"
        EMG = "EMG"
        PULSILOGRAM = "PULSILOGRAM"
        TENS1 = "TENS1"
        TENS2 = "TENS2"
        TENS3 = "TENS3"
        SURGE = "SURGE"
        DAMPEDOSC = "DAMPEDOSC"
        SWINGOSC = "SWINGOSC"
        RADAR = "RADAR"
        THREEAM = "THREEAM"
        THREEFM = "THREEFM"
        THREEPM = "THREEPM"
        THREEPWM = "THREEPWM"
        THREEPFM = "THREEPFM"
        RESSPEED = "RESSPEED"
        MCNOSIE = "MCNOSIE"
        PAHCUR = "PAHCUR"
        RIPPLE = "RIPPLE"
        ISO76372TP1 = "ISO76372TP1"
        ISO76372TP2A = "ISO76372TP2A"
        ISO76372TP2B = "ISO76372TP2B"
        ISO76372TP3A = "ISO76372TP3A"
        ISO76372TP3B = "ISO76372TP3B"
        ISO76372TP4 = "ISO76372TP4"
        ISO76372TP5A = "ISO76372TP5A"
        ISO76372TP5B = "ISO76372TP5B"
        ISO167502SP = "ISO167502SP"
        ISO167502VR = "ISO167502VR"
        SCR = "SCR"
        IGNITION = "IGNITION"
        NIMHDISCHARGE = "NIMHDISCHARGE"
        GATEVIBR = "GATEVIBR"
        PRBS = "PRBS"
        SEQUENCE = "SEQ"
        RS232 = "RS232"

    class limit:
        NORMAL = "NORM"
        DEFAULT = "DEF"
        MINIMUM = "MIN"
        MAXIMUM = "MAX"
        INFINITY = "INF"

    class polarity:
        NORMAL = "NORM"
        INVERTED = "INV"

    class slope:
        POSITIVE = "POS",
        NEGATIVE = "NEG"

    generic_function_list = [waveform.NOISE, waveform.RS232, waveform.DC, waveform.DUALTONE, waveform.PRBS, waveform.HARMONIC,
                             waveform.PULSE, waveform.RAMP, waveform.SINUSOID, waveform.SQUARE, waveform.USER, waveform.SEQUENCE]

    # OUTPUT

    def setup_output(self, channel=1, impedance=limit.INFINITY, polarity=polarity.NORMAL):
        self.send_command(':OUTP' + str(channel) + ':IMP ' + str(impedance))
        self.send_command(':OUTP' + str(channel) + ':POL ' + str(polarity))
        self.logger.info("CH" + str(channel) + ", impedance is " +
                         str(impedance) + " polarity is " + str(polarity))

    def output_state(self, channel=1, state=1):
        if (state == 1):
            self.send_command(':OUTP' + str(channel) + ':STAT ' + 'ON')
            self.logger.info("Turned on channel " + str(channel))
        else:
            self.send_command(':OUTP' + str(channel) + ':STAT ' + 'OFF')
            self.logger.info("Turned off channel " + str(channel))

    # SOURCE

    def setup_source(self, source=1, shape=waveform.SINUSOID, frequency='1Hz', amplitude='5Vpp', offset='0V', duty=50.0, period='0ms', phase='0.0deg', freq_prbs='2kbps', sample_rate='2kbps'):
        match(shape):
            case self.waveform.NOISE | self.waveform.RS232:
                self.send_command(
                    f':SOUR{source}:APPL:{shape} {amplitude},{offset}')
                self.logger.info(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t OFFSET: {offset}')

            case self.waveform.DC | self.waveform.DUALTONE:
                self.send_command(
                    f':SOUR{source}:APPL:{shape} {frequency},{amplitude},{offset}')
                self.logger.info(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {frequency},\t OFFSET: {offset}')

            case self.waveform.HARMONIC | self.waveform.PULSE | self.waveform.RAMP | self.waveform.SINUSOID | self.waveform.SQUARE | self.waveform.USER:
                self.send_command(
                    f':SOUR{source}:APPL:{shape} {frequency},{amplitude},{offset},{val_and_unit_to_real_val(phase)}')
                self.logger.info(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {frequency},\t OFFSET: {offset},\t PHASE: {phase}')

            case self.waveform.SEQUENCE:
                self.send_command(
                    f':SOUR{source}:APPL:{shape} {sample_rate},{amplitude},{offset},{phase}')
                self.logger.info(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t OFFSET: {offset},\t PHASE: {phase},\t Samplerate: {sample_rate}')

            case self.waveform.PRBS:
                self.send_command(
                    f':SOUR{source}:APPL:{shape} {freq_prbs},{amplitude},{offset}')
                self.logger.info(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {freq_prbs},\t OFFSET: {offset},\t ')

            case others:
                self.setWaveform(source, shape)
                self.setFrequency(source, frequency)
                self.setVoltage(source, amplitude, offset)
                self.setPhase(source, val_and_unit_to_real_val(phase))

        if shape is self.waveform.SQUARE:
            self.send_command(':SOUR' + str(source) + ':FUNC:SQU:DCYC ' +
                              str(val_and_unit_to_real_val(duty)))

    def setSweep(self, source=1, state=1, starting_frequency=0, stop_frequency=0, center_frequency=0, frequency_span=0, sweep_time=0, return_time=0, scale_type=scale.LINEAR, steps=0, trigger_source=trigger.INTERNAL, trigger_slope=slope.POSITIVE):
        self.send_command(f':SOUR{source}:SWE:STAT {state}')
        time.sleep(0.1)
        if starting_frequency and stop_frequency:
            self.send_command(
                f':SOUR{source}:FREQ:STAR {starting_frequency}')
            time.sleep(0.1)
            self.send_command(f':SOUR{source}:FREQ:STOP {stop_frequency}')
            time.sleep(0.1)
        elif center_frequency and frequency_span:
            self.send_command(f':SOUR{source}:FREQ:CENT {center_frequency}')
            time.sleep(0.1)
            self.send_command(f':SOUR{source}:FREQ:SPAN {frequency_span}')
            time.sleep(0.1)
        if return_time:
            self.send_command(f':SOUR{source}:SWE:RTIM {return_time}')
            time.sleep(0.1)
        if sweep_time:
            self.send_command(f':SOUR{source}:SWE:TIME {sweep_time}')
            time.sleep(0.1)
        if steps:
            self.send_command(f':SOUR{source}:SWE:STEP {steps}')
            time.sleep(0.1)

        self.send_command(f':SOUR{source}:SWE:TRIG:SOUR {trigger_source}')
        time.sleep(0.1)
        if trigger_source == self.trigger.EXTERNAL:
            self.send_command(f':SOUR{source}:SWE:TRIG:SLOP {trigger_slope}')
            time.sleep(0.1)

        self.send_command(f':SOUR{source}:SWE:SPAC {scale_type}')
        time.sleep(0.1)

    def triggerSweep(self, source=1):
        # self.fgen.write(f':SOUR{source}:SWE:TRIG') # not working for me
        self.send_command(f':TRIG{source}')

    def setWaveform(self, source=1, shape=waveform.SINUSOID):
        self.send_command(f':SOUR{source}:FUNC:SHAP {shape}')
        self.logger.info(f'Source set up NUMBER: {source}, SHAPE: {shape}')

    def setFrequency(self, source=1, frequency='1Hz'):
        self.send_command(f':SOUR{source}:FREQ {frequency}')
        self.logger.info(
            f'Source set up NUMBER: {source}, FREQUENCY: {frequency}')

    def setVoltage(self, source=1, amplitude='1V', offset='0V'):
        self.send_command(
            f':SOUR{source}:VOLT:OFFS {offset}'.format(source, offset))
        self.send_command(
            f':SOUR{source}:VOLT {amplitude}'.format(source, amplitude))
        self.logger.info(
            f'Source set up NUMBER: {source}, AMPLITUDE: {amplitude},\t OFFSET: {offset}')

    def setPhase(self, source=1, phase='0deg'):
        self.send_command(f':SOUR{source}:PHAS {phase}')
        self.logger.info(f'Source set up NUMBER: {source}, PHASE: {phase}')

    def channel_align(self, channel=1):
        self.send_command(f':SOUR{channel}:PHAS:SYNC')
        self.logger.info(f"Alligned other ouput to Channel {channel} ")

    # COUPLING

    # ALL

    def setCoupling(self, source=1, state=1):
        self.send_command(f':COUP{source} {state}')
        self.logger.info(
            f'Coupling set up SOURCE: {source}, STATE: {state}')

    # TRIGGER

    def setTriggerCoupling(self, source=1, state=1):
        self.send_command(f':COUP{source}:TRI {state}')
        self.logger.info(
            f'Trigger coupling set up SOURCE: {source}, STATE: {state}')

    # FREQUENCY

    def setFrequencyCoupling(self, source=1, state=1):
        self.send_command(f':COUP{source}:FREQ {state}')
        self.logger.info(
            f'Frequency coupling set up SOURCE: {source}, STATE: {state}')

    def setFrequencyCouplingRatio(self, source=1, ratio=1):
        self.send_command(f':COUP{source}:FREQ:RAT {ratio}')
        self.logger.info(
            f'Frequency ratio coupling set up SOURCE: {source}, Ratio: {ratio}')

    def setFrequencyCouplingMode(self, source=1, mode='RAT'):
        self.send_command(f':COUP{source}:FREQ:MODE {mode}')
        self.logger.info(
            f'Frequency coupling mode set up SOURCE: {source}, MODE: {mode}')

    # PHASE

    def setPhaseCoupling(self, source=1, state=1):
        self.send_command(f':COUP{source}:PHAS {state}')
        self.logger.info(
            f'Phase coupling set up SOURCE: {source}, STATE: {state}')

    def setPhaseCouplingRatio(self, source=1, ratio=1):
        self.send_command(f':COUP{source}:PHAS:RAT {ratio}')
        self.logger.info(
            f'Phase coupling ratio set up SOURCE: {source}, RATIO: {ratio}')

    def setPhaseCouplingMode(self, source=1, mode='RAT'):
        self.send_command(f':COUP{source}:PHAS:MODE {mode}')
        self.logger.info(
            f'Phase coupling mode set up SOURCE: {source}, MODE: {mode}')

    def setPhaseCouplingDeviation(self, source=1, deviation='RAT'):
        self.send_command(f':COUP{source}:PHAS:DEV {deviation}')
        self.logger.info(
            f'Phase coupling mode set up SOURCE: {source}, DEVIATION: {deviation}')

    # AMPLITUDE

    def setAmplitudeCoupling(self, source=1, state=1):
        self.send_command(f':COUP{source}:AMPL {state}')
        self.logger.info(
            f'Amplitude coupling set up SOURCE: {source}, STATE: {state}')

    def setAmplitudeCouplingRatio(self, source=1, ratio=1):
        self.send_command(f':COUP{source}:AMPL:RAT {ratio}')
        self.logger.info(
            f'Amplitude coupling ratio set up SOURCE: {source}, RATIO: {ratio}')

    def setAmplitudeCouplingMode(self, source=1, mode='RAT'):
        self.send_command(f':COUP{source}:AMPL:MODE {mode}')
        self.logger.info(
            f'Amplitude coupling mode set up SOURCE: {source}, MODE: {mode}')

    def setAmplitudeCouplingDeviation(self, source=1, deviation='RAT'):
        self.send_command(f':COUP{source}:AMPL:DEV {deviation}')
        self.logger.info(
            f'Amplitude coupling mode set up SOURCE: {source}, DEVIATION: {deviation}')

    # SYSTEM

    def close(self):
        self.device.close()
        self.logger.info("Closed USB session to fgen")

    def reset(self):
        self.send_command('*RST')
        self.logger.warning("Reset fgen")
        time.sleep(4)

    def beep(self):
        self.send_command(':SYST:BEEP:IMM')

    def write_screen_capture(self, filename=''):
        self.send_command(':HCOP:SDUM:DATA:FORM PNG')
        self.send_command(':HCOP:SDUM:DATA?')
        # strip off first 9 bytes
        raw_data = self.read_response()[11:]
        # save image file
        if (filename == ''):
            filename = "rigol_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".png"
        fid = open(filename, 'wb')
        fid.write(raw_data)
        fid.close()
        self.logger.info("Wrote screen capture to filename " +
                         '\"' + filename + '\"')
        time.sleep(5)

    def print_info(self):
        self.send_command('*IDN?')
        fullreading = self.read_response()
        readinglines = fullreading.splitlines()
        self.logger.info(f"Gen information: {readinglines[0]}")
        # time.sleep(2)


class RigolDG811(_RigolDG900):
    pass


class RigolDG812(_RigolDG900):
    pass


class RigolDG821(_RigolDG900):
    pass


class RigolDG822(_RigolDG900):
    pass


class RigolDG831(_RigolDG900):
    pass


class RigolDG952(_RigolDG900):
    pass


class RigolDG972(_RigolDG900):
    pass


class RigolDG992(_RigolDG900):
    pass
