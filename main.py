import os
import paramiko


class GetFiles:
    """getFiles:class is used to get data of files """

    def __init__(self, path):
        """ path:str is the route of all IPs"""
        self.path = path

    def open_file_txt(self):
        """open_file_txt:function is used explicitly to open a file"""
        try:
            file_open = open(self.path, mode="r", encoding="utf-8")
            file_read = file_open.read()
            file_data = file_read.split(",")
            return file_data  # return a list of IPs
        except FileNotFoundError:
            os.system('cls')
            print("Error File not found, try again ! \n")
            run()


class SetSsh:
    """setParamsSsh:class is used to set variables and methods for connect via SSH """

    def __init__(self, command: str, password: str):
        """command:str is the command to execute, password:str is password to each host"""
        self.command = command
        self.password = password

    def connect_to_ip(self, list_ips):
        """connect_to_ip:function is used to finally connect to a IP """
        for i in range(len(list_ips)):
            try:
                path_export = "data"
                exist_file = os.path.exists(path_export)
                if exist_file:
                    file_path = path_export + "/{}.txt"
                    create_file = open(file_path.format(
                        list_ips[i]), "w+", encoding="utf-8")
                else:
                    os.mkdir(path_export)
                    file_path = path_export + "/{}.txt"
                    # create each file of hosts
                    create_file = open(file_path.format(
                        list_ips[i]), "w+", encoding="utf-8")
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                client.connect(list_ips[i], username='admin',
                               password=str(self.password), timeout=2)
            except TimeoutError:
                print(f"[Timeout : {list_ips[i]}]")
                client.close()
                break
            except paramiko.ssh_exception.AuthenticationException:
                os.system('cls')
                print("Your password or user is failed")
                run()
            # The command’s input and output streams are returned as Python file-like objects representing stdin, stdout, and stderr.
            stdin, stdout, stderr = client.exec_command(
                self.command, timeout=3)
            for i in stdout:
                data_bare = stdout.read().decode("utf-8").replace("\n", "")
                create_file.write(data_bare)
                create_file.close()
                client.close()


def run():
    """run:function is used with main function to run the program """
    print(f"Host : {os.environ.get('USERNAME')}")
    print("Set duration=seconds when use monitor !\n")
    path = str(input("[Directory] > "))
    password = input("[Password] > ")
    command = input("[$] > ")
    SetSsh(command, password).connect_to_ip(GetFiles(path).open_file_txt())


run()
