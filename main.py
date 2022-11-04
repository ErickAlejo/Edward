import paramiko
import pandas as pd
import numpy as np


class files:
    def __init__(self,path):
        self.path = path
        """ File Class give somes variables, route of file and route of output (path,output)  """
        
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

class getAccess:
    def __init__(self,command):
        self.command = command
        """ getAcc get data of files and a command to execute a multiple IPs """

    def connectToIp(self,ip):
        for i in range(len(ip)): 
            try:
                saveData = open(f"{ip[i]}.txt","w+")
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip[i], username='admin', password='S0m0s_2021', timeout=3)
            except TimeoutError:
                print(f"Time out ip : {ip[i]}")
                continue
            stdin,stdout,strerror = client.exec_command(self.command)
            for line in stdout:
                dataBare = stdout.read().decode("ascii").replace("\n","")
                saveData.write(dataBare)
                client.close()
            
def main():
    path = str(input("Path : "))
    command = input("$ ")
    getAccess(command).connectToIp(files(path).openFileTxt())

main()