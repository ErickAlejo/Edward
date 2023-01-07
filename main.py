import paramiko
import time
import os

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

    def connect_to_ip(self, ips_list):
        """Method to connect to SSH"""
        for i in range(len(ips_list)):
            try:
                "Create a file to save the information"
                ips_error = []
                path_export = "data"
                path_exist_file = os.path.exists(path_export)
                if path_exist_file:
                    file_path = path_export + "/{}.txt"
                    file_create = open(file_path.format(
                        ips_list[i]), "w+")
                else:
                    os.mkdir(path_export)
                    file_path = path_export + "/{}.txt"
                    # create each file of hosts
                    file_create = open(file_path.format(
                        ips_list[i]), "w+")
                "Create a connection to SSH and we add a Policy Paramiko"
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ips_list[i], username='admin',
                               password=str(self.password), banner_timeout=200)
            except TimeoutError:
                print(f"[Error Timeout] : {ips_list[i]} ⚠️")
                client.close()
                continue
            except paramiko.ssh_exception.AuthenticationException:
                os.system('cls')
                print(f"[Error Authentication] : {ips_list[i]} ⚠️")
                client.close()
                continue
            except paramiko.ssh_exception.NoValidConnectionsError:
                print(f"[Error Port request] : {ips_list[i]} ⚠️")
                continue
            except Exception as error:
                ips_error.append(ips_list[i])
                print(f"{ips_error}:⚠️")
                #print(f"[{error}]")
                continue
            print(f"[{ips_list[i]}]: ✅")
            stdin, stdout, stderr = client.exec_command(self.command)
            for i in stdout:
                
                data_bare = stdout.read().decode("ascii").replace("\n", "")
                file_create.write(data_bare)
                file_create.close()
                client.close()


def run():
    """Runner"""
    print("Nota : Podrias lanzar un reset a todos los equipos que tengas, cuidado!")
    #path = str(input("[Directory] "))
    password = input("[Password] ")
    command = input("[$] ")
    print("\n")
    SetSsh(command, password).connect_to_ip(
        GetFiles('ips.txt').open_file_txt())


run()
