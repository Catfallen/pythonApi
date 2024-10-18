import psycopg2 

#conn = psycopg2.connect(database = 'python',host = "localhost",user = "postgres",port = "5432",password = "markim")

conn = psycopg2.connect(
        database='python',
        host='localhost',
        user='postgres',
        password='markim',
        port='5432'
    )
cursor = conn.cursor()
#cursor.execute('''CREATE TABLE USERS(
#    id SERIAL PRIMARY KEY,
#    name VARCHAR               
#);
#''')

cursor.execute('''insert into users (name) values ('markim'),('yan'),('italo');
''')

conn.commit()
conn.close()





