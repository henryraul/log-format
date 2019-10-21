#!/usr/bin/env python
# -*- coding: utf-8 -*-
from Logs_List import LogsList
from Log import Log
import os
from Nomenclator_List_Manager import NomenclatorListManager

class LogsManager:

    def __init__(self, nomenclator_list_manager ):
        self.nomenclator_list_manager = nomenclator_list_manager
        #nomenclator_list_manager.print()
        self.file_name = None
        self.logs_list = LogsList()
        print("LogsManager creado")


    def get_logs_list(self):
        return self.logs_list

    def get_file_name(self):
        return self.file_name

    def get_file_name_clean(self):
         return os.path.basename(self.file_name)

    def logs_processing(self):
        print("Processing...",self.get_file_name_clean())
        #infile = open(self.file_name.nombre, encoding="utf8")
        counter = 0
        #print("CANTIDAD DE TRAZAS INICIALES", self.logs_list.get_count())
        #print("******", self.get_file_name_clean())
        log_file = self.nomenclator_list_manager.get_logs_file_list().append_nomenclator(self.get_file_name_clean())
        #print("--------------------------", log_file.nombre, str(log_file.db_id))
        with open(self.file_name, 'r', encoding='utf8', errors='ignore') as infile:
        #infile = open(self.file_name.nombre, encoding="utf8")
            for line in infile:
                t = Log()
                t.log_file = log_file
                
                counter = counter + 1
                t.posicion = counter
                log = line[0:len(line) - 1]
                t.log = log
                if (self.logs_list.append_log(t)):
                    cadena = line

                    ip = cadena[0:cadena.index(" ")]

                    posicion = cadena.index("[")
                    cadena = cadena[posicion:]
                    date_string = cadena[1:cadena.index(" ")]

                    posicion = cadena.index('\"')
                    cadena = cadena[posicion:]
                    posicion = cadena.index(" ")
                    http_method = cadena[1:posicion]

                    cadena = cadena[posicion + 1:]
                    posicion = cadena.index(" ")
                    url = cadena[0:posicion]

                    cadena = cadena[posicion + 1:]
                    posicion = cadena.index('\"')
                    http_version = cadena[0:posicion]

                    cadena = cadena[posicion + 2:]
                    posicion = cadena.index(" ")
                    response_code = cadena[0:posicion]

                    cadena = cadena[posicion + 1:]
                    posicion = cadena.index(" ")
                    size_request = cadena[0:posicion]

                    cadena = cadena[posicion + 1:]
                    posicion = cadena.rfind(" ")
                    server_response = cadena[posicion + 1:len(cadena) - 1]

                    cadena = cadena[:posicion]
                    posicion = cadena.rfind("\" \"")
                    referer = cadena[1:posicion]

                    ua = cadena[posicion + 3:len(cadena) - 1]


                    t.ip = self.nomenclator_list_manager.get_ip_list().append_nomenclator(ip)

                    t.date_string = date_string
                    
                    t.http_method = self.nomenclator_list_manager.get_http_method_list().append_nomenclator(http_method)

                    t.url = self.nomenclator_list_manager.get_url_list().append_nomenclator(url)

                    t.http_version = self.nomenclator_list_manager.get_http_version_list().append_nomenclator(http_version)

                    t.response_code = self.nomenclator_list_manager.get_response_code_list().append_nomenclator(response_code)

                    t.size_request = size_request
                    
                    t.referer = self.nomenclator_list_manager.get_referer_list().append_nomenclator(referer)

                    t.ua = self.nomenclator_list_manager.get_ua_list().append_nomenclator(ua)

                    t.server_response = self.nomenclator_list_manager.get_server_code_list().append_nomenclator(server_response)

                    t.resourse = self.nomenclator_list_manager.get_resource_list().append_nomenclator(t.get_resourse())

                    t.domain = self.nomenclator_list_manager.get_domain_list().append_nomenclator(t.get_domain())

                    t.analysis()
                    print(counter)

        print("Procesadas", counter, "Trazas", self.file_name)
        print("CANTIDAD DE TRAZAS FINALES", self.logs_list.get_count())

















