#ifndef H_HELP
#define H_HELP
#include <pthread.h>
#include <iostream>
#include <unistd.h>

using namespace std;
#include <list> // you could use std::list or your implementation 
class ass1 { 
public: 
    ass1(){}
    int rsint(){int i=1;return i;}
   // char* rschar(){char c[]="chara";return c;}
private: 
    
    int i;
    char c;
};

class as1 { 
public: 
    as1(ass1 x,int a){}
    int rint(){int i=1;return i;}
    //char* rchar(){char c[]="chara";return c;}
    //static Queue q(int i){a=Queue(i); return a;}
private: 
    
    int i;
    char c;
};


#endif
