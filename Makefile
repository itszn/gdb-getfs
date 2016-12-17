getFS: getFS.c
	gcc -c -Wall -Werror -fpic getFS.c
	gcc -shared -o getFS.so getFS.o
