# pip install mysqlclient

# c:\xampp\mysql\bin\mysql -u root < script_creacion.sql

# C:\xampp\mysql\bin\mysql -u root < ecotech_db.sql

import MySQLdb

def test():
    try:
        conexion = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="",
            db="ecotech_db"
        )
        print("Conexion exitosa!")
        cursor = conexion.cursor()
        cursor.execute("select version();")
        version = cursor.fetchone()[0]
        print(f"Version del servidor: {version}")
        conexion.close()
    except MySQLdb.Error as e:
        print(f"Error de conexion: {e}")

test()