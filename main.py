"""
Parses cable modem signal data
See http://www.dslreports.com/faq/16085 for acceptable signal ranges
@author ozigindere
"""

import ConfigParser
import os
import sys
import urllib2
import pprint
from sShamer import SignalShamer
from BeautifulSoup import BeautifulSoup

pp = pprint.PrettyPrinter(indent=4)

config = ConfigParser.ConfigParser()
config.read('modem.cfg')

argc = len(sys.argv)
if argc < 3:
    _IP_       = config.get('modem', 'ip')
    _PATH_     = config.get('modem', 'path')
    _PROTOCOL_ = config.get('modem', 'protocol')
    _MODEL_    = config.get('modem', 'model')
    _MAKE_     = config.get('modem', 'make')
    #if reading from cfg file we are accessing data via URL
    _type      = 'url'
    _source    = _PROTOCOL_ + '://' + _IP_ + '/' + _PATH_
elif argc >= 3:
    _type   = sys.argv[1]  #_type can be 'url' or 'file'
    _source = sys.argv[2]  #_source is either a url or a filename

if _type == 'url':
    doc = urllib2.urlopen(_source)
elif _type == 'file':
    doc = open(_source, 'r').read()
else:
    print'''Usage:
    python main.py <- reads default configuration values from ./modem.cfg
    python main.py [url|file] [http://...|filename.ext]
    '''
    exit(1)

sShamer = SignalShamer(BeautifulSoup(doc))

downStreamRes  = sShamer.get_downstream_values()
upStreamRes    = sShamer.get_upstream_values()
signalStatsRes = sShamer.get_signal_stat_values()

channelInfo = {}
for ii, channel in enumerate(downStreamRes[0]):
    channelInfo[int(channel)] = {'frequency': downStreamRes[1][ii],
                                 'signal_to_noise': downStreamRes[2][ii],
                                 'power_level': downStreamRes[3][ii]}

print('Total Channels: ' + str(len(channelInfo)))
pp.pprint(channelInfo)
