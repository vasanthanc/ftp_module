from ftplib import FTP
from ftplib import error_perm
import re
import os

class FTP_Module:
    def __init__(self,*args,**kwargs):
        print(kwargs)
        self.server_address = kwargs.get("server_address",'127.0.0.1')
        self.port_address = kwargs.get("port",'21')
        self.user = kwargs.get("user_name",'')
        self.password = kwargs.get("password",'')
        self.ftp = None

    def connect_to_ftp(self):
        self.ftp = FTP()
        self.ftp.connect(self.server_address,int(self.port_address))
        self.ftp.login(self.user,self.password)

    def get_required_list(self,*args,**kwargs):
        list_files = kwargs.get("file_list",True)
        required_list = []
        raw_file_name_list = []
        full_file_details_list = []
        raw_file_name_list = self.ftp.nlst()
        self.ftp.dir(full_file_details_list.append)
        if type(raw_file_name_list) is list:
            for file_name,file_details in zip(raw_file_name_list,full_file_details_list):
                file_permission = file_details.split()[0]
                if list_files:
                    if not re.match(r'^d',file_permission):
                        required_list.append(file_name)
                else:
                    if re.match(r'^d',file_permission):
                        required_list.append(file_name)
        return required_list

    def list_all_directories(self,*args,**kwargs):
        kwargs["file_list"] = False
        list_of_directories = []
        list_of_directories = self.get_required_list(*args, **kwargs)
        print(list_of_directories)

    def get_list_all_files(self,*args,**kwargs):
        kwargs["file_list"] = True
        list_of_files = []
        list_of_files = self.get_required_list(*args, **kwargs)
        print(list_of_files)

    def create_directory(self,*args,**kwargs):
        status = False
        try:
            new_directory = kwargs.get("new_directoy",None)
            if new_directory is None:
                return None
            self.ftp.mkd(new_directory)
            status = True
        except Exception as error:
            print(error)
        return status

    def create_directoy_path(self,*args,**kwargs):
        status = False
        try:
            directory_path = kwargs.get("directory_path",None)
            if not directory_path:
                return None
            for index,directory_name in enumerate(directory_path.split("/")):
                print(directory_name)
                if not directory_name and index==0:
                    directory_name = "/"
                kwargs["to_directory"] = directory_name
                if self.change_working_directory(**kwargs):
                    print("Existing {}".format(directory_name))
                else:
                    kwargs["new_directoy"] = directory_name
                    if self.create_directory(**kwargs):
                        kwargs["to_directory"] = directory_name
                        if not self.change_working_directory(**kwargs):
                            raise Exception("could not create directory")
                        else:
                            print("created successfully")
                    else:
                        raise Exception("could not create directory")
                # print(directory_name)
            status = True
        except Exception as error:
            print(error)
        return status

    def change_working_directory(self,*args,**kwargs):
        status = False
        try:
            to_directory = kwargs.get("to_directory","/")
            self.ftp.cwd(to_directory)
            status = True
        except error_perm as perm_error:
            print(perm_error)
        except Exception as error:
            print(error)
        return status

    def upload_file(self,*args,**kwargs):
        status = False
        try:
            local_file_path = kwargs.get("local_file_path",None)
            remote_file_path = kwargs.get("remote_file_path",None)
            if not local_file_path or not remote_file_path:
                return status
            if not os.path.exists(local_file_path):
                raise Exception("File does not exist {}".format(local_file_path))
            print(remote_file_path)
            kwargs["directory_path"] = "/".join(remote_file_path.split("/")[0:-1])
            if self.create_directoy_path(**kwargs):
                with open(local_file_path,'rb') as file_obj:
                    file_name = remote_file_path.split("/")[-1]
                    print(file_name)
                    print('STOR {}'.format(file_name))
                    self.ftp.storbinary('STOR {}'.format(file_name), file_obj)
            status = True
        except Exception as error:
            print(error)
        return True

if __name__ == "__main__":
    kwargs = {"user_name":"","password":""}
    ftp = FTP_Module(**kwargs)
    ftp.connect_to_ftp()
    kwargs["remote_file_path"] = "Downloads/Download2/Download3/chrome.deb"
    kwargs["local_file_path"] = "/home/dev/Downloads/google-chrome-stable_current_amd64.deb"
    ftp.upload_file(**kwargs)
    # kwargs["to_directory"] = "Downloads"
    # ftp.change_working_directory(**kwargs)
    # kwargs["new_directoy"] = "Download2"
    # ftp.create_directory(**kwargs)
    # kwargs["to_directory"] = "Download2"
    # ftp.change_working_directory(**kwargs)
    # ftp.list_all_directories()
    # ftp.get_list_all_files()
