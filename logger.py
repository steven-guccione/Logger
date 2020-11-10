#!/usr/bin/python3

"""
logger.py:  This python script is used to log commands
to monitior various system or application parameters.
This is used mostly for later graphing.

An example is a ping command, extracting the time delay in ms:

$ ./logger.py --command="ping -c 1 -w 60 google.com" --postprocess="split()[14][5:]" --delay=60

The output to the log file will be of the form:

2020-09-09 00:11:56,953 INFO 19.2
2020-09-09 00:12:57,063 INFO 21.9
2020-09-09 00:13:57,155 INFO 25.6
2020-09-09 00:14:57,217 INFO 23.7

Logs curently rotate every 24 hours at midnight and are kept for 31 days.

Version 1.0:  Sept. 3, 2020: Initial version
Version 1.1:  Nov. 5, 2020:  Cleaned up.  Updated subprocess.

"""

__author__    = "Steven A. Guccione"
__date__      = "November 5, 2020"
__copyright__ = "Copyright (c) 2020 by Steven A. Guccione"
__version__   = "1.1"

import argparse
import time
import subprocess
import os
import sys
import logging
from logging.handlers import TimedRotatingFileHandler

if __name__ == '__main__':

   # Parse command line parameters
   parser = argparse.ArgumentParser()
   parser.add_argument("--command", required=True, help="command to be executed")
   parser.add_argument("--filename", default="log", help="logfile name (default=log)")
   parser.add_argument("--postprocess", help="python string post-process command")
   parser.add_argument("--delay", type=int, help="delay in seconds (default=60)", default=60)
   parser.add_argument("--debug", help="debug flag", action='store_true')
   args = parser.parse_args()

   # Set up Logging   
   logger = logging.getLogger('loggerlog')
   if args.debug:
      logger.setLevel(logging.DEBUG)
   else:
      logger.setLevel(logging.INFO)

   # Rotate at midnight
   logHandler = TimedRotatingFileHandler(filename=args.filename, when="midnight", backupCount=31)
   logFormatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
   logHandler.setFormatter(logFormatter)
   logger.addHandler(logHandler)
   
   try:

      # Loop forever
      while True:

         try:
             
            # Run command
            cmd_out = subprocess.check_output(args.command, shell=True).decode()
            if args.debug:
               logger.debug(cmd_out)
            if args.postprocess:
               cmd_out = eval("cmd_out." + args.postprocess)
               if args.debug:
                  logger.debug(cmd_out)

         except Exception as e:
            # Something went wrong executing command
            logger.error(e)
            cmd_out = ""

         # Print to log
         if cmd_out:
            logger.info(cmd_out)

         # Delay (addition to time to run comand)
         time.sleep(args.delay)

   # Exit on CTRL-C
   except KeyboardInterrupt:
      logger.error("Execution interrupted.  Exiting.")
   # Any other unexpected error
   except Exception as e:
      logger.error(e)

   # Should never get here
   logger.error("Unkown error.  Main loop exited.")
   sys.exit(1)
