#GDB getFS

This script allows you to inspect values in fs: by LD_PRELOADing a shared library that interacts with fs for you.

To use, clone this repo somewhere, and then do
```gdb -x /path/to/gdbGetFs.py``` or ```source /path/to/gdbGetFs.py``` once you start gdb (or in your ~/.gdbinit).

##Example
Printing out a stack cookie value from fs:0x28
```
$ gdb ../test2 -x gdbGetFS.py
Reading symbols from ../test2...(no debugging symbols found)...done.
gdb-peda$ fsinject on
Enabled FS injection
gdb-peda$ start
[----------------------------------registers-----------------------------------]
...
[-------------------------------------code-------------------------------------]
   0x400598 <frame_dummy+40>:   jmp    0x400510 <register_tm_clones>
   0x40059d <main>:     push   rbp
   0x40059e <main+1>:   mov    rbp,rsp
=> 0x4005a1 <main+4>:   sub    rsp,0x70
   0x4005a5 <main+8>:   mov    rax,QWORD PTR fs:0x28
   0x4005ae <main+17>:  mov    QWORD PTR [rbp-0x8],rax
   0x4005b2 <main+21>:  xor    eax,eax
   0x4005b4 <main+23>:  lea    rax,[rbp-0x70]
[------------------------------------stack-------------------------------------]
...
[------------------------------------------------------------------------------]
Legend: code, data, rodata, value

Temporary breakpoint 1, 0x00000000004005a1 in main ()
gdb-peda$ pfs 0x28
$2 = 0x4fc58c2b020d5200
gdb-peda$
```

##Commands
####fsinject
Enables or disables the LD_PRELOAD.

```fsinject [on|off]```

If you see an error like this when using a 32 bit binary,

`ERROR: ld.so: object '......getFS32.so' from LD_PRELOAD cannot be preloaded (wrong ELF class: ELFCLASS32): ignored.`

Just ignore it, since that is your 64 bit shell complaining before execing the real binary. The binary will still have the preload.


####pfs
Prints an offset of fs.

```pfs[/xd] offset_expr```

##API
If you wish to use this in some other gdb script, there are two functions you can import to use.
####gdbGetFS.setFSInjection(boolean)
Enables or disables the LD_PRELOAD. Must be done before the program is started.

####gdbGetFS.getFS(offset, doraise=False)
Returns the value at fs:offset. If there is an error or exception returns None, unless doraise is true, in which case it raises the exception. 


