getFS: getFS.c
	gcc -c -Wall -Werror -fpic getFS.c
	gcc -shared -o getFS.so getFS.o
	gcc -c -Wall -Werror -fpic getFS.c -m32
	gcc -shared -o getFS32.so getFS.o -m32
