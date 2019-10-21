from Manager import Manager
import pickle
import pathlib
import os
import shutil
from DBConnection import DBConnection
from Nomenclator_List_Manager import NomenclatorListManager
from constants import PROBLEM_LOGS_DIR
from constants import FINISH_LOGS_PROCESING
from constants import INPUT_LOGS_DIRECTORY
from constants import OUTPUT_LOGS_DIRECTORY
from constants import DATABASE_LOGS_DIRECTORY


class Processor:

    def __init__(self):
        self.nomenclator_list_cache = NomenclatorListManager()
        self.hash_list = set()



    def index_database_update(self):
        operation_file = self.check_operation_file_exist(OUTPUT_LOGS_DIRECTORY)
        nomenclator_list_cache = self.check_nomenclator_list_cache_file_exist(OUTPUT_LOGS_DIRECTORY)

        p = pathlib.Path(OUTPUT_LOGS_DIRECTORY)
        for child in p.iterdir():
            file_name = str(child)
            print(file_name)
            if (file_name in operation_file):
                print("File done", file_name)
            else:
                data_file = open(child, 'rb')
                manager = pickle.load(data_file)
                nomenclator_list_cache.batch_cache_id_db_check(manager.get_nomenclator_list_manager().get_all_nomenclator_list())
                print("IDBSETTING begining...")
                
                manager.get_nomenclator_list_manager().id_db_setting()
                
                fn = DATABASE_LOGS_DIRECTORY + manager.get_file_name_preprocessing()+".pickle"
                self.object_saving(manager,fn )
                print("Finish operations", file_name)

                operation_file.add(file_name)
                self.object_saving(operation_file, self.get_operation_file_name(OUTPUT_LOGS_DIRECTORY))
                self.object_saving(nomenclator_list_cache, self.get_nomenclator_list_cache_file_name(OUTPUT_LOGS_DIRECTORY))

                

    def load_hash(self):
        result = None
        file_name = DATABASE_LOGS_DIRECTORY + "HASH.pickle"
        if (os.access(file_name, 0)):
            data_file = open(file_name, 'rb')
            result = pickle.load(data_file)
            print("cargado")
        else:
            dbconnection = DBConnection()
            result = dbconnection.get_all_logs_hash()
        return result



    def load_to_db(self):
        operation_file = self.check_operation_file_exist(DATABASE_LOGS_DIRECTORY)
        p = pathlib.Path(DATABASE_LOGS_DIRECTORY)
        for child in p.iterdir():
            file_name = str(child)
            print(file_name)
            if (file_name in operation_file):
                print("Operación concluida", file_name)
            else:
                data_file = open(child, 'rb')
                manager = pickle.load(data_file)
                print("Load file", manager.get_file_name_preprocessing())
                manager.load_to_database()

                print("Finish operation", file_name)
                operation_file.add(file_name)
                self.object_saving(operation_file, self.get_operation_file_name(DATABASE_LOGS_DIRECTORY))



    def get_operation_file_name(self, directory):
        return directory + "OPERATION_FILE.pickle"

    def get_nomenclator_list_cache_file_name(self, directory):
        return directory + "NOMENCLATOR_LIST_CACHE.pickle"


    def check_operation_file_exist(self, directory):
        result = None
        if (os.access(self.get_operation_file_name(directory), 0)):
            data_file = open(self.get_operation_file_name(directory), 'rb')
            result = pickle.load(data_file)
            print("cargado")
        else:
            result = set()
            result.add(self.get_operation_file_name(directory))
            result.add(self.get_nomenclator_list_cache_file_name(directory))
        return result


    def check_nomenclator_list_cache_file_exist(self, directory):
        result = None
        if (os.access(self.get_nomenclator_list_cache_file_name(directory), 0)):
            data_file = open(self.get_nomenclator_list_cache_file_name(directory), 'rb')
            result = pickle.load(data_file)
            print("Load Nomenclator List Cache")
        else:
            result =  NomenclatorListManager()
        return result



    def preprosessing(self):
        operation_file = self.check_operation_file_exist(INPUT_LOGS_DIRECTORY)

        p = pathlib.Path(INPUT_LOGS_DIRECTORY)
        for child in p.iterdir():
            file_name = str(child)
            print(file_name)
            if (file_name in operation_file):
                print("File done", file_name)
            else:
                manager = Manager() 
                manager.add_logs_manager(file_name)
                try:

                    manager.processing()
                    
                    fn = OUTPUT_LOGS_DIRECTORY + manager.get_file_name_preprocessing() + ".pickle"
                    #    print("Directorio a salvar", fn)
                    self.object_saving(manager, fn)


                    print("Finish operation", file_name)

                    operation_file.add(file_name)
                    self.object_saving(operation_file, self.get_operation_file_name(INPUT_LOGS_DIRECTORY))
                    shutil.move(file_name, FINISH_LOGS_PROCESING)

                except:
                    shutil.move(file_name, PROBLEM_LOGS_DIR)
                    print("Bad file")





    def object_saving(self, object, out_file_name):
        file_object = open(out_file_name, 'wb')
        pickle.dump(object, file_object)
        print(out_file_name)