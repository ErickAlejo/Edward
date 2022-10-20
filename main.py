from os import remove
import paramiko
import pandas as pd
import numpy as np
import time 


def open_file_excel():
    #Open file excel
    sheet_add = pd.read_excel("output_export/info.xlsx",sheet_name="Hoja2")
    sheet_value = sheet_add[["ips"]]
    sheet_value_to_list = sheet_value.values.tolist()
    value_to_list = np.array(sheet_value_to_list) 
    value_to_arr = value_to_list.reshape(-1).tolist()
    return value_to_arr

def open_file_txt():
    #Open file txt
    file_add = open("ips.txt","r")
    file_value = file_add.read()
    file_value_to_list = file_value.split(",")
    return file_value_to_list

def create_string_to_vector (cadena,area_name,area_border,area_cost,area_name2,area_border2,area_cost2): 
    cadena2 = cadena.split()
    if len(cadena2) > 7 :
        indexes = [0,2,2,3,5,5]
        for index in sorted(indexes, reverse=False):
           del cadena2[index]
        area_name.append(cadena2[0])
        area_border.append(cadena2[1])
        area_cost.append(cadena2[2])
        area_name2.append(cadena2[3])
        area_border2.append(cadena2[4])
        area_cost2.append(cadena2[5])
    elif len(cadena2) < 7:
        indexes = [0,2,2]
        for index in sorted(indexes, reverse=False):
           del cadena2[index]
        area_name.append(cadena2[0])
        area_border.append(cadena2[1])
        area_cost.append(cadena2[2])
    else:
        print("error")
    df = pd.DataFrame({'Area_Name':area_name, 'Area_Borde_one':area_border, 'Cost':area_cost })
    write_excel('output_export/info.xlsx','Hoja1',df)


def separate_info():
    print("h")

def write_excel(filename,sheetname,dataframe):
    with pd.ExcelWriter(filename, engine='openpyxl', mode='a') as writer: 
        workBook = writer.book
        try:
            workBook.remove(workBook[sheetname])
        except:
            print("Worksheet does not exist")
        finally:
            dataframe.to_excel(writer, sheet_name=sheetname,index=False)
            writer.save()

#df = pd.DataFrame({'Col1':[1,2,3,4,5,6], 'col2':['foo','bar','foobar','barfoo','foofoo','barbar']})
#write_excel('output_export/info.xlsx','Hoja1',df)


def get_Data(value_to_arr,command):
    area_name = []
    area_border = []
    area_cost = []
    area_name2 = []
    area_border2 = []
    area_cost2 = []
    for i in range(len(value_to_arr)):
        #Connect to SSH 
        try:
            dir_output = "output_export/{}.txt"
            create_file = open(dir_output.format(value_to_arr[i]),"w+")
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(value_to_arr[i],username='admin',password='S0m0s_2021S0m0s_2021')
        except TimeoutError:
            print("Error")
            print("")
            continue
        except FileNotFoundError:
            print("Error with Directory")
            print("")
            break
        if command.find("speed-test"):
            stdin, stdout, stderr = client.exec_command(command)
            time.sleep(5)
        elif command.find("monitor"):
            time.sleep(3)
            stdin, stdout, stderr = client.exec_command(command)
        else:
            stdin, stdout, stderr = client.exec_command(command)
        
        for line in stdout:
            data_buffer = stdout.read().decode("ascii").replace("\n","")
            data_to_str = str(data_buffer)
            create_string_to_vector(data_buffer,area_name,area_border,area_cost,area_name2,area_border2,area_cost2)
            create_file.write(data_to_str)
            create_file.write("")
            create_file.close()
            client.close()
    command_repeat = input("🪶  Again y/n : ")
    if command_repeat == "y":
        main()
    else:
        print("🪶  Cancel ✘ ")

def main():
    try:
        command = str(input("🪶  Command : "))
        get_Data(open_file_excel(),command)
    except KeyboardInterrupt:
        print("\n")
        print("Cancel ✘ ")

main()