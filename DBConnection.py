import psycopg2
import os
import pickle
from configparser import ConfigParser
#from constants import HASH_PATH
from constants import DUPLICATED_DIRECTORY


class DBConnection:

	def __init__(self):
		print("Iniciando DBCONNECTION")
		param = self.config()
		self.PSQL_HOST = param["host"]
		self.PSQL_PORT = param["port"]
		self.PSQL_USER = param["user"]
		self.PSQL_PASS = param["password"]
		self.PSQL_DB   = param["database"]

		pool = (None, None)
		self.poolconn = list(pool)
		self.poolcur = list(pool)
		"""
		self.hash_list = self.load_hash()
		print("HASH CARGADOS", len(self.hash_list))
		"""

	def config(self, filename='database.ini', section='postgresql'):
		parser = ConfigParser()
		parser.read(filename)
		db = {}
		if parser.has_section(section):
			params = parser.items(section)
			for param in params:
				db[param[0]] = param[1]
		else:
			raise Exception('Section {0} not found in the {1} file'.format(section, filename))
		
		return db

	"""
	def load_hash(self):
		result = None
		if (os.access(HASH_PATH, 0)):
			data_file = open(HASH_PATH, 'rb')
			result = pickle.load(data_file)
			print("cargado")
		else:
			result = self.get_all_logs_hash()
		return result

	
	def get_all_logs_hash(self):
		result = set()
		self.connect()
		cur_select = self.poolcur[0]
		cur_select.execute("SELECT hash FROM logs")
		rows = cur_select.fetchall()
		for h in rows:
			result.add(h)
			print(h)
		self.desconnect()
		return result
		
	
	def save_hash(self):
		file_object = open(HASH_PATH, 'wb')
		pickle.dump(self.hash_list, file_object)
	"""

	def connect(self):
		connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (self.PSQL_HOST, self.PSQL_PORT, self.PSQL_USER, self.PSQL_PASS, self.PSQL_DB)
		for i in [0,1]:
			self.poolconn[i] = psycopg2.connect(connstr)
			self.poolcur[i] = self.poolconn[i].cursor()


	def desconnect(self):
		for i in [0,1]:
			self.poolcur[i].close()
			self.poolconn[i].close()


	def nomclators_update_db_id(self, nomenclator_list):
		self.connect()
		cur_select = self.poolcur[0]
		cur_insert = self.poolcur[1]
		temp_nom_list = list()
		count = 0
		tabla = nomenclator_list.table_name
		for nom in nomenclator_list.nom_list:
			if (nom.db_id == 0):
				#nombre = str(nom.nombre)

				cur_select.execute("SELECT id, description FROM {} WHERE description = %s".format(tabla),(nom.nombre,))
				rows = cur_select.fetchone()
				print(count, tabla)
				if (rows == None):
					print ("[+]", count, tabla, nom.nombre)
					#print("+", nom.nombre[:6])
					temp_nom_list.append(nom)
				else:
					nom.db_id = rows[0]
			else:
				print(". nom")
			count = count  + 1
		if ( len(temp_nom_list) > 0 ):
			for nom in temp_nom_list:
				nombre = nom.nombre
				cur_insert.execute("INSERT INTO {} (description) VALUES(%s) RETURNING id".format(tabla),(nombre,))
				self.poolconn[1].commit()
				nom.db_id = cur_insert.fetchone()[0]
				print("+ >>", nom.print())
		self.desconnect()
		print (count)



	def quickly_logs_insert_to_db(self, logs_manager):
		self.connect()
		tmp_list = list()
		cur_insert = self.poolcur[1]
		count = 0
		count_all = 1
		idarchivo = logs_manager.get_logs_list().get_logs_list()[0].log_file.db_id
		l = len(logs_manager.get_logs_list().get_logs_list())
		print("Cantidad de logs", l)
		for t in logs_manager.get_logs_list().get_logs_list():
			hash = t.hash
			if (hash in self.hash_list):
				print("-", count, count_all, l)
				tmp_list.append(t.log + '\n')
			else:
				posicion = t.posicion
				normal = t.normal
				repeat = t.repeat
				ip = t.ip.db_id
				date_string = t.date_string
				https = t.https
				http_method = t.http_method.db_id
				url = t.url.db_id
				domain = t.domain.db_id
				resourse = t.resourse.db_id
				http_version = t.http_version.db_id
				response_code = t.response_code.db_id
				size_request = t.size_request
				referer = t.referer.db_id
				ua = t.ua.db_id
				server_response = t.server_response.db_id
				log = t.log
				cur_insert.execute("INSERT INTO log (id_log_file, position, normal, repeat, id_ip, date_string, ishttps, id_http_method, id_url, id_domain, id_resource, id_http_version, id_response_code, size_request, id_referer, id_ua, id_server_response, log, hash)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (idarchivo, posicion, normal, repeat, ip, date_string, https, http_method, url, domain, resourse, http_version, response_code, size_request,referer, ua, server_response, log, hash,) )
				print("+", count, count_all, l)
				if (count > 20):
					self.poolconn[1].commit()
					count = 0
				else:
					count = count + 1
				self.hash_list.add(hash)
			count_all = count_all + 1
		if (count>0):
			self.poolconn[1].commit()
		self.desconnect()
		self.save_hash()
		n = DUPLICATED_DIRECTORY + "LOGS_REPETIDOS---"+str(idarchivo)+".txt"
		self.save_to_file(tmp_list, n  )











	def logs_insert_to_db(self, logs_manager):
		self.connect()
		cur_select = self.poolcur[0]
		cur_insert = self.poolcur[1]
		idarchivo = logs_manager.get_logs_list().get_logs_list()[0].log_file.db_id
		print ("--", idarchivo,"--" )
		count = 0
		for t in logs_manager.get_logs_list().get_logs_list():
			posicion = t.posicion
			normal = t.normal
			repeat = t.repeat
			ip = t.ip.db_id
			date_string = t.date_string
			https = t.https
			http_method = t.http_method.db_id
			url = t.url.db_id
			domain = t.domain.db_id
			resourse = t.resourse.db_id
			http_version = t.http_version.db_id
			response_code = t.response_code.db_id
			size_request = t.size_request
			referer = t.referer.db_id
			ua = t.ua.db_id
			server_response = t.server_response.db_id
			log = t.log
			hash = t.hash
			cur_select.execute("SELECT id  FROM log WHERE hash = %s",(hash,))
			rows = cur_select.fetchone()
			if (rows == None):
				cur_insert.execute("INSERT INTO log (id_log_file, position, normal, repeat, id_ip, date_string, ishttps, id_http_method, id_url, id_domain, id_resource, id_http_version, id_response_code, size_request, id_referer, id_ua, id_server_response, log, hash)  VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (idarchivo, posicion, normal, repeat, ip, date_string, https, http_method, url, domain, resourse, http_version, response_code, size_request,referer, ua, server_response, log, hash,) )
				print("Insertado", count)
				if (count > 20):
					self.poolconn[1].commit()
					count = 0
				else:
					count = count + 1

			else:
				print("Ya esta")
		self.poolconn[1].commit()
		self.desconnect()









	def save_to_file(self, tmp_list, file_name):
		print("Logs saving...", file_name)
		fn = file_name
		outfile = open(fn, 'w')
		counter_aux = 0
		for line in tmp_list:
			outfile.write(line)
			counter_aux = counter_aux + 1
			print(counter_aux)
		outfile.close()
		return counter_aux
