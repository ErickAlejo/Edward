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
                "Create a connection to SSH and we add a Policy Paramiko"
                ips_error = []
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(ips_list[i], username='admin',
                               password=str(self.password), banner_timeout=200)
            except TimeoutError:
                print(f"[Error Timeo]:\t[{ips_list[i]}]  ⚠️")
                client.close()
                continue
            except paramiko.ssh_exception.AuthenticationException:
                os.system('cls')
                print(f"[Error Auths]:\t{ips_list[i]}  ⚠️")
                client.close()
                continue
            except paramiko.ssh_exception.NoValidConnectionsError:
                print(f"[Error Ports]:\t{ips_list[i]}  ⚠️")
                continue
            except Exception as error:
                ips_error.append(ips_list[i])
                print(f"[Error Unkno]:\t{ips_error}  ⚠️")
                # print(f"[{error}]")
                continue

            # Execute first command
            data_name = ''
            stdin, stdout, stderr = client.exec_command(
                '/system identity export')
            for x in stdout:
                data_bare = stdout.read().decode("ascii").replace("\n", "").split()
                data_conver = data_bare[9].split('name=')
                data_name = data_conver[1]
                "Create a file to save the information"
                path_export = "data"
                path_exist_file = os.path.exists(path_export)

                # Evaluation to create a file with name of edge
                if path_exist_file:
                    file_path = path_export + "/{}.txt"
                    file_create = open(file_path.format(
                        data_name), "w+")
                else:
                    os.mkdir(path_export)
                    file_path = path_export + "/{}.txt"
                    # create each file of hosts
                    file_create = open(file_path.format(
                        ips_list[i]), "w+")
                break

            # Execute second command and modifiying session vars
            stdin, stdout, stderr = client.exec_command(self.command)
            for y in stdout:
                data_bare = stdout.read().decode("ascii").replace("\n", "")
                file_create.write(data_bare)
                file_create.close()
                print(f"[{data_name}  {ips_list[i]}]: ✅")
                client.close()


def run():
    """Runner"""
    print("Nota : Cuidado con el comando que uses !!!")
    #path = str(input("[Directory] "))
    password = input("[Password] ")
    command = input("[$] ")
    print("")
    SetSsh(command, password).connect_to_ip(
        GetFiles('ips.txt').open_file_txt())


run()
