from Database import DataStorageDatabaseClass
from multiprocessing import Process
from MessageConsumer import start_consumers 
from gRPCServer import serve

""" Main Function """
def main():
    db_instance = DataStorageDatabaseClass()
    db_instance.init_database()
    p = Process(target=start_consumers, args=[DataStorageDatabaseClass()])
    p.start()
    serve()

""" Start Main Script """

if __name__ == '__main__':
    main()