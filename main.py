import os
import paramiko
import time

class GetFiles:
    """Class Get Files"""

    def __init__(self, path):
        """Initialized path"""
        self.path = path

    def open_file_txt(self):
        """Method to open file txt"""
        try:
            file_open = open(self.path, mode="r")
            file_read = file_open.read()
            file_data = file_read.split("\n")
            return file_data  # return a list of IPs
        except FileNotFoundError:
            os.system('cls')
            print("Error File not found, try again ! \n")
            run()


class SetSsh:
    """Class SSH """

    def __init__(self, command: str, password: str):
        """Constructors Initializing vars command and password"""
        self.command = command
        self.password = password


    def connect_to_ip(self, list_ips):
        """Method to connect to SSH"""
        for i in range(len(list_ips)):
            try:
                "Create a file to save the information"
                path_export = "data"
                exist_file = os.path.exists(path_export)
                if exist_file:
                    file_path = path_export + "/{}.txt"
                    create_file = open(file_path.format(
                        list_ips[i]), "w+")
                else:
                    os.mkdir(path_export)
                    file_path = path_export + "/{}.txt"
                    # create each file of hosts
                    create_file = open(file_path.format(
                        list_ips[i]), "w+")
                "Create a connection to SSH and we add a Policy Paramiko"
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(list_ips[i], username='admin',
                               password=str(self.password),banner_timeout=200)
            except TimeoutError:
                print(f"[Timeout: {list_ips[i]}]")
                client.close()
                continue
            except paramiko.ssh_exception.AuthenticationException:
                os.system('cls')
                print(f"[Password Failed: {list_ips[i]}]")
                client.close()
                continue
            except paramiko.ssh_exception.NoValidConnectionsError:
                print(f"[Probably bad ports : {list_ips[i]}]")
                continue
            stdin, stdout, stderr = client.exec_command(self.command)
            for i in stdout:
                data_bare = stdout.read().decode("ascii").replace("\n", "")
                create_file.write(data_bare)
                create_file.close()
                client.close()


def run():
    """Runner"""
    
    print(f"Host : {os.environ.get('USERNAME')}")
    print("Set duration=seconds when use monitor !\n")
    #path = str(input("[Directory] "))
    password = input("[Password] ")
    command = input("[$] ")
    SetSsh(command,password).connect_to_ip(GetFiles('ips.txt').open_file_txt())

run()