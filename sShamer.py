"""
SignalShamer Class
@ToDo: Implement an interface that defines base methods for parsing values

From http://www.dslreports.com/faq/16085 :
It's recommended to have the modem's signal levels at least 3dB away from the
maximum/minimum levels listed above due to normal temperature related signal
variation. If the modem's signal levels are at the maximum or minimum limits,
they may be out of spec. if the temperature changes significantly. Signal levels
that vary more then 3 dB in a 24-hour period usually indicate a problem that
should be looked into.

@author ozigindere
"""

class SignalShamer(object):

    ranges = {"power_level": {"recommended": {"min": -7, "max": 7, "unit": "dBmV"},
                              "acceptable": {"min": -10, "max": 10, "unit": "dBmV"},
                              "maximum": {"min": -15, "max": 15, "unit": "dBmV"},
                              "out_of_spec": {"min": -16, "max": 16, "unit": "dBmV"}},
              "signal_to_noise": {"QAM" : {"256": {"min": 30, "recommended": 33, "unit": "dB"},
                                           "64": {"min": 24, "recommended": 27, "unit": "dB"},
                                           "16": {"min": 18, "recommended": 21, "unit": "dB"}},
                                  "QPSK": {"min": 12, "recommended": 15, "unit": "dB"}}}

    def __init__(self, soup):
        self.soup = soup
        self.tables = self.find_tables()

    def find_tables(self):
        # SB6141 has 4 tables
        # <table>[0] => Downstream
        # <table>[1] => this is embedded in a <td> in <table>[0]
        # <table>[2] => Upstream
        # <table>[3] => Signal Stats (Codewords)
        return self.soup.findAll('table')

    def clean_string(self, s):
        return s.replace("&nbsp;", "").strip()

    def get_downstream_values(self):
        downstreamRows = self.tables[0].findAll('tr')
        channelIDs = downstreamRows[1].findAll('td')
        frequencies = downstreamRows[2].findAll('td')
        sig2NoiseRatios = downstreamRows[3].findAll('td')
        powerLevels = downstreamRows[5].findAll('td')

        channels = []
        for ii, channelID in enumerate(channelIDs):
            if ii == 0:  # skip label
                continue
            val = self.clean_string(channelID.string)
            channels.append(val)

        freq = []
        for ii, frequency in enumerate(frequencies):
            if ii == 0:  # skip label
                continue
            val = self.clean_string(frequency.string)
            freq.append(val)

        sig2noise = []
        for ii, s2n in enumerate(sig2NoiseRatios):
            if ii == 0:  # skip label
                continue
            val = self.clean_string(s2n.string)
            sig2noise.append(val)

        pwr = []
        for ii, pwrLvl in enumerate(powerLevels):
            if ii == 0 or ii == 1:  # skip label and the next <td> value
                continue
            val = self.clean_string(pwrLvl.string)
            pwr.append(val)

        return channels, freq, sig2noise, pwr

    def get_upstream_values(self):
        pass

    def get_signal_stat_values(self):
        pass
