import os
import time
import paramiko
import pandas as pd
from numpy import array,reshape

class files:

    def __init__(self,path:str):
        self.path = path
        """ path:str is the route of all IPs"""
    def openFileExcel(self):
        sheet = pd.read_excel("output_export/info.xlsx",sheet_name="Hoja2")
        sheetCol = sheet[["ips"]]
        sheetList = sheetCol.values.tolist()
        sheetArr = np.array(sheetList) 
        sheetVal = sheetArr.reshape(-1).tolist()
        return sheetVal
    def openFileTxt(self):
        fileOpen = open(format(self.path),"r")
        fileRead = fileOpen.read()
        fileData= fileRead.split(",")
        return fileData #return a list of IPs

class setParamsSsh:

    def __init__(self,command:str,password:str):
        self.command = command
        self.password = password
        """command:str is the command to execute, password:str is password to each host"""
    def connectIP(self,ip:list):
        for i in range(len(ip)): 
            try:
                export = "data"
                exist_file = os.path.exists(export)
                if exist_file :
                    filePath = export + "/{}.txt"
                    createFile = open(filePath.format(ip[i]),"w+")
                else :
                    os.mkdir(export)
                    filePath = export + "/{}.txt"
                    createFile = open(filePath.format(ip[i]),"w+") #create each file of hosts
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip[i], username='admin', password=str(self.password), timeout=2)
            except TimeoutError:
                print(f"[Timeout : {ip[i]}]")
                break
            if self.command.find("monitor") & self.command.find("duration"):
                stdin,stdout,strerror = client.exec_command(self.command)
            elif self.command.find("duration"):
                stdin,stdout,strerror = client.exec_command(self.command)
            else:
                stdin,stdout,strerror = client.exec_command(self.command)
            for line in stdout:
                dataBare = stdout.read().decode("ascii").replace("\n","")
                createFile.write(dataBare)
                createFile.close()
                client.close()

def run():
    print(f"Welcome to ssh-script {os.environ.get('USERNAME')} \nHace falta una vida para aprender a vivir -Seneca\n")
    print("Please set duration=seconds when use monitor !")
    path = str(input("[Directory] > "))
    password = input("[Password] > ")
    command = input("[$] > ")
    setParamsSsh(command,password).connectIP(files(path).openFileTxt())
run()