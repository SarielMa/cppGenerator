#!usr/bin/python
#from tasks import variable 
import random
class primitiveProvider(object):
    def __init__(self):
        self.intl=[-100,-10,-5,-2,-1,0,1,2,5,10,100]
        self.charl='asdfghjklqwertyuiopzxcvbnm'
        self.floatl=[-0.5,0.0,0.1,0.5]
        self.doublel=[-0.5,0.0,0.1,0.5]
        self.booll=['true','false']
    def isptype(self,tp):
        if tp.find("int")>=0 or tp.find("float")>=0 or tp.find("double")>=0 or tp=="char" or tp=="bool" or tp=="string":
            return True
        else:
            return False
    def getv(self,tp):
        if tp.find("int")>=0:
            return random.randint(-100,100)
        elif tp.find("float")>=0:
            return self.floatl[random.randint(0,len(self.floatl)-1)]+'f'
        elif tp.find("double")>=0:
            return self.doublel[random.randint(0,len(self.floatl)-1)]
        elif tp=="char":
            return "'"+random.choice(self.charl)+"'"
        elif tp=="bool":
            return self.booll[random.randint(0,len(self.booll)-1)]
        elif tp=="string":
            s='xas'
            while random.randint(0,1)==1:
                s+=random.choice(self.charl)
            return '"'+s+'"'
        else:
            return None
if __name__=="__main__":
    print(primitiveProvider().isptype("string"))
    print(primitiveProvider().isptype("char"))
    print(primitiveProvider().isptype("bool"))
    print(primitiveProvider().getv("string"))
    print(primitiveProvider().getv("char"))
    print(primitiveProvider().getv("bool"))

