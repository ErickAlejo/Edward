import paramiko
import pandas as pd
import numpy as np

def open_file_excel():
    #Open file excel
    sheet_add = pd.read_excel("data/info.xlsx",sheet_name="Hoja1")
    sheet_value = sheet_add[["ips"]]
    sheet_value_to_list = sheet_value.values.tolist()
    value_to_list = np.array(sheet_value_to_list) 
    value_to_arr = value_to_list.reshape(-1).tolist()
    return value_to_arr

def open_file_txt():
    #Open file txt
    file_add = open("ips.txt","r")
    file_value = file_add.read()
    file_value_to_list = file_value.split("\n")
    return file_value_to_list

def get_Data(value_to_arr,command):
    for i in range(len(value_to_arr)):
        #Connect to SSH 
        try:
            dir_output = "output_export/{}.txt"
            create_file = open(dir_output.format(value_to_arr[i]),"w+")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(value_to_arr[i],username='admin',password='')
        except TimeoutError:
            print("Error")
            print("")
            continue
        except FileNotFoundError:
            print("Error with Directory")
            print("")
            break
        stdin, stdout, stderr = client.exec_command(command)
        for line in stdout:
            data_buffer = stdout.read().decode("ascii").replace("\n","")
            data_to_str = str(data_buffer)
            create_file.write(data_to_str)
            create_file.write("")
            create_file.close()
            client.close()
    command_repeat = input("🪶  Again [y/n] : ")
    if command_repeat == "y":
        main()
    else:
        return False

def main():
    try:
        command = str(input("🪶  Command : "))
        get_Data(open_file_txt(),command)
    except KeyboardInterrupt:
        print("\n")
        print("Cancel ✘ ")

main()