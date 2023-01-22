@app.route("/")
def hello_world():
    database = connect()
    cursor = database.cursor()
    try:
        cursor.execute("INSERT INTO metriche (id, nome, metadata) VALUES (15, 'averageMem', 'Pippo pluto')")
        cursor.execute("INSERT INTO statistiche (id, nome) VALUES (1, 'MAX')")
        cursor.execute("INSERT INTO statistiche_metriche (id_metrica, id_statistica, timestamp, 1h, 3h, 12h) VALUES (15, 1, 00001, 15, 12, 20)")
        return "<p>Hello World</p>"
    except Error as e:
        print("Error while execute the query", e)
    finally:
        cursor.close()
        close(database)

def execute(query):
    database = connect()
    cursor = database.cursor()
    data = False
    try:
        cursor.execute(query)
        data = cursor
    except Error as e:
        print("Error while execute the query", e)
    print(data)
    return data