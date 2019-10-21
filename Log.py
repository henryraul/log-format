import hashlib
from constants import NULL_ELEMENT
from constants import TOKEN_END_LINE


class Log:

    def __init__(self):
        self.log_file = None
        self.posicion = 0
        self.normal = False
        self.repeat = 1
        self.ip = None
        self.date_string = ""
        self.https = False
        self.http_method = None
        self.url = None
        self.domain = None
        self.resourse = None
        self.http_version = None
        self.response_code = None
        self.size_request = 0
        self.referer = None
        self.ua = None
        self.server_response = None
        self.log = ""
        self.hash = ""


    def set_repeat(self):
        self.repeat = self.repeat + 1


    def get_domain(self):
        result = NULL_ELEMENT
        if (self.url_is_normal(self.url.nombre)):
            result = self.url.nombre[self.url.nombre.find("//")+2:]
            result = result[:result.find("/")]
        return result


    def get_resourse(self):
        result = NULL_ELEMENT
        if (self.url_is_normal(result)):
            pos = self.url.nombre.rfind("/")
            result = self.url.nombre[pos + 1:]
        return result


    def url_is_normal(self,url_string):
        result = self.url_is_HTTPS(url_string)
        if (not result):
            segment = url_string[0:7]
            if (segment == "http://"):
                result = True
        return result


    def url_is_HTTPS(self, url_string):
        result = False
        segment = url_string[0:8]
        if (segment == "https://"):
            result = True
        return result


    def get_hash_value(self):
        if (self.hash == ""):
            c = self.log.encode("utf-8")
            self.hash = hashlib.sha3_512(c).hexdigest()
        return self.hash


    def save_to_file(self):
        result = self.ip.get_id_to_str() + TOKEN_END_LINE
        result = result + self.date_string + TOKEN_END_LINE
        if (self.https):
            result = result + "1" + TOKEN_END_LINE
        else:
            result = result + "0" + TOKEN_END_LINE
        result = result + self.http_method.get_id_to_str() + TOKEN_END_LINE
        result = result + self.url.get_id_to_str() + TOKEN_END_LINE
        result = result + self.domain.get_id_to_str() + TOKEN_END_LINE
        result = result + self.resourse.get_id_to_str() + TOKEN_END_LINE
        result = result + self.http_version.get_id_to_str() + TOKEN_END_LINE
        result = result + self.response_code.get_id_to_str() + TOKEN_END_LINE
        result = result + str(self.size_request) + TOKEN_END_LINE
        result = result + self.referer.get_id_to_str() + TOKEN_END_LINE
        result = result + self.ua.get_id_to_str() + TOKEN_END_LINE
        result = result + self.server_response.get_id_to_str() + TOKEN_END_LINE
        result = result + self.log + TOKEN_END_LINE
        result = result + self.hash + TOKEN_END_LINE
        return result



    def analysis(self):
        if (self.url != None):
            if (self.url.nombre != ""):
                self.normal = self.url_is_normal(self.url.nombre)
                if (self.normal):
                    self.https = self.url_is_HTTPS(self.url.nombre)
                else:
                    self.https = False