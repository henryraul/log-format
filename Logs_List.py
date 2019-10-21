from constants import CONST_FILE_LOGS

class LogsList:

    def __init__(self):
        self.logs_list = list()
        self.filename = ""


    def get_logs_list(self):
        return self.logs_list


    def get_count(self):
        return len(self.logs_list)


    def append_log(self, newlog):
        result = True
        if (self.get_count() > 0):
            if (self.logs_list[-1].get_hash_value() == newlog.get_hash_value()):
                self.logs_list[-1].set_repeat()
                result = False
            else:
                self.logs_list.append(newlog)
        else:
            self.logs_list.append(newlog)
        return result


    def print(self):
        for i in self.logs_list:
            i.get_domain()


    def save_to_file(self, file_name):
        print("Logs saving...",self.filename)
        fn = file_name + CONST_FILE_LOGS
        outfile = open(fn, 'w')
        counter_aux = 0;
        for t in self.logs_list:
            outfile.write(t.save_to_file())
            counter_aux = counter_aux + 1
            print(counter_aux)
        outfile.close()
        return counter_aux



