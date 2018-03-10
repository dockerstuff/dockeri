import os
import platform
import subprocess
from subprocess import PIPE, STDOUT

_DISPLAY = os.environ['DISPLAY']

try:
    from subprocess import DEVNULL  # py3k
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


def hostip4darwin():
    ipaddr = None
    cmdline = 'ifconfig en0'.split()
    if subprocess.call(cmdline, stdout=DEVNULL, stderr=STDOUT) != 0:
        return None
    ifout = subprocess.check_output(cmdline)
    cmdline = ['awk', '$1=="inet" {print $2}']
    proc = subprocess.Popen(cmdline, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = proc.communicate(ifout)
    out = out.strip()
    if out is not "":
        ipaddr = out
    ipaddr = ipaddr.decode('utf-8')
    cmdline = ['xhost', '+{}'.format(ipaddr)]
    #proc = subprocess.call(cmdline, stdout=DEVNULL, stderr=STDOUT)
    _= os.system(' '.join(cmdline))
    return ipaddr


def x114darwin():
    # cmdline = 'socat TCP-LISTEN:6000,reuseaddr,fork UNIX-CLIENT:\"{0}\"'.format(_DISPLAY)
    # proc = subprocess.Popen(cmdline.split(),stdout=PIPE,stderr=PIPE,stdin=PIPE)
    #procid = proc.pid
    vmip = hostip4darwin()
    return '{!s}:0'.format(vmip)


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
    # print 'DISPLAY={}'.format(DISPLAY)
    return DISPLAY
