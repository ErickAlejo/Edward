from array import array
from lib2to3.pytree import type_repr
from os import strerror
import paramiko

#Open and get Data
def open_File():
    file_readable = open("ips.txt","r")
    file_txt = str(file_readable.read())
    file_arr = file_txt.split()
    return file_arr

#Backend

def get_Data(file_arr,command_exec):
    
    for i in range(len(file_arr)):
        try:

            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(file_arr[i],username='admin',password='pass')
        except TimeoutError:
            print("Error")
            continue
        stdin, stdout, stderr = client.exec_command(command_exec)
        for line in stdout:
            data_raw = stdout.read().decode("ascii").strip("\n")
            data_arr = data_raw.split()
            print(data_arr,"\n")
            client.close()

def main():
    print("\033[1;32m","\"Sempre parece imposible hasta que se hace -\"")
    print("\033[1;37m")
    command_exec = str(input("Por favor digite el comando : "))
    if (command_exec === "system reset-configuration"):
        print("No se puede")
        main()
    else:
        get_Data(open_File(),command_exec)

main()
