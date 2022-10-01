import paramiko


def open_File():
    file = open("ips.txt","r")
    file_raw = file.read()
    file_arr = file_raw.split()
    return file_arr

def get_Data(arr_data):
    for i in arr_data:
        try:

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(file_arr[i],"admin","pass")
        except TimeOutError:
            print("Dispositivo : ",file_arr[i]," TimeOut")
            continue
        stdin, stdout, stderr = ssh.exec_command("system routerboard pr")
        print(stdout.read().decode("ascii").strip("\n"))
        ssh.close()

def get_Data(open_File())
