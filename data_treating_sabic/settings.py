import os

BASEDIR = os.path.dirname(os.path.dirname(__file__))

CONFIG_DIR = os.path.join(BASEDIR, 'config')

LOGLEVEL = 'DEBUG'
VERBOSE = True
LOGFILE = os.path.join(BASEDIR, 'log', 'process.log')
