#!/usr/bin/python
import sys
import os
from cppgen import Cppgen as cgen
from tasks import instCutTask
import random
from tasks import sfixgen
class Tester(object):
    def __init__(self,filename1,ccut,filename2,helpclass):
        self.fn1=filename1
        self.cut=ccut
        self.fn2=filename2
        self.hcls=helpclass
        #print("Welcome!")
        #print("para1: cut %s"%self.cut)
        #print("para2: assistant class %s"%self.hcls)
        #print("run....")
        self.ccps = 4 #the max number of calls in per seq(int)
        self.maxsfixes=20
        self.maxpfixes=self.maxsfixes/10 # the number of pfix  
        self.maxsfixlen=10

        self.prefixes=[]
        self.p2sgen={}
        self.p2s={}
        self.counter=0
    def singlerun(self):
	prefix=self.getPrefix()	
	sfixgen=self.p2sgen.get(prefix)
	l1=random.choice(range(1,self.ccps))
	l2=random.choice(range(1,self.ccps))
	sfix1=sfixgen.nextsfix(l1)
	sfix2=sfixgen.nextsfix(l2)
	singlegen=cgen(sys.argv[2],sys.argv[1])
	singlegen.gen(self.fn1,self.cut,self.fn2,prefix.tos(),sfix1.tos(),sfix2.tos(),sfix2.rectos())
	self.mybuild()
    def run(self):
        prefix = self.getPrefix()
        sfixgen=self.p2sgen.get(prefix)
        sfixes=self.p2s.get(prefix)

        nextsfix=sfixgen.nextsfix(self.ccps)
        if nextsfix!=None:
            if len([p for p in sfixes if nextsfix.equivalentto(p)])==0:
                sfixes.append(nextsfix)
                for s in sfixes:
                    cgen(self.counter,sys.argv[1]).gen(self.fn1,self.cut,self.fn2,prefix.tos(),nextsfix.tos(),s.tos(),s.rectos())
		    self.counter+=1
    def rrun(self):
        for i in range(1,self.maxsfixes):
            self.run()

        print("generating process end")
    def getPrefix(self):
        if len(self.prefixes)<self.maxpfixes:
            itask=instCutTask(self.fn1,self.cut,self.fn2,self.hcls)
            npfix=itask.cptseqc()
            if npfix==None:
                if len(self.prefixes)==0:
                    return None
                else:
                    return self.prefixes[random.randint(0,len(self.prefixes)-1)]
            else:
                npfix.fixcutv()
                if len([p for p in self.prefixes if npfix.equivalentto(p)])>0:
                    return self.prefixes[random.randint(0,len(self.prefixes)-1)]
                else:
                    self.prefixes.append(npfix)
                    self.p2sgen[npfix]=sfixgen(npfix,self.maxsfixlen,self.fn1,self.cut,self.fn2,self.hcls)
                    self.p2s[npfix]=[]
                    return npfix
        else:
            return self.prefixes[random.randint(0,len(self.prefixes)-1)]

    def appendstatechange(self,pfix):
        pass
    def mybuild(self):
	os.system('pwd')
	ad=os.getcwd()
	os.chdir(ad+'/tests')
	ad1=os.getcwd()
	files=os.listdir(ad1)
	#print(files)
	nf=[]
	for f in files:
	    if f.find('.cpp')>=0:
		nf.append(f)
	nf.sort(key=lambda x: int(x[4:-7]))
	if sys.argv[1]=='0':
	    os.chdir('../myrun')
	    os.system('rm -rf *')
	    os.chdir(ad1)
	for fn in nf:
	    if fn.find('.cpp')>=0:
		cpp=fn
		#gpp='g++ '+self.fn1+' '+self.fn2+' '+cpp+' -o ../myrun/'+cpp[4:-7]+' -pthread'
		gpp='g++ '+cpp+' -o ../myrun/'+cpp[4:-7]+' -pthread'
		os.system(gpp)
		print(gpp)
		#print (fn)
		

'''
    def testp(self):
        print("class Tester\n")
        print("class Tester2\n")
'''
if __name__ == "__main__":
    if not os.path.dirname(sys.argv[0])=='':
	    os.chdir(os.path.dirname(sys.argv[0]))
    #print(sys.argv[0])
    _cut='/home/malh/experiment/mm/mars/my_q.h'
    _ac='/home/malh/experiment/mm/mars/help.h'
    a=Tester(_cut,'Queue',_ac,['as1','ass1'])
    if sys.argv[1]=='0':
	a.singlerun()
    elif sys.argv[1]=='1':
	a.rrun()
    elif sys.argv[1]=='2':
	a.mybuild()
    else:
	print('parameters:')
	print('1: gen tests in test/')
	print('2: build tests in myrun/')
   # a.run()

