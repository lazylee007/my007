A tool to scan Struts2-045. 

It has two scan models: 1. Scan a target file. 2. Scan a single target and send commands in interactive mode.

Here is the usage:

    Usage: struts2.py [options]

    Options:
      -h, --help    show this help message and exit.
      -f FILENAME   the targets file to scan.
      -u URL        the target url to scan.
      -t THREADNUM  set the number of threads.(default is 10)

You can use `-f` option to select the file with the targets you want to scan. Using `-t` option to set the thread number.

![](http://7xp22c.com1.z0.glb.clouddn.com/2017-03-08_115211.png)

You can use `-u` option to scan a single target and send commands in interactive mode.

![](http://7xp22c.com1.z0.glb.clouddn.com/2017-03-08_120346.png)