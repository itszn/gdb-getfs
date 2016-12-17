import os
import gdb

isFSInjectEnabled = False
PYFILE = os.path.abspath(os.path.expanduser(__file__))


def to_int(val):
    """
    Convert a string to int number
    """
    try:
        return int(str(val), 0)
    except:
        return None

def getarch():
    """
    Get architecture of debugged program
    Returns:
        - tuple of architecture info (arch (String), bits (Int))
    """
    arch = "unknown"
    bits = 32
    out = gdb.execute('maintenance info sections ?',to_string=True).splitlines()
    for line in out:
        if "file type" in line:
            arch = line.split()[-1][:-1]
            break
    if "64" in arch:
        bits = 64
    return (arch, bits)

def getreg(register):
    """
    Get value of a specific register
    Args:
        - register: register name (String)
    Returns:
        - register value (Int)
    """
    r = register.lower()
    regs = gdb.execute("info registers %s" % r, to_string=True)
    if regs:
        regs = regs.splitlines()
        if len(regs) > 1:
            return None
        else:
            result = gdb.to_int(regs[0].split()[1])
            return result

    return None

def setFSInjection(b):
    global isFSInjectEnabled
    isFSInjectEnabled = b

    sopath = os.path.join(os.path.dirname(PYFILE),'getFS.so' if getarch()[1]==64 else 'getFS32.so')
    e = gdb.execute('show environ LD_PRELOAD',to_string=True).strip()
    if b:
        if not sopath in e:
            if not e.startswith('LD_PRELOAD = ') or e[11:]=='':
                e = sopath
            else:
                e = e[13:]+' '+sopath
            gdb.execute('set environ LD_PRELOAD=%s'%e,to_string=True)
    else:
        if sopath in e:
            e = e[13:]
            e=e.replace(' '+sopath,'')
            e=e.replace(sopath,'')
            gdb.execute('set environ LD_PRELOAD=%s'%e,to_string=True)

class CommandEnableFSInject(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, 'fsinject', gdb.COMMAND_RUNNING)

    def dont_repeat(self):
        return True

    def invoke(self, arg, from_tty):
        global isFSInjectEnabled
        args = gdb.string_to_argv(arg)
        if len(args)==0:
            print "FS Injection is %s"%('enabled' if isFSInjectEnabled else 'disabled')
        elif arg=='on':
            setFSInjection(True)

            print "Enabled FS injection"
        elif arg=='off':
            setFSInjection(False)
            print "Disabled FS injection"

    def complete(self, text, word):
        res = []
        if 'on'.startswith(text):
            res.append('on')
        if 'off'.startswith(text):
            res.append('off')
        return res


def getFS(off, doraise=False):
    res = None
    oldUnwind = gdb.execute('show unwindonsignal',to_string=True).split()[-1][:-1]
    if oldUnwind != 'on':
        gdb.execute('set unwindonsignal on',to_string=True)

    try:
        res = gdb.execute('call ((unsigned long (*)(unsigned long))getFS)(%u)'%off,to_string=True)
        v = to_int(res.strip().split()[-1])
        res = v

    except gdb.error as e:
        if doraise:
            raise e
        res = None
    finally:
        if oldUnwind != 'on':
            gdb.execute('set unwindonsignal off',to_string=True)
    return res


class CommandPrintFs(gdb.Command):
    def __init__(self):
        gdb.Command.__init__(self, 'pfs',gdb.COMMAND_DATA, gdb.COMPLETE_EXPRESSION)

    def invoke(self, arg, from_tty):
        args = gdb.string_to_argv(arg)
        pref = ''

        if not isFSInjectEnabled:
            print 'FS Injection is disabled. Use `fsinject on` before starting the program to enable'
            return

        if len(args)>0 and args[0][0]=='/':
            pref = args[0]
            arg = arg[len(pref):]
        if len(args)>0:
            v = gdb.parse_and_eval(arg)
            try:
                v = getFS(to_int(v), doraise=True)
                gdb.execute('p%s %u'%(pref,v))

            except gdb.error as e:
                if str(e).startswith('The program being debugged was signaled'):
                    print "%s is out of range for fs"%v
                else:
                    print "Could not read fs, either the program is not running, or injection has not happened yet (restart the program)"





if __name__ == '__main__':
    CommandEnableFSInject()
    CommandPrintFs()



