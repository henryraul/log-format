from Nomenclador import Nomenclador

class NomenclatorList:


    def __init__(self):
        self.nom_list = list()
        self.table_name = ""
        self.cache = list()
        self.max_value = -1
        self.nom_set = set()


    # SETTERS AND GETTERS
    def get_list(self):
        return self.nom_list


    def get_table_name(self):
        return self.table_name


    def get_count(self):
        return len(self.nom_list)


    # APPEND PROCESS
    def append_nomenclator(self,nombre):
        result = self.find_nomenclator(nombre)
        if (result == None):
            result = Nomenclador()
            result.nombre = nombre
            result.id = self.get_max_value()
            self.nom_list.append(result)
            self.cache.append(result)
            if (len(self.cache)>100):
                self.cache.pop(0)
            self.nom_set.add(nombre)
        return result


    def find_nomenclator(self,nombre):
        result = None
        if (nombre in self.nom_set):
            result = self.search_nomenclator(self.cache,nombre)
            if (result == None):
                result = self.search_nomenclator(self.nom_list, nombre)
        return result


    def search_nomenclator(self, nomenclator_list, string_search):
        result = None
        count = len(nomenclator_list)
        flag = count > 0
        pos = 0
        while (flag):
            if (nomenclator_list[pos].nombre == string_search):
                flag = False
                result = nomenclator_list[pos]
            else:
                pos = pos + 1
                flag = pos < count
        return result


    #UTILITIES
    def get_max_value(self):
        self.max_value = self.max_value + 1
        return self.max_value


    def set_id_batch(self):
        for i in self.nom_list:
            if (i.id == 0):
                i.id = self.get_max_value()
                i.print()


    def print(self):
        print("NOMENCLADORES: ", self.table_name)
        for i in self.nom_list:
            i.print()
        print(self.table_name, self.get_count())


    # FILES INTERACTIONS
    def save_to_file(self):
        print("SALVANDO EN",self.table_name)
        fn = self.table_name + ".txt"
        print(fn)
        new_nomenclators_outfile = open(fn, 'w')
        counter_aux = 0
        for n in self.nom_list:
            #print(n.nombre)
            new_nomenclators_outfile.write(n.save_string() + '\n')
            counter_aux = counter_aux + 1
        new_nomenclators_outfile.close()
        return counter_aux


    def load_to_file(self):
        print("LOAD EN",self.table_name)
        filename = self.table_name + ".txt"
        infile = open(filename, 'r')
        counter_aux = 0
        for line in infile:
            tuple = line[0:len(line) - 1]
            pos = tuple.find(":")
            idtmp = tuple[0:pos]
            id = int(idtmp)
            nombre = tuple[pos+1:len(tuple)]
            nomenclador = Nomenclador()
            nomenclador.nombre = nombre
            nomenclador.id = id
            self.nom_list.append(nomenclador)
            counter_aux = counter_aux + 1
        infile.close()
        return counter_aux

    # TESTING
    def pos_checking(self):
        result = True
        count = 0
        for n in self.nom_list:
            if (n.id != count):
                result = False
                print("No coincide",count,n.id)
            count = count + 1
        return result






