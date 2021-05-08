  
import psycopg2 as pg

def create_table():
    conn = None
    try:
        #connecting to the Heroku Postgres DB
        conn = pg.connect("postgres://vqwhcbktlfaihv:908a4af5059f235ddffa464534f293fbf70e292e2ffd8ca57a535c2767695aa8@ec2-18-204-74-74.compute-1.amazonaws.com:5432/d7g5bjs552srrc", sslmode="require")
        cur = conn.cursor()
        print("Connection Established")

        #create a table within the cloud postgres
        createCmd = """ CREATE TABLE public."sensorData"(
                        machine_id integer NOT NULL,
                        temperature double precision[],
                        pressure double precision[],
                        humidity double precision[],
                        date date NOT NULL,
                        "timestamp" integer NOT NULL,
                        CONSTRAINT "sensorData_pkey" PRIMARY KEY (machine_id, date, "timestamp"))
                    """
        cur.execute(createCmd)

        cur.close()

        conn.commit()
    except (Exception, pg.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    create_table()