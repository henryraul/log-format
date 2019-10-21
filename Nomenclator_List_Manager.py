from Nomenclator_List import NomenclatorList
from DBConnection import DBConnection
from constants import IP_TABLE_NAME
from constants import UA_TABLE_NAME
from constants import CODE_SERVER_TABLE_NAME
from constants import METHOD_HTTP_TABLE_NAME
from constants import REFERER_TABLE_NAME
from constants import URL_TABLE_NAME
from constants import RESPONSE_CODE_TABLE_NAME
from constants import HTTP_VERSION_TABLE_NAME
from constants import DOMAIN_TABLE_NAME
from constants import RESOURCE_TABLE_NAME
from constants import LOGS_FILE_TABLE_NAME

class NomenclatorListManager:

    def __init__(self):
        self.logs_manager_list = list()
        self.ip_list = NomenclatorList()
        self.ip_list.table_name = IP_TABLE_NAME
        self.ua_list = NomenclatorList()
        self.ua_list.table_name = UA_TABLE_NAME
        self.server_code_list = NomenclatorList()
        self.server_code_list.table_name = CODE_SERVER_TABLE_NAME
        self.http_method_list = NomenclatorList()
        self.http_method_list.table_name = METHOD_HTTP_TABLE_NAME
        self.referer_list = NomenclatorList()
        self.referer_list.table_name = REFERER_TABLE_NAME
        self.url_list = NomenclatorList()
        self.url_list.table_name = URL_TABLE_NAME
        self.response_code_list = NomenclatorList()
        self.response_code_list.table_name = RESPONSE_CODE_TABLE_NAME
        self.http_version_list = NomenclatorList()
        self.http_version_list.table_name = HTTP_VERSION_TABLE_NAME
        self.domain_list = NomenclatorList()
        self.domain_list.table_name = DOMAIN_TABLE_NAME
        self.resource_list = NomenclatorList()
        self.resource_list.table_name = RESOURCE_TABLE_NAME
        self.logs_file_list = NomenclatorList()
        self.logs_file_list.table_name = LOGS_FILE_TABLE_NAME
        self.all_nomenclator_list = [self.ip_list, self.ua_list, self.server_code_list, self.http_method_list,
                                     self.referer_list, self.url_list,
                                     self.response_code_list, self.http_version_list, self.domain_list,
                                     self.resource_list, self.logs_file_list]
        self.nomenclador_index = {"m-*-m": "-1"}
        self.nomenclador_index.clear()
        for n in self.all_nomenclator_list:
            self.nomenclador_index[n.table_name] = n

        self.nomenclador_dict_temp = self.nomenclador_index.copy()



    def id_db_setting(self):
        dbconnection = DBConnection()
        for n in self.all_nomenclator_list:
            dbconnection.nomclators_update_db_id(n)
        #print(len(self.logs_file_list.get_list()))


    def cache_id_db_check(self, nom_list):
        print(nom_list.get_table_name())
        if (nom_list.get_table_name() in self.nomenclador_index):
            nl = self.nomenclador_index[nom_list.get_table_name()]
            for n in nom_list.get_list():
                nt = nl.find_nomenclator(n.nombre)
                if (nt == None):
                    self.nomenclador_dict_temp[nom_list.get_table_name()].get_list().append(n)
                    print("+ ch", n.nombre)
                else:
                    n.db_id = nt.db_id
                    print(". ch")



    def batch_cache_id_db_check(self, all_nom_list):
        for n in all_nom_list:
            self.cache_id_db_check(n)
            print(n.table_name)



    # BATCH NOMENCLATORS OPERATIONS
    def print(self):
        for n in self.all_nomenclator_list:
            n.print()

    def nomenclator_save_to_file(self):
        print("SALVANDO...")
        for n in self.all_nomenclator_list:
            n.save_to_file()




# GET Y SET
    def get_ip_list(self):
        return self.ip_list

    def get_ua_list(self):
        return self.ua_list

    def get_server_code_list(self):
        return self.server_code_list

    def get_http_method_list(self):
        return self.http_method_list

    def get_referer_list(self):
        return self.referer_list

    def get_url_list(self):
        return self.url_list

    def get_response_code_list(self):
        return self.response_code_list

    def get_http_version_list(self):
        return self.http_version_list

    def get_domain_list(self):
        return self.domain_list

    def get_resource_list(self):
        return self.resource_list

    def get_all_nomenclator_list(self):
        return self.all_nomenclator_list;

    def get_logs_file_list(self):
        return self.logs_file_list













