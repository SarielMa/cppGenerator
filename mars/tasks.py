#!/usr/bin/python
import CppHeaderParser
import random
from  primitiveProvider import primitiveProvider as ppder
import types
from seqPrinter import seqPrinter as sp
from sfseqPrinter import sfseqPrinter as sfp
class atom(object):
    def __init__(self):
        pass
class methodatom(atom):
    def __init__(self,fname,cls,method):
        cppheader=CppHeaderParser.CppHeader(fname)
        myq=cppheader.classes[cls]
        meth=[m for m in myq["methods"]["public"] if m["name"]==method][0]
        methptype=[t["type"] for t in meth["parameters"]]
        self.name=method
        self.cls=cls
        self.nbParams=len(methptype)
        self.paramtypes=methptype
        self.returntype=meth["rtnType"]
        #self.declaringtype=0
        str1=','.join(self.paramtypes)
        self.signature=cls+"."+method+"("+str1+")"
        self.isstatic=meth["static"]
        self.isconstructor=False
        self.ismethod=True
        self.isfield=False

    def execute(self):
        pass

    def mprint(self):
        print("nb para",self.nbParams)
        print("params ",self.paramtypes)
        print("rtntype ",self.returntype)
        print("sig ",self.signature)
        print("isstatic? ",self.isstatic)
        print("isfield? ",self.isfield)

class constructoratom(atom):
    def __init__(self,fname,cls,method,mpara):
        cppheader=CppHeaderParser.CppHeader(fname)
        myq=cppheader.classes[cls]
        meth=[m for m in myq["methods"]["public"] if (m["name"]==method and [t["type"] for t in m["parameters"]]==mpara)][0]
        methptype=[t["type"] for t in meth["parameters"]]

        self.name=method
        self.cls=cls

        self.nbParams=len(methptype)
        self.paramtypes=methptype
        self.returntype=cls
        #self.declaringtype=0
        str1=','.join(self.paramtypes)
        self.signature=cls+"("+str1+")"
        self.isstatic=False
        self.isconstructor=True
        self.ismethod=False
        self.isfield=False
    def execute(self):
        pass
    def mprint(self):
        print("nb para",self.nbParams)
        print("params ",self.paramtypes)
        print("rtntype ",self.returntype)
        print("sig ",self.signature)
        print("isstatic? ",self.isstatic)
        print("isfield? ",self.isfield)

class fieldgetteratom(atom):
    def __init__(self,fname,cls,v):
        cppheader=CppHeaderParser.CppHeader(fname)
        myq=cppheader.classes[cls]
        #meth=[m for m in myq["properties"]["private"] if m["name"]==v][0]
        p=[m for m in myq["properties"]["private"] if m["name"]==v][0]

        self.name=v
        self.cls=cls
        self.nbParams=0
        #self.paramtypes=
        self.returntype=p["type"]
        #self.declaringtype=0
        #str1=','.join(self.paramtypes)
        self.signature=cls+"."+v
        self.isstatic=(p["static"]==1)
        self.isconstructor=False
        self.ismethod=False
        self.isfield=True
    def execute(self):
        pass
    def mprint(self):
        print("nb para",self.nbParams)
        #print("params ",self.paramtypes)
        print("rtntype ",self.returntype)
        print("sig ",self.signature)
        print("isstatic? ",self.isstatic)
        print("isfield? ",self.isfield)


class clsreader(object):
    def __init__(self,filename,classname):
        self.cls=classname
        self.fname=filename
        self.matoms=[]
        self.catoms=[]
        self.fatoms=[]
    def rdmethodatom(self):
        #cls get list methods
        cppheader=CppHeaderParser.CppHeader(self.fname)
        myq=cppheader.classes[self.cls]
        ml=[m["name"] for m in myq["methods"]["public"] if m["name"]!=self.cls]# method list
        #print(ml)
        for mn in ml:
            self.matoms.append(methodatom(self.fname,self.cls,mn))
        #print(atoms)    
        # sort the methods in atoms list, later sth could be done here to enhance the algorithm 
        def getKey(item):
            return item.name
        self.matoms.sort(key=getKey)
        #print([i.signature for i in atoms])
        return self.matoms

    def rdconstructoratom(self):
        #cls get list methods
        cppheader=CppHeaderParser.CppHeader(self.fname)
        myq=cppheader.classes[self.cls]
        ml=[(m["name"],[t["type"] for t in m["parameters"]]) for m in myq["methods"]["public"] if m["constructor"]==True]# constructors list
        #print(ml)
        for mn in ml:
            self.catoms.append(constructoratom(self.fname,self.cls,mn[0],mn[1]))
        #print(atoms)    
        # sort the methods in atoms list, later sth could be done here to enhance the algorithm 
        def getKey(item):
            return item.nbParams# sort by the number of params in the constructor
        self.catoms.sort(key=getKey)
        #print([i.signature for i in atoms])
        return self.catoms
 
    def readfieldatom(self):
         #cls get list methods
        cppheader=CppHeaderParser.CppHeader(self.fname)
        myq=cppheader.classes[self.cls]
        ml=[m["name"] for m in myq["properties"]["public"]]# public properties list
        #print(ml)
        for mn in ml:
            self.fatoms.append(fieldgetteratom(self.fname,self.cls,mn))
        #print(atoms)    
        # sort the methods in atoms list, later sth could be done here to enhance the algorithm 
        def getKey(item):
            return item.name
        self.fatoms.sort(key=getKey)
        #print([i.signature for i in atoms])
        return self.fatoms

class mtype(object):
    def __init__(self,fname1,cut,fname2,helpcls):#helpcls is a list
        self.cut=cut
        self.fn1=fname1
        self.hcls=helpcls
        self.fn2=fname2
        self.c2f={}
        self.c2f[cut]=fname1
        self.tp2atm={}
        for c in helpcls:
            self.c2f[c]=fname2
        allcls=[]
        allcls.extend(helpcls)
        allcls.append(cut)
        #print(allcls)
        #print(c2f)
        self.atoms=[]
        for clsn in allcls:
            con=self.constructors(self.c2f[clsn],clsn)
        #    print([rtn.returntype for rtn in con])
            for atm in con:
                if atm.returntype !="void":
                    if self.tp2atm.get(atm.returntype) == None:
                        self.tp2atm[atm.returntype]=[atm]
                    else:
                        self.tp2atm.get(atm.returntype).extend([atm])

            for atm in self.methods(self.c2f[clsn],clsn):
                if atm.returntype !="void":
                    if self.tp2atm.get(atm.returntype) == None:
                        self.tp2atm[atm.returntype]=[atm]
                    else:
                        self.tp2atm.get(atm.returntype).extend([atm])


            for atm in self.fieldgetter(self.c2f[clsn],clsn):
                if atm.returntype !="void":
                    if self.tp2atm.get(atm.returntype) == None:
                        self.tp2atm[atm.returntype]=[atm]
                    else:
                        self.tp2atm.get(atm.returntype).extend([atm])


            #print(self.tp2atm)

    def atmgivingtype(self,tp):
        self.atoms=self.tp2atm.get(tp)
        if self.atoms is None:
            return None
        else:
            return self.atoms[random.randint(0,len(self.atoms)-1)]
    def allatmgivingtype(self,tp):
        self.atoms=self.tp2atm.get(tp)
        if self.atoms is None:
            return []
        else:
            return self.atoms
    def constructors(self,fn,cls):
        #a=clsreader(fn,cls)
        return clsreader(fn,cls).rdconstructoratom()
    def methods(self,fn,cls):
        m=clsreader(fn,cls)
        return m.rdmethodatom()
    def fieldgetter(self,fn,cls):
        f=clsreader(fn,cls)
        return f.readfieldatom()
    def cutmethod(self):
        return self.methods(self.fn1,self.cut)
class mvariable(object):
    def __init__(self):
        pass
class obj(mvariable):
    def __init__(self):
        pass
class nullconstant(mvariable):
    def __init__(self):
        pass
class constant(mvariable):
    def __init__(self,value):
        self.v=value

class call(object):
    def __init__(self,atom,receiver,args,ret):
        self.atm=atom
        self.rec=receiver
        self.args=args
        self.ret=ret#variable
        if self.atm.nbParams != len(args):
            print("call init error in class call")
    def tos(self):
        s="call to "+str(self.atm.signature)+"  receiver="+str(self.rec)+"  args="+str(self.args)+"  return val="+str(self.ret)
        return s
#        print(s)
class fix(object):
    def __init__(self):
        pass
class prefix(fix):
    def __init__(self):
        self.fix='prefix'
        self.calls=[]
        self.t2v={}
        self.v2id={}
        self.nextid=0
        self.cutv=None
        self.v2o={}
    def equivalentto(self,other):
        if type(other)!=prefix:
            return False
        elif self.cutv== None or other.cutv==None:
            return False
        elif self.tos()==other.tos() and self.cutv==other.cutv:
            return True
        else:
            return False

    def fixcutv(self):
        last=self.calls[len(self.calls)-1]
        self.cutv=last.ret#the type of ret is obj's super class, but the cutv should be obj
    def vid(self,v):# null type is ignored now, future work
        if self.v2id.get(v)=='null':
            return 'null'
        if self.v2id.get(v)==None:
            newid="var"+str(self.nextid)
            self.nextid=self.nextid+1
            self.v2id[v]=newid
            return newid
        else:
            return self.v2id[v]
    def hasid(self,v):
        if self.v2id.get(v)!=False:
            return True
        else:
            return False
    def appendcall(self,atm,rec,args,ret):#the 6th para is not used
        cal=call(atm,rec,args,ret)
        #print(cal.tos())
        self.calls.append(cal)
        #print("calls len is ",len(self.calls))
        if atm.returntype=="void":
            return None
        tp=atm.returntype
        retv=ret
        #super type could be added in as well,future work
        if self.t2v.get(tp)==None:
            self.t2v[tp]=[retv]
        else:
            self.t2v[tp].extend([retv])

        return self.vid(retv)
    def copy(self):
        res=prefix()
        cutvarassigned=False
        for c in self.calls:
            if cutvarassigned == True:
                producecutv=False
            else:
                if c.ret.returntype!="void" and c.ret==self.cutv:
                    cutvarassigned=True
                    producecutv=True
                else:
                    producecutv=False
            res.appendcall(c.atm,c.rec,c.args,c.ret,producecutv)
        res.cutv=self.cutv
        return res
    def tos(self):
        return sp().cals2s(self)
class suffix(object):
    def __init__(self,pfix):
        self.pfix=pfix
        self.calls=[]
        self.t2v={}
        self.v2id={}
        self.nextid=0

    def equivalentto(self,other):
        if type(other)!=suffix:
            return False
        elif self.tos()==other.tos() and self.pfix.equivalentto(other.pfix):
            return True
        else:
            return False

    def copy(self):
        res=suffix(self.pfix)
        for call in self.calls:
            res.appendcall(call.atm,call.rec,call.args,call.ret)
        return res
    def appendcall(self,atm,rec,args,ret):#the 6th para is not used
        cal=call(atm,rec,args,ret)
        #print(cal.tos())
        self.calls.append(cal)
        #print("calls len is ",len(self.calls))
        if atm.returntype=="void":
            return None
        tp=atm.returntype
        retv=ret
        #super type could be added in as well,future work
        if self.t2v.get(tp)==None:
            self.t2v[tp]=[retv]
        else:
            self.t2v[tp].extend([retv])

        return self.vid(retv)
    def tos(self):
        return sfp().cals2s(self)
    def rectos(self):
        return self.pfix.vid(self.pfix.cutv)

    def vid(self,v):# null type is ignored now, future work
        if self.pfix.hasid(v):
            return self.pfix.vid(v)
        if self.v2id.get(v)=='null':
            return 'null'
        if self.v2id.get(v)==None:
            newid="var"+str(self.nextid)
            self.nextid=self.nextid+1
            self.v2id[v]=newid
            return newid
        else:
            return self.v2id[v]
   
class sfixgen(object):
    def __init__(self,pfix,maxfixlen,fn1,cut,fn2,hcls):
        self.cutm=mtype(fn1,cut,fn2,hcls).cutmethod()
        self.f1=fn1
        self.f2=fn2
        self.c=cut
        self.h=hcls
        self.pfix=pfix
        #print(self.cutm)
    def nextsfix(self,cals):
        fix=suffix(self.pfix)
        cc=0
        while cc<cals:
            ctask=callmtask(fix,self.cutm,self.f1,self.c,self.f2,self.h)
            s=ctask.cptseqc()
            if s==None:
                return None
            else:
                fix=s
            cc+=1
        return fix

class callmtask(object):
    def __init__(self,sfix,cutmethods,ffn1,ccut,ffn2,hhcls):
        self.sfix=sfix
        self.cutm=cutmethods
        self.fn1=ffn1
        self.cut=ccut
        self.fn2=ffn2
        self.hcls=hhcls
    def cptseqc(self):
        seq=self.sfix.copy()
        cm=self.cutm[random.randint(0,len(self.cutm)-1)]
        rec=seq.pfix.cutv
        args=[]
        for tp in cm.paramtypes:
            ptask=getptask(seq,tp,self.fn1,self.cut,self.fn2,self.hcls)
            s=ptask.cptseqc()
            if s==None:
                return None
            else:
                seq=s
                args.append(ptask.param)
                #print(tp+": "+str(ptask.param))
        retv=cm.returntype
        if retv==None:#ret may have something wrong
            retv= None
        else:
            retv= obj()
        ec=seq.copy()
        ec.appendcall(cm,rec,args,retv)
        return ec
class getptask(object):# be tested
    def __init__(self,pfix,tp,fn1,cut,fn2,cls):#this pfix is actually a seq, more than a just pfix
        self.mrc=50
        self.crc=0
        self.pfix=pfix
        self.tp=tp
        self.fn1=fn1
        self.fn2=fn2
        self.cut=cut
        self.cls=cls
        self.param=None
        self.maxtry=10
        
    def findv(self,tp,seq,nullallowed):
        na=nullallowed
        if self.crc>self.mrc:
            return None
        self.crc+=1

#        if ppder().isptype(tp)==True:
#            return ppder().getv(tp)

        if seq.t2v.keys().count(tp)>0:
            vars=seq.t2v[tp]
            sv=vars[random.randint(0,len(vars)-1)]
            print(tp+" already exixt in "+str(seq.t2v.keys())+str(sv))
            return sv
        else:#there is no such type in the seq
            if ppder().isptype(tp)==True:
                return ppder().getv(tp)
            else:
                atom=mtype(self.fn1,self.cut,self.fn2,self.cls).atmgivingtype(tp)
                #print(atom.name)
                if atom==None:
                    return None
                if atom.isstatic==True or atom.isconstructor==True:
                    rec=None
                else:
                    rec=self.findv(atom.cls,seq,False)
                    if rec==None:
                        return None
                    else:
                        if rec==seq.cutv and atom.cls!=cut:
                            return None
                args=[]
                for t in atom.paramtypes:
                    arg=self.findv(t,seq,False)
                    if arg==None:
                        return None
                    else:
                        args.append(arg)
                retval=obj()
                seq.appendcall(atom,rec,args,retval)
                #print(seq.calls[0].tos())
                return retval

    def cptseqc(self):
        seq=self.pfix.copy()
        self.param=self.findv(self.tp,seq,True)
        if self.param!=None:
            return seq
        else:
            return None
            
class instCutTask(object):
    def __init__(self,filename1,ccut,filename2,hclss):
        self.maxtries=10
        self.cut=ccut
        self.fn1=filename1
        self.cut=ccut
        self.fn2=filename2
        self.hcls=hclss
    def cptseqc(self):
        tpprovider=mtype(self.fn1,self.cut,self.fn2,self.hcls)
        self.constructoratoms=[]
        constructors=tpprovider.constructors(self.fn1,self.cut)
        self.constructoratoms.extend(constructors)
        #print(self.constructoratoms)
        #print(constructors)
        prestaticconstructors=tpprovider.methods(self.fn1,self.cut)
        staticconstructors=[]
        for m in prestaticconstructors:
            if m.returntype==self.cut and m.isstatic==True:
                staticconstrucors.append(m)
        #print(staticconstructors)
        self.constructoratoms.extend(staticconstructors)

        othercreator=[]
        other=tpprovider.allatmgivingtype(self.cut)
        for i in other:
            if i.ismethod==True and i.isstatic==True:
                othercreator.append(i)
        #print(other)        
        self.constructoratoms.extend(othercreator)

        if len(self.constructoratoms)==0:
            print("no contrustors could be used to create a instance of cut")
            return None        
#        for a in self.constructoratoms:
#            print(a.name)
        constructor=self.constructoratoms[random.randint(0,len(self.constructoratoms)-1)]
        #constructor=self.constructoratoms[2]
        #print(constructor.paramtypes)
        res=prefix()
        args=[]
        for tp in constructor.paramtypes:
            ptask=getptask(res,tp,self.fn1,self.cut,self.fn2,self.hcls)
            exseq= ptask.cptseqc()
            if exseq==None:
                return None
            else:
                res=exseq
                args.append(ptask.param)
        res.appendcall(constructor,None,args,obj())
        return res
#    def run():
#        pass
if __name__=="__main__":
    #a=constructoratom("my_q.h","Queue","Queue")
    #a.mprint()
    #a=clsreader("my_q.h","Queue").rdconstructoratom()
    #a=mtype("my_q.h","Queue","help.h",["as","ass"])
    #a=instCutTask("my_q.h","Queue","help.h",["as","ass"])
    #a=call(1,2,3,4).tos()
    #print(getptask('char[]',1).findv('char[]','1','2'))
    a=instCutTask('my_q.h','Queue','help.h',['as','ass'])
    #print(a.param)
    seq=a.cptseqc()
    #print()
    for c in seq.calls:
        print(c.tos())
    print(seq.tos())
