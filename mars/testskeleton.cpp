#include<iostream>
#include<pthread.h>
#include"${filename}"
#include"${helpfile}"
using namespace std;
${PREFIX}
void *thrd1(void* arg)
{
    //${classname} * ${rec}=(${classname}*)arg;
${SUFFIX1}
    pthread_exit((void*)1);
}
void *thrd2(void* arg)
{
    //${classname} * ${rec}=(${classname}*)arg;
${SUFFIX2}
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
