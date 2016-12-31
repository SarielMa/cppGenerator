#include <pthread.h>
#include <iostream>
#include <unistd.h>
#include <assert.h>
using namespace std;
#include <list> // you could use std::list or your implementation 
#include "help.h"

//namespace concurrent { 
//template <typename 
class Queue { 
public: 
   Queue( ) { 
       pthread_mutex_init(&_lock, NULL);
	length=0; 
    }
    Queue(int len,double a){pthread_mutex_init(&_lock, NULL);length=0;}
    Queue(string len){pthread_mutex_init(&_lock, NULL);length=0;}
   Queue(as1 a){pthread_mutex_init(&_lock, NULL);length=0;}
    
    ~Queue( ) { 
       pthread_mutex_destroy(&_lock);
    } 
    void push(const int& data);

    int pop( ); 
    //int getlength(){return length;}
    //void method(int a,char c,int f){}
    //static Queue a();
private: 
    list<int> _list; 
    pthread_mutex_t _lock;
    int length;
};



void Queue::push(const int& value ) { 
       //pthread_mutex_lock(&_lock);
       _list.push_back(value);
	//cout<<"push"<<value<<endl;
        length++;
       //pthread_mutex_unlock(&_lock);
	//assert(length==_list.size());
}

int Queue::pop( ) { 

       if(length==0){cout<<"nothing to remove"<<endl;return -999;}
       pthread_mutex_lock(&_lock); 
       int _temp = _list.front( );
       _list.pop_front( );
	//cout<<"pop"<< _temp;
        sleep(0.1);
	//cout<<"(length is "<<--length<<")"<<endl;
       pthread_mutex_unlock(&_lock);
	//assert(length==_list.size());
       return _temp;
}


