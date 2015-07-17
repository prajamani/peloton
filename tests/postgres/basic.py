#!/usr/bin/env python
# encoding: utf-8

## ==============================================
## GOAL : Test initdb, pg_ctl start and stop
## ==============================================

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

import sys
import shlex
import shutil
import tempfile
import os
import time
import logging

from subprocess import Popen, PIPE

## ==============================================
## LOGGING CONFIGURATION
## ==============================================

LOG = logging.getLogger(__name__)
LOG_handler = logging.StreamHandler()
LOG_formatter = logging.Formatter(
    fmt='%(asctime)s [%(funcName)s:%(lineno)03d] %(levelname)-5s: %(message)s',
    datefmt='%m-%d-%Y %H:%M:%S'
)
LOG_handler.setFormatter(LOG_formatter)
LOG.addHandler(LOG_handler)
LOG.setLevel(logging.INFO)


## ==============================================
## CONFIGURATION
## ==============================================

BASE_DIR = os.path.dirname(__file__)

initdb = 'initdb'
pg_ctl = 'pg_ctl'

## ==============================================
## UTILS
## ==============================================
def exec_cmd(cmd):
    """
    Execute the external command and get its exitcode, stdout and stderr.
    """
    args = shlex.split(cmd)

    proc = Popen(args, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    exitcode = proc.returncode

    print(out)
    print(err)
    sys.stdout.flush()
    assert(exitcode == 0)

## ==============================================
## MAIN
## ==============================================
if __name__ == '__main__':    
    
    LOG.info("Setting up temp data dir")
    temp_dir_path = tempfile.mkdtemp()
    LOG.info("Temp data dir : %s" % (temp_dir_path))

    LOG.info("Bootstrap data dir using initdb")
    cmd = initdb + ' ' + temp_dir_path
    exec_cmd(cmd)

    LOG.info("Starting the Peloton server")    
    cmd = pg_ctl + ' -D ' + temp_dir_path + ' -l logfile start'
    exec_cmd(cmd)
    
    LOG.info("Waiting for the server to start")    
    time.sleep(10)

    LOG.info("Stopping the Peloton server")        
    cmd = pg_ctl + ' -D ' + temp_dir_path + ' -l logfile stop'
    exec_cmd(cmd)
    
    LOG.info("Cleaning up the data dir")    
    shutil.rmtree(temp_dir_path)
    
    