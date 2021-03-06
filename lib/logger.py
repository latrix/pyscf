#!/usr/bin/env python
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#


'''
Logging system
**************

Log level
---------

======= ======
Level   number
------- ------
DEBUG4  9 
DEBUG3  8 
DEBUG2  7 
DEBUG1  6 
DEBUG   5 
INFO    4 
NOTE    3 
WARN    2 
ERROR   1 
QUIET   0 
======= ======

Big ``verbose`` number means more noise in the output file.

.. note::
    At log level 1 (ERROR) and 2 (WARN), the messages are also output to stderr.

Each Logger object has its own output destination and verbose level.  So
multiple Logger objects can be created to manage the message system without
affecting each other.
The methods provided by Logger class has the direct connection to the log level.
E.g.  :func:`info` print messages if the verbose level >= 4 (INFO):

>>> import sys
>>> from pyscf import lib
>>> log = lib.logger.Logger(sys.stdout, 4)
>>> log.info('info level')
info level
>>> log.verbose = 3
>>> log.info('info level')
>>> log.note('note level')
note level


timer
-----
Logger object provides timer method for timing.  Set :attr:`TIMER_LEVEL` to
control which level to output the timing.  It is 5 (DEBUG) by default.

>>> import sys, time
>>> from pyscf import lib
>>> log = lib.logger.Logger(sys.stdout, 4)
>>> t0 = time.clock()
>>> log.timer('test', t0)
>>> lib.logger.TIMER_LEVEL = 4
>>> log.timer('test', t0)
    CPU time for test      0.00 sec

'''

import sys
import time

from pyscf.lib import parameters as param

DEBUG4 = param.VERBOSE_DEBUG + 4
DEBUG3 = param.VERBOSE_DEBUG + 3
DEBUG2 = param.VERBOSE_DEBUG + 2
DEBUG1 = param.VERBOSE_DEBUG + 1
DEBUG  = param.VERBOSE_DEBUG
INFO   = param.VERBOSE_INFO
NOTE   = param.VERBOSE_NOTICE
NOTICE = NOTE
WARN   = param.VERBOSE_WARN
WARNING = WARN
ERR    = param.VERBOSE_ERR
ERROR  = ERR
QUIET  = param.VERBOSE_QUIET
CRIT   = param.VERBOSE_CRIT
ALERT  = param.VERBOSE_ALERT
PANIC  = param.VERBOSE_PANIC

TIMER_LEVEL  = param.TIMER_LEVEL

sys.verbose = NOTE

class Logger(object):
    def __init__(self, stdout=sys.stdout, verbose=NOTE):
        self.stdout = stdout
        self.verbose = verbose
        self._t0 = time.clock()
        self._w0 = time.time()

    def debug(self, msg, *args):
        debug(self, msg, *args)

    def debug1(self, msg, *args):
        debug1(self, msg, *args)

    def debug2(self, msg, *args):
        debug2(self, msg, *args)

    def debug3(self, msg, *args):
        debug3(self, msg, *args)

    def debug4(self, msg, *args):
        debug4(self, msg, *args)

    def info(self, msg, *args):
        info(self, msg, *args)

    def note(self, msg, *args):
        note(self, msg, *args)

    def warn(self, msg, *args):
        warn(self, msg, *args)

    def error(self, msg, *args):
        error(self, msg, *args)

    def log(self, msg, *args):
        log(self, msg, *args)

    def timer(self, msg, cpu0=None, wall0=None):
        if cpu0:
            return timer(self, msg, cpu0, wall0)
        else:
            self._t0, self._w0 = timer(self, msg, self._t0, wall0)
            return self._t0, self._w0

    def timer_debug1(self, msg, cpu0=None, wall0=None):
        if self.verbose >= DEBUG1:
            return self.timer(msg, cpu0, wall0)
        elif wall0:
            return time.clock(), time.time()
        else:
            return time.clock()

def flush(rec, msg, *args):
    rec.stdout.write(msg%args)
    rec.stdout.write('\n')
    rec.stdout.flush()

def log(rec, msg, *args):
    if rec.verbose > QUIET:
        flush(rec, msg, *args)

def error(rec, msg, *args):
    if rec.verbose >= ERROR:
        flush(rec, 'Error: '+msg, *args)
    sys.stderr.write('Error: ' + (msg%args) + '\n')

def warn(rec, msg, *args):
    if rec.verbose >= WARN:
        flush(rec, 'Warn: '+msg, *args)
    #if rec.stdout is not sys.stdout:
        sys.stderr.write('Warn: ' + (msg%args) + '\n')

def info(rec, msg, *args):
    if rec.verbose >= INFO:
        flush(rec, msg, *args)

def note(rec, msg, *args):
    if rec.verbose >= NOTICE:
        flush(rec, msg, *args)

def debug(rec, msg, *args):
    if rec.verbose >= DEBUG:
        flush(rec, msg, *args)

def debug1(rec, msg, *args):
    if rec.verbose >= DEBUG1:
        flush(rec, msg, *args)

def debug2(rec, msg, *args):
    if rec.verbose >= DEBUG2:
        flush(rec, msg, *args)

def debug3(rec, msg, *args):
    if rec.verbose >= DEBUG3:
        flush(rec, msg, *args)

def debug4(rec, msg, *args):
    if rec.verbose >= DEBUG4:
        flush(rec, msg, *args)

def stdout(rec, msg, *args):
    if rec.verbose >= DEBUG:
        flush(rec, msg, *args)
    sys.stdout.write('>>> %s\n' % msg)

def timer(rec, msg, cpu0, wall0=None):
    cpu1, wall1 = time.clock(), time.time()
    if wall0:
        if rec.verbose >= TIMER_LEVEL:
            flush(rec, ' '.join(('    CPU time for', msg,
                                 '%9.2f sec, wall time %9.2f sec')),
                  cpu1-cpu0, wall1-wall0)
        return cpu1, wall1
    else:
        if rec.verbose >= TIMER_LEVEL:
            flush(rec, ' '.join(('    CPU time for', msg, '%9.2f sec')),
                  cpu1-cpu0)
        return cpu1

def timer_debug1(rec, msg, cpu0, wall0=None):
    if rec.verbose >= DEBUG1:
        return timer(rec, msg, cpu0, wall0)
    elif wall0:
        return time.clock(), time.time()
    else:
        return time.clock()
