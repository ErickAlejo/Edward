from array import array
from lib2to3.pytree import type_repr
from logging import error
from os import strerror
import paramiko
import pandas as pd

#Open files
def open_File():
    file = open("ips.txt","r")
    file_output = str(file.read())
    file_data = file_output.split(",")
    return file_data

def open_file_excel():
    data = pd.read_excel("data/info.xlsx",sheet_name="Hoja1")
    data2 = data[["ips"]]
    arr = data2.loc[1]
    arr2 = [arr]
    print(arr2)
#Get Data
def get_Data(file_data,command_exec):
    #Iter on the file and pass command
    for i in range(len(file_data)):
        #Connect to SSH through mikrotik
        try:
            file_new = open(file_data[i],"w")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(file_data[i],username='admin',password='pass')
        except TimeoutError:
            print("Error")
            continue
        stdin, stdout, stderr = client.exec_command(command_exec)
        #Iter on output and save file
        for line in stdout:
            data_raw = stdout.read().decode("ascii").replace("\n","")
            data_trans = str(data_raw)
            file_new.write(data_trans)
            client.close()
    #Function Main
def main():
    try:
        command_exec = str(input("Command ✔ :  "))
        print("\n")
        get_Data(open_File(),command_exec)
    except KeyboardInterrupt:
        print("\n")
        print("Cancel ✘ ")

open_file_excel()
#main()
