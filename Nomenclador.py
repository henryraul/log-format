class Nomenclador:

    def __init__(self):
        self.id = 0
        self.nombre = ""
        self.db_id = 0

    # SETTERS AND GETTERS
    def print(self):
        print("ID: ",self.id,"Nombre: ",self.nombre, "ID BD:",self.db_id)

    # UTILITIES
    def get_id_to_str(self):
        return str(self.id)


    def save_string(self):
        result = str(self.id) + ":" + self.nombre
        return result