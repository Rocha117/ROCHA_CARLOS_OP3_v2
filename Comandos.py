import psycopg2


def Crear_tabla(tabla):
    conn = None
    sql = f"""CREATE TABLE {tabla} (
      Nombre VARCHAR NOT NULL,
      PUNTAJE VARCHAR NOT NULL)"""

    try:
        conn = psycopg2.connect(host="localhost",
                                database="Scoreboard_base",
                                user="postgres",
                                password="a",
                                port="5432")
        cur = conn.cursor()
        cur.execute(sql)
        conn.commit()
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def añadir(tabla, nombre, puntaje):
    conn = None
    sql = f"""INSERT INTO {tabla} (Nombre,PUNTAJE) VALUES(%s, %s);"""

    try:
        conn = psycopg2.connect(host="localhost",

                                database="Scoreboard_base",

                                user="postgres",

                                password="a",

                                port="5432")

        cur = conn.cursor()
        cur.execute(sql, (nombre, puntaje))
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:

        print(error)

    finally:

        if conn is not None:

            conn.close()


def Buscar(nombre):
    conn = None
    try:
        conn = psycopg2.connect(host="localhost",

                                database="Scoreboard_base",

                                user="postgres",

                                password="a",

                                port="5432")

        cur = conn.cursor()
        tabla = "Scoreboard"
        cur.execute(f"SELECT * FROM {tabla} WHERE Nombre = %s", (nombre,))
        usuario = cur.fetchone()
        conn.commit()
        cur.close()
        return usuario
    except (Exception, psycopg2.DatabaseError) as error:

        print(error)

    finally:

        if conn is not None:

            conn.close()


def MostrarTodo(tabla):
    conn = None
    try:
        conn = psycopg2.connect(host="localhost",

                                database="Scoreboard_base",

                                user="postgres",

                                password="a",

                                port="5432")

        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {tabla};")
        u = cur.fetchall()
        print(u)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:

        print(error)

    finally:

        if conn is not None:

            conn.close()
