from DBConnection import DBConnection
from Logs_Manager import LogsManager
import os
from Nomenclator_List_Manager import NomenclatorListManager
import hashlib
import datetime


class Manager:

    def __init__(self):
        self.logs_manager_list = list()
        self.nomenclator_list_manager = NomenclatorListManager()
        print("CREADO MANAGER")


    def get_nomenclator_list_manager(self):
        return self.nomenclator_list_manager






    def get_file_name_preprocessing(self):
        #result = ""
        """
        for lm in self.logs_manager_list:
            result = result + str(lm.file_name.nombre)
        result = str(datetime.datetime.now())+ hashlib.md5(result.encode("utf-8")).hexdigest()
        return result.replace(":","-").replace(" ", "_").replace(".", "_")
        """
        return self.logs_manager_list[0].get_file_name_clean()

    


    def load_to_database(self):
        dbconnection = DBConnection()
        for lm in self.logs_manager_list:
            dbconnection.logs_insert_to_db(lm)
            #dbconnection.quickly_logs_insert_to_db(lm)


    def add_logs_manager(self,filename):
        #convert_file_name = print(filename[filename.find("\\")+1:])
        #convert_file_name = self.get_file_name_clean(filename)
        #fn = self.nomenclator_list_manager.get_logs_file_list().append_nomenclator(convert_file_name)
        result = LogsManager(self.get_nomenclator_list_manager())
        #result.file_name = fn
        result.file_name = filename
        self.logs_manager_list.append(result)
        print ("add_logs_manager")
        return result


    def processing(self):
        for i in self.logs_manager_list:
            print("FILE NAME:", i.file_name)
            i.logs_processing()
        

