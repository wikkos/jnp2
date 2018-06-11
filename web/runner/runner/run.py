import time
import os
import json

sourceFileName = "file"
inputFileName = "input"

# not proud of it, but it works
def checkFilesArePresent():
    filesArePresent = False
    while not filesArePresent:
        try:
            file = open(sourceFileName + ".c", "r")
            file.close()
            file = open(inputFileName, "r")
            file.close()
            filesArePresent = True
        except:
            print("files not present")
            time.sleep(3)

def addToDict(dict, fileName):
    file = open(fileName, "r")
    dict[fileName] = file.read()
    file.close()

def compile(dict):
    #os.system("gcc -std=c11 " + sourceFileName + ".c -o " + sourceFileName + " >compiler-out && echo $? >compiler-errcode")
    os.system("echo ajajaj >compiler-out")
    os.system("echo 0 >compiler-errcode")
    addToDict(dict, "compiler-out")
    addToDict(dict, "compiler-errcode")

def run(dict):
    if dict["compiler-errcode"] == "0\n":
        # TODO some timeout maybe
        #os.system("./" + sourceFileName + " <" + inputFileName + " >out >>err && echo $? >errcode")
        os.system("echo arrgh >out")
        os.system("echo asd >err")
        os.system("echo 111 >errcode")
        addToDict(dict, "out")
        addToDict(dict, "err")
        addToDict(dict, "errcode")
    else:
        # TODO is it necessary?
        dict["out"] = ""
        dict["err"] = ""
        dict["errcode"] = ""

checkFilesArePresent()
data = {}
compile(data)
run(data)
print(json.dumps(data))
