unsigned long getFS(unsigned long off) {
    unsigned long res;
    asm("mov %%fs:(%1),%0"
            : "=r" (res)
            : "r" (off));
    return res;
}

unsigned long getGS(unsigned long off) {
    unsigned long res;
    asm("mov %%gs:(%1),%0"
            : "=r" (res)
            : "r" (off));
    return res;
}
