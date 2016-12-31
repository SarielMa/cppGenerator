#include<iostream>
#include<pthread.h>
#include"/home/malh/experiment/mm/mars/my_q.h"
#include"/home/malh/experiment/mm/mars/help.h"
using namespace std;
Queue var0 = Queue(-52,-0.5);

void *thrd1(void* arg)
{
    //Queue * var0=(Queue*)arg;
    int var1 = var0.pop();
    var0.push(78);
    int var2 = var0.pop();

    pthread_exit((void*)1);
}
void *thrd2(void* arg)
{
    //Queue * var0=(Queue*)arg;
    var0.push(-13);
    var0.push(81);

    pthread_exit((void*)2);
}
int main()
{
   int err=0;
   pthread_t tid1,tid2;
   void* res;
   pthread_create(&tid1,NULL,thrd1,NULL); 
   pthread_create(&tid2,NULL,thrd2,NULL);
   pthread_join(tid1,&res); 
   pthread_join(tid2,&res); 
   return 0;
}
