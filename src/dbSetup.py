from dbOperations import Couch

foo = Couch('localhost', '5984')

print " Creating databases...."
foo.createDb('userdb')
foo.createDb('pindb')
foo.createDb('boarddb')
print " Succesfully created userdb, pindb, boarddb databases"
