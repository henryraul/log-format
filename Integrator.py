from Processor import Processor
#pre
p = Processor()
p.preprosessing()


#proclear
p.index_database_update()

#post
p.load_to_db()