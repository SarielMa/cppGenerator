#!/usr/bin/python
import CppHeaderParser

cppheader=CppHeaderParser.CppHeader("my_q.h")
#print("cppheader view of %s"%cppheader)
h=CppHeaderParser.CppHeader("help.h")
h1=h.classes["as"]
myq=cppheader.classes["Queue"]
#print("myq is %s"%myq)
mn=[n for n in h1["methods"]["public"] if n["name"]=="q"][0]
print(mn["rtnType"])
print(mn["static"])

#print("the public methods in the class as are %s"%(mn))
#print("the number of private methods in the class Queue is %d"%(len(myq["methods"]["private"])))
print("the public method 0 in the class Queue is %s"%(myq["methods"]["public"][0]["name"]))
print(myq["methods"]["public"][0]["static"])
#print("the public method 1 in the class Queue is %s"%(myq["methods"]["public"][1]["name"]))
#print("the public method 2 in the class Queue is %s"%(myq["methods"]["public"][2]["name"]))
#print("the public method 3 in the class Queue is %s"%(myq["methods"]["public"][3]["name"]))
#meth=[m for m in myq["methods"]["public"] if m["name"]=="mmethod"][0]
#p=[m for m in myq["properties"]["private"] if m["name"]=="_lock"][0]
#print("meth=%s"%meth)
#print(p)
#ml=[m["name"] for m in myq["methods"]["public"]]
#ml=[m["name"] for m in myq["methods"]["public"] if m["constructor"]==True]
#print("methods list is ",ml)
#print("constructors are ",ml)
#methptype=[t["type"] for t in meth["parameters"]]
#print("the public method  in the class Queue has parameters types that are %s"%(methptype))
#print("the public method  in the class Queue has parameters %d"%(len(methptype)))
#print("the public method  in the class Queue has return type %s"%(meth["rtnType"]))
#print("the public method  in the class Queue static is %s"%(meth["static"]))
a={}
a["1"]="a"
a["1"]="b"
print(a)

