def open_file_txt(path):
        """open_file_txt:function is used explicitly to open a file"""
        file_open = open(path, mode="r", encoding="utf-8")
        file_read = file_open.read()
        file_data = file_read.split(",")
        return file_data  # return a list of IPs

path = input("route : ")
open_file_txt(path)