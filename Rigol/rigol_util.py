from math import floor, log10, pi
import re
import logging


def powerise10(x):
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


def eng_notation(x):
    """Return a string representing x in an engineer friendly notation"""
    a, b = powerise10(x)
    if -3 < b < 3:
        return "%.4g" % x
    a = a * 10**(b % 3)
    b = b - b % 3
    return "%.4gE%s" % (a, b)


def val_and_unit_to_real_val(val_with_unit='1s'):
    if isinstance(val_with_unit, float):
        return val_with_unit
    elif isinstance(val_with_unit, int):
        return val_with_unit
    elif isinstance(val_with_unit, str):
        number = float(re.search(r"([0-9.]+)", val_with_unit).group(0))
        unit = re.search(r"([a-zA-Z]+)", val_with_unit).group(0)
        if (unit == 'MHz'):
            real_val_no_units = number * 1e6
        elif (unit == 'kHz'):
            real_val_no_units = number * 1e3
        elif (unit == 's' or unit == 'V' or unit == 'Hz'):
            real_val_no_units = number
        elif (unit == 'ms' or unit == 'mV' or unit == 'mHz'):
            real_val_no_units = number * 1e-3
        elif (unit == 'us' or unit == 'uV'):
            real_val_no_units = number * 1e-6
        elif (unit == 'ns' or unit == 'nV'):
            real_val_no_units = number * 1e-9
        elif (unit == 'deg'):
            real_val_no_units = number
        elif (unit == 'rad'):
            real_val_no_units = number * 180 / pi
        else:
            real_val_no_units = number
        return real_val_no_units
    else:
        return val_with_unit


class CustomLogger(logging.Logger):

    def __init__(self, name, loglevel) -> None:
        super().__init__(name, loglevel)
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(loglevel)
        stream_handler.setFormatter(ColorFormatter())
        file_handler = logging.FileHandler(f'{name}.log')
        file_handler.setLevel(loglevel)
        file_handler.setFormatter(StandardFormatter())
        self.addHandler(file_handler)
        self.addHandler(stream_handler)


format_string = "%(asctime)s %(name)-12s  %(levelname)-8s  %(message)s (%(filename)s:%(lineno)d)"


class ColorFormatter(logging.Formatter):

    darkgrey = "\x1b[38;5;235m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: darkgrey + format_string + reset,
        logging.INFO: grey + format_string + reset,
        logging.WARNING: yellow + format_string + reset,
        logging.ERROR: red + format_string + reset,
        logging.CRITICAL: bold_red + format_string + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class StandardFormatter(logging.Formatter):

    FORMATS = {
        logging.DEBUG: format_string,
        logging.INFO: format_string,
        logging.WARNING: format_string,
        logging.ERROR: format_string,
        logging.CRITICAL: format_string
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
