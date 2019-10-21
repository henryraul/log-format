from DBConnection import DBConnection
from constants import LOGS_FILE_TABLE_NAME
import psycopg2

class AnalysisDB:
    PSQL_HOST = "localhost"
    PSQL_PORT = "5432"
    PSQL_USER = "postgres"
    PSQL_PASS = "abretesesamo"
    PSQL_DB   = "weblogs_1005"

    def __init__(self):
        print("Iniciando AnalysisDB")
        self.connstr = "host=%s port=%s user=%s password=%s dbname=%s" % (self.PSQL_HOST, self.PSQL_PORT, self.PSQL_USER, self.PSQL_PASS, self.PSQL_DB)





    def logs_count_from_file(self):
        content_to_file = list()
        with psycopg2.connect(self.connstr) as conexion:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT * FROM "+LOGS_FILE_TABLE_NAME)
                rows = cursor.fetchall()
                for r in rows:
                    cursor.execute("SELECT COUNT(id) FROM log WHERE id_log_file=%s",(r[0],))
                    count = cursor.fetchone()
                    print(r[1],",",count[0])
                    line = r[1]+","+str(count[0])
                    content_to_file.append(line)
        self.save_to_file(content_to_file, "REP-LOGS-COUNT.csv")



    def save_to_file(self, content_to_file, filename):
        outfile = open(filename, 'w')
        for line in content_to_file:
            outfile.write(line + '\n')
        outfile.close()