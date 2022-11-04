import paramiko
import pandas as pd
import numpy as np
from os import environ as env


class getFiles:
    def __init__(self,path):
        self.path = path
        """ Setting vars : path to save file"""
        
    def openFileExcel(self):
        sheet = pd.read_excel("output_export/info.xlsx",sheet_name="Hoja2")
        sheetCol = sheet[["ips"]]
        sheetList = sheetCol.values.tolist()
        sheetArr = np.array(sheetList) 
        sheetVal = sheetArr.reshape(-1).tolist()
        return sheetVal

    def openFileTxt(self):
            filePath = "{}.txt"
            fileOpen = open(format(self.path),"r")
            fileRead = fileOpen.read()
            fileData= fileRead.split(",")
            return fileData

class getConnect:
    def __init__(self,command,password):
        self.command = command
        self.password = password
        """Setting vars : command to execute and password"""

    def connectToIp(self,ip):
        for i in range(len(ip)): 
            try:
                createFile = open(f"{ip[i]}.txt","w+")
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip[i], username='admin', password=str(self.password), timeout=3)
            except TimeoutError:
                print(f"Time out : {ip[i]}")
                continue
            stdin,stdout,strerror = client.exec_command(self.command)
            for line in stdout:
                dataBare = stdout.read().decode("ascii").replace("\n","")
                createFile.write(dataBare)
                client.close()
            
def main():
    print(f"Welcome to ssh-script {env.get('USERNAME')}")
    password = input("[Password] ")
    path = str(input("[Directory] "))
    command = input(f"[$] ")
    getConnect(command,password).connectToIp(getFiles(path).openFileTxt())

main()