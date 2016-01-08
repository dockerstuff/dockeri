import os
import platform
import subprocess
from subprocess import PIPE,STDOUT

_DISPLAY = os.environ['DISPLAY']

try:
    from subprocess import DEVNULL # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')

def vmip4darwin():
    ipaddr = None
    for i in range(9):
        netint = "vboxnet{}".format(i)
        cmdline = ["ifconfig",netint]
        if subprocess.call(cmdline,stdout=DEVNULL,stderr=STDOUT)!=0:
            continue
        ifout = subprocess.check_output(cmdline)
        cmdline = ["awk","{if(/inet/){print substr($2,1)}}"]
        proc = subprocess.Popen(cmdline,stdout=PIPE,stderr=PIPE,stdin=PIPE)
        out,err = proc.communicate(ifout)
        out = out.strip()
        if out is not "":
            ipaddr = out
    return ipaddr

def x114darwin():
    cmdline = 'socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"{0}\"'.format(_DISPLAY)
    proc = subprocess.Popen(cmdline.split(),stdout=PIPE,stderr=PIPE,stdin=PIPE)
    #procid = proc.pid
    vmip = vmip4darwin()
    return '{0}:0'.format(vmip)

def x114linux():
    return 'unix{}'.format(_DISPLAY)

def get_DISPLAY():
    if platform.system().upper() == 'DARWIN':
        DISPLAY = x114darwin()
    elif platform.system().upper() == 'LINUX':
        DISPLAY = x114linux()
    else:
        print("System not supported.")
        return None
    print 'DISPLAY={}'.format(DISPLAY)
    return DISPLAY
