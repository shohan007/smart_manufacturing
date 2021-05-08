import pandas as pd
import psycopg2 as pg

try:
    conn = pg.connect("postgres://vqwhcbktlfaihv:908a4af5059f235ddffa464534f293fbf70e292e2ffd8ca57a535c2767695aa8@ec2-18-204-74-74.compute-1.amazonaws.com:5432/d7g5bjs552srrc", sslmode="require")
    cur = conn.cursor()
    print("Connection Established")
except (Exception, pg.DatabaseError) as error:
    print(error)

#--------function that retrieves recent sensor data from Table using start and end timepoint (sec)
def sensorData(start, end):

    qCmd = f'SELECT * FROM public."sensorData" WHERE timestamp > {start} AND timestamp <= {end} ORDER BY timestamp DESC LIMIT 200;'
    df = pd.read_sql_query(qCmd, conn)

    if df.empty:
        qCmd = f'SELECT * FROM public."sensorData" ORDER BY timestamp DESC LIMIT 200'
        df = pd.read_sql_query(qCmd, conn)
    
    df['temperature'] = df['temperature'].apply(lambda x:x[0])
    df['pressure'] = df['pressure'].apply(lambda x:x[0])
    df['humidity'] = df['humidity'].apply(lambda x:x[0])
    
    return df