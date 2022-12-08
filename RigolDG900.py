import time
import re
from math import floor, log10, pi
import pyvisa as visa


class RigolDG900:

    # Constructor
    def __init__(self, resource, debug=False):
        resources = visa.ResourceManager('@py')
        # insert your device here
        # print(resources.list_resources()) #will show you the USB resource to put below
        self.fgen = resources.open_resource(resource)
        self.debug = debug

    def print_info(self):
        self.fgen.write('*IDN?')
        fullreading = self.fgen.read_raw()
        readinglines = fullreading.splitlines()
        print("Gen information: {0}".format(readinglines[0]))
        # time.sleep(2)

    def powerise10(self, x):
        """ Returns x as a*10**b with 0 <= a < 10"""
        if x == 0:
            return 0, 0
        Neg = x < 0
        if Neg:
            x = -x
        a = 1.0 * x / 10**(floor(log10(x)))
        b = int(floor(log10(x)))
        if Neg:
            a = -a
        return a, b

    def eng_notation(self, x):
        """Return a string representing x in an engineer friendly notation"""
        a, b = self.powerise10(x)
        if -3 < b < 3:
            return "%.4g" % x
        a = a * 10**(b % 3)
        b = b - b % 3
        return "%.4gE%s" % (a, b)

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

    def close(self):
        self.fgen.close()
        print("Closed USB session to fgen")

    def reset(self):
        self.fgen.write('*RST')
        print("Reset fgen")

    def setup_output(self, channel=1, impedance=limit.INFINITY, polarity=polarity.NORMAL):
        self.fgen.write(':OUTP' + str(channel) + ':IMP ' + str(impedance))
        self.fgen.write(':OUTP' + str(channel) + ':POL ' + str(polarity))
        print("CH" + str(channel) + ", impedance is " +
              str(impedance) + " polarity is " + str(polarity))

    def channel_align(self, channel=1):
        self.fgen.write(f':SOUR{channel}:PHAS:SYNC')
        print(f"Alligned other ouput to Channel {channel} ")

    def output_state(self, channel=1, state=1):
        if (state == 1):
            self.fgen.write(':OUTP' + str(channel) + ':STAT ' + 'ON')
            print("Turned on channel " + str(channel))
        else:
            self.fgen.write(':OUTP' + str(channel) + ':STAT ' + 'OFF')
            print("Turned off channel " + str(channel))

    def getClassVars(self, cl):
        return [val for key, val in cl.__dict__.items() if not key.startswith('__') and not callable(val)]

    def valueIsMemberOfClass(self, cl, value):
        return value in self.getClassVars(cl)

    generic_function_list = [waveform.NOISE, waveform.RS232, waveform.DC, waveform.DUALTONE, waveform.PRBS, waveform.HARMONIC,
                             waveform.PULSE, waveform.RAMP, waveform.SINUSOID, waveform.SQUARE, waveform.USER, waveform.SEQUENCE]

    def setup_source(self, source=1, shape=waveform.SINUSOID, frequency='1Hz', amplitude='5Vpp', offset='0V', duty=50.0, period='0ms', phase='0.0deg', freq_prbs='2kbps', sample_rate='2kbps'):
        match(shape):
            case self.waveform.NOISE | self.waveform.RS232:
                self.fgen.write(
                    f':SOUR{source}:APPL:{shape} {amplitude},{offset}')
                print(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t OFFSET: {offset}')

            case self.waveform.DC | self.waveform.DUALTONE:
                self.fgen.write(
                    f':SOUR{source}:APPL:{shape} {frequency},{amplitude},{offset}')
                print(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {frequency},\t OFFSET: {offset}')

            case self.waveform.HARMONIC | self.waveform.PULSE | self.waveform.RAMP | self.waveform.SINUSOID | self.waveform.SQUARE | self.waveform.USER:
                self.fgen.write(
                    f':SOUR{source}:APPL:{shape} {frequency},{amplitude},{offset},{self.__val_and_unit_to_real_val(phase)}')
                print(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {frequency},\t OFFSET: {offset},\t PHASE: {phase}')

            case self.waveform.SEQUENCE:
                self.fgen.write(
                    f':SOUR{source}:APPL:{shape} {sample_rate},{amplitude},{offset},{phase}')
                print(
                    f'Source set up NUMBER: {source}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t OFFSET: {offset},\t PHASE: {phase},\t Samplerate: {sample_rate}')

            case self.waveform.PRBS:
                self.fgen.write(
                    f':SOUR{source}:APPL:{shape} {freq_prbs},{amplitude},{offset}')
                print(
                    'Source set up NUMBER: {0}, SHAPE: {shape},\t AMPLITUDE: {amplitude},\t FREQUENCY: {freq_prbs},\t OFFSET: {offset},\t ')

            case others:
                self.setWaveform(source, shape)
                self.setFrequency(source, frequency)
                self.setVoltage(source, amplitude, offset)
                self.setPhase(source, self.__val_and_unit_to_real_val(phase))

        if shape is self.waveform.SQUARE:
            self.fgen.write(':SOUR' + str(source) + ':FUNC:SQU:DCYC ' +
                            str(self.__val_and_unit_to_real_val(duty)))

    def setWaveform(self, source=1, shape=waveform.SINUSOID):
        self.fgen.write(f':SOUR{source}:FUNC:SHAP {shape}')
        print(f'Source set up NUMBER: {source}, SHAPE: {shape}')

    def setFrequency(self, source=1, frequency='1Hz'):
        self.fgen.write(f':SOUR{source}:FREQ {frequency}')
        print(f'Source set up NUMBER: {source}, FREQUENCY: {frequency}')

    def setVoltage(self, source=1, amplitude='1V', offset='0V'):
        self.fgen.write(
            f':SOUR{source}:VOLT:OFFS {offset}'.format(source, offset))
        self.fgen.write(
            f':SOUR{source}:VOLT {amplitude}'.format(source, amplitude))
        print(
            f'Source set up NUMBER: {source}, AMPLITUDE: {amplitude},\t OFFSET: {offset}')

    def setPhase(self, source=1, phase='0deg'):
        self.fgen.write(':SOUR{source}:PHAS {phase}')
        print('Source set up NUMBER: {source}, PHASE: {phase}')

    def __val_and_unit_to_real_val(self, val_with_unit='1s'):
        # mostly not needed as dg900 understands units (except radians)
        if isinstance(val_with_unit, float):
            return val_with_unit
        if isinstance(val_with_unit, int):
            return val_with_unit
        if (self.valueIsMemberOfClass(self.limit, val_with_unit)):
            return val_with_unit
        number = float(re.search(r"([0-9.]+)", val_with_unit).group(0))
        unit = re.search(r"([a-zA-Z]+)", val_with_unit).group(0).lower()
        if (unit == 'mhz'):
            real_val_no_units = number * 1e6
        elif (unit == 'khz'):
            real_val_no_units = number * 1e3
        elif (unit == 's' or unit == 'v' or unit == 'Hz'):
            real_val_no_units = number
        elif (unit == 'ms' or unit == 'mv' or unit == 'mHz'):
            real_val_no_units = number * 1e-3
        elif (unit == 'us' or unit == 'uv'):
            real_val_no_units = number * 1e-6
        elif (unit == 'ns' or unit == 'nv'):
            real_val_no_units = number * 1e-9
        elif (unit == 'deg'):
            real_val_no_units = number
        elif (unit == 'rad'):
            real_val_no_units = number * 180 / pi
        else:
            real_val_no_units = number
        return real_val_no_units

    def beep(self):
        self.fgen.write(':SYST:BEEP:IMM')

    # def write_waveform_data(self, channel=1, filename=''):
    #     self.fgen.write(':WAV:SOUR: CHAN' + str(channel))
    #     time.sleep(1)
    #     self.fgen.write(':WAV:MODE NORM')
    #     self.fgen.write(':WAV:FORM ASC')
    #     self.fgen.write(':ACQ:MDEP?')
    #     fullreading = self.fgen.read_raw()
    #     readinglines = fullreading.splitlines()
    #     mdepth = int(readinglines[0])
    #     num_reads = int((mdepth / 15625) + 1)
    #     if (filename == ''):
    #         filename = "rigol_waveform_data_channel_" +
    #         str(channel) + "_" +
    #         datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    #     fid = open(filename, 'wb')
    #     print("Started saving waveform data for channel " + str(channel) +
    #           " " + str(mdepth) + " samples to filename " + '\"' + filename + '\"')
    #     for read_loop in range(0, num_reads):
    #         self.fgen.write(':WAV:DATA?')
    #         fullreading = self.fgen.read_raw()
    #         readinglines = fullreading.splitlines()
    #         reading = readinglines[0] + b'\n'
    #         reading = reading.replace(b',', b'\n')
    #         fid.write(reading[11:])
    #     fid.close()

    # def write_scope_settings_to_file(self, filename=''):
    # 	self.fgen.write(':SYST:SET?')
    # 	raw_data = self.fgen.read_raw()[11:] # strip off first 11 bytes

    # 	if (filename == ''):
    # 		filename = "rigol_settings_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") +".stp"
    # 	fid = open(filename, 'wb')
    # 	fid.write(raw_data)
    # 	fid.close()
    # 	print ("Wrote fgen settings to filename " + '\"' + filename + '\"')
    # 	time.sleep(5)

    # def restore_scope_settings_from_file(self, filename=''):
    # 	if (filename == ''):
    # 		print("ERROR: must specify filename\n")
    # 	else:
    # 		with open(filename, mode='rb') as file: # b is important -> binary
    # 			fileContent = file.read()
    # 			valList = list()
    # 			#alter ending to append new CRLF
    # 			fileContent = fileContent + chr(13) + chr(10)
    # 			#convert to a list that write_binary_values can iterate
    # 			for x in range(0,len(fileContent)-1):
    # 				valList.append(ord(fileContent[x]))
    # 			self.fgen.write_binary_values(':SYST:SET ', valList, datatype='B', is_big_endian=True)
    # 		print ("Wrote fgen settings to scope")
    # 		time.sleep(8)
