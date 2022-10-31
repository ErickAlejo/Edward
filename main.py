from os import remove, strerror
from sys import stdin, stdout
import paramiko
import pandas as pd
import numpy as np
import time 


class files:
    def __init__(self,path,output):
        """ File Class give somes variables, route of file and route of output (path,output)  """
        
    def openFileExcel():
        sheet = pd.read_excel("output_export/info.xlsx",sheet_name="Hoja2")
        sheetCol = sheet[["ips"]]
        sheetList = sheetCol.values.tolist()
        sheetArr = np.array(sheetList) 
        sheetVal = sheetArr.reshape(-1).tolist()
        return sheetVal

    def openFileTxt():
            fileOpen = open("ips.txt","r")
            fileRead = fileOpen.read()
            fileData= fileRead.split(",")
            return fileData

class getAccess:
    def __init__(self,data,command):
        """ getAcc get data of files and a command to execute a multiple IPs """

    def connectToIp(self,ip,command):
        for i in range(len(ip)): 
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ip[i], username='admin', password='', timeout=3)
            except TimeoutError:
                print(f"Time out ip : {ip[i]}")
                continue
            stdin,stdout,strerror = client.exec_command(command)
            for line in stdout:
                dataBare = stdout.read().decode("ascii").replace("\n","")
                dataToStr = str(dataBare)
                client.close()
            