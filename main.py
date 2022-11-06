from gettext import find
import os
import time
import paramiko
import pandas as pd
import numpy as np



class getFiles:
    def __init__(self,path:str):
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
        fileOpen = open(format(self.path),"r")
        fileRead = fileOpen.read()
        fileData= fileRead.split(",")
        return fileData #return a list of IPs

class getConnect:
    def __init__(self,command,password):
        self.command = command
        self.password = password
        """Setting vars : command to execute and password"""

    def connectToIp(self,ip:list):
        for i in range(len(ip)): 
            try:
                export = "export"
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
                client.connect(ip[i], username='admin', password=str(self.password), timeout=3)
            except TimeoutError:
                print(f"[Timeout : {ip[i]}]")
                continue
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
    print(f"Welcome to ssh-script {os.environ.get('USERNAME')} \nNo existe gran Genio, sin un toque de demencia -Seneca")
    print("")
    password = input("[Password] > ")
    path = str(input("[Directory] > "))
    print("[Set duration=seconds if your command use monitor]")
    time.sleep(2)
    command = input("[$] > ")
    getConnect(command,password).connectToIp(getFiles(path).openFileTxt())


run()