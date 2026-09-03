from pathlib import Path
import os

def createfile():
    try:
        name = input("Give your file name -: ")
        path = Path(name)
        if not path.exists():
            with open(path,"w") as fs:
                data = input("What you want to write -: ")
                fs.write(data)
            print("File created successfully")
        else:
            print("Error File name already exists")
    except Exception as err:
        print(f"An error occured as {err}")
    
def readfile():
    pass

def updatefile():
    pass

def deletefile():
    pass


print("press 1 for creating a file")
print("press 2 for reading a file")
print("press 3 for updating a file")
print("press 4 for deleting a file")

a = int(input("\ntell your response :- "))


if a == 1:
    createfile()
if a == 2:
    readfile()
if a == 3:
    updatefile()
if a == 4:
    deletefile()