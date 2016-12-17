import gdbGetFs

gdbGetFs.setFSInjection(True)

gdb.execute("start")

print gdbGetFs.getFS(8)
