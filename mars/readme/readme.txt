0.python 2.7 is used
1.PLY-3.0 is used 
2.cppheaderparser(enclosed in the folder) is used
3.help.h is used to generate objects that are needed by the constructor of cut(class under test)
  these objects's type are not including int, char, char[], double and float, which can be generated automatedly by our tool.
4.if you are willing to run with g++, you should specify the additional lib:
	g++ help.h my_q.h test0gen.cpp -o 1 -lpthread
5.when you encounter problems such as double free, while running. you could use MALLOC_CHECK_=0 before you run the exe
	MALLOC_CHECH_=0 ./2 


