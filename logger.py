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

"""

__author__    = "Steven A. Guccione"
__date__      = "September 3, 2020"
__copyright__ = "Copyright (c) 2020 by Steven A. Guccione"

import argparse
import datetime
import time
import subprocess
import logging
from logging.handlers import TimedRotatingFileHandler

if __name__ == '__main__':

   # Parse command line parameters
   parser = argparse.ArgumentParser()
   parser.add_argument("--command", required=True, help="command")
   parser.add_argument("--filename", default="log", help="logfile name (default=log)")
   parser.add_argument("--postprocess", help="python post-process command")
   parser.add_argument("--delay", type=int, help="delay in seconds (default=60)", default=60)
   parser.add_argument("--debug", help="debug flag", action='store_true')
   args = parser.parse_args()

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
      while True:

         # Get current time for timestamp
         current_time = datetime.datetime.today()
         if args.debug:
            print(current_time)

         try:
             
            # Run command
            p = subprocess.Popen(args.command, shell=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            out, err = p.communicate()

            # Get the command output
            cmd_out = out.decode("ASCII")
            if args.debug:
               logger.debug(cmd_out)
            if args.postprocess:
               cmd_out = eval("cmd_out." + args.postprocess)
               if args.debug:
                  logger.debug(cmd_out)

         except Exception as e:
            # Something went wrong executing command
            logger.error(e)
            
         logger.info(cmd_out)

         # Total delay will include time to ping
         time.sleep(args.delay)

   # Exit on CTRL-C
   except KeyboardInterrupt:
      logger.error("Execution interrupted.  Exiting.")
   # Any other error
   except Exception as e:
      logger.error(e)
   
   SystemExit(0)
