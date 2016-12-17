import gdbGetFS

gdbGetFS.setFSInjection(True)

gdb.execute("start")

print gdbGetFS.getFS(8)
