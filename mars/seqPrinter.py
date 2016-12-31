#!/usr/bin/python
from primitiveProvider import primitiveProvider as ppder
class seqPrinter(object):
    def __init__(self):
        pass
    def cals2s(self,seq):
        self.seq=seq
        self.p=''
        for c in self.seq.calls:
            self.p+=self.cal2s(c)
            self.p+='\n'
        return self.p
    def cal2s(self,call):
        from tasks import mvariable
        cs=''
        if call.ret!=None:
            cs += call.atm.returntype+' '+self.seq.vid(call.ret)+' = '
        if call.atm.isconstructor==True:
            cs += call.atm.cls
        elif call.atm.isstatic==True:
            cs += call.atm.cls+'.'+call.atm.name
        else:
            cs += self.seq.vid(call.rec)+'.'+call.atm.name
        if call.atm.isfield==False:
            cs +='('
            cargs=[]
            
            for p in range(len(call.args)):
                arg=call.args[p]
                ags=''
                if arg=='null':
                    ags+='null'
                if isinstance(arg,mvariable):
                    ags+=self.seq.vid(arg)
                else:
                    ags+=str(arg)
                #ts=call.atm.paramtypes[p]
                cargs.append(ags)
            cs+=','.join(cargs)
            cs+=')'
        
        cs+=';'
        return cs
            
    def con2s(self,c):
        pass
    
    

