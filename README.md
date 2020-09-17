# Logger
Flexible Event Logger

Logger is a flexible event logger written in Python.  It uses standard Python logging packages and uses rotating logs, rotating every night at midnight by default.  The command line help is:

```
$ ./logger.py --help
usage: logger.py [-h] --command COMMAND [--filename FILENAME] [--postprocess POSTPROCESS]
                 [--delay DELAY] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --command COMMAND     command
  --filename FILENAME   logfile name (default=log)
  --postprocess POSTPROCESS
                        python post-process command
  --delay DELAY         delay in seconds (default=60)
  --debug               debug flag
```

The `--command` is an OS executable command used to collect data.  The `--postprocess` flag specifies a Python command used to process the output of the command.  An example of this is getting the delay time of the Linux `ping` command.  In this case a command of the form:

```
./logger.py --command="ping -c 1 -w 60 google.com" --postprocess="split()[14][5:]" --delay=60
```

will execute a `ping` command to `google.com` every 60 seconds.  The result of a `ping` command, however, is several lines of text as below:

```
$ ping -c 1 -w 60 google.com
PING google.com (172.217.2.238) 56(84) bytes of data.
64 bytes from dfw28s01-in-f14.1e100.net (172.217.2.238): icmp_seq=1 ttl=115 time=28.2 ms

--- google.com ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 28.245/28.245/28.245/0.000 ms

```

In order to break this down into something more manageable for the logs, the `postprocess` flag of `"split()[14][5:]"` splits the returned text according to whitespace.  The 14th element of this split text is `time=28.2` with the final `[:5]` returning the numeric porting past the `"time="` string, in this case `"28.2"`.  This produces log files of the form:

```
2020-09-16 00:15:30,524 INFO 21.5
2020-09-16 00:16:30,715 INFO 19.3
2020-09-16 00:17:30,904 INFO 25.3
```

Logs generated with this utility can be plotted with the `PlotLog` utility.

