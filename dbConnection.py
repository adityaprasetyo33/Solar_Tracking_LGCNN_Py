import mysql.connector
import random
import numpy as np
import decimal


class getData:
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost", user="username", password="password", 
            database="skripsi_fix"
        )

    def getTraining(self, val):
        mycursor = self.mydb.cursor()
        sql = "SELECT dt1,dt2,dt3,dt4,dt5,dt6,dt7,dt8,dt9 FROM tb_data WHERE id IN (SELECT id_training FROM sub_data_training WHERE id_jlm_training = %s)"
        mycursor.execute(sql, (val,))
        myresult = mycursor.fetchall()
        return myresult

    def getTrainingKelas(self, val):
        mycursor = self.mydb.cursor()
        mycursor.execute(
            "SELECT kelas FROM tb_data WHERE id IN (SELECT id_training FROM sub_data_training WHERE id_jlm_training = %s)", (val, ))
        myresult = mycursor.fetchall()
        return myresult

    def getVariasi(self):
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT * FROM dt_jlm_training")
        myresult = mycursor.fetchall()
        return myresult

    def updateVariasi(self, val):
        mycursor = self.mydb.cursor()
        mycursor.execute("UPDATE dt_jlm_training SET variasi = %s, error= %s, iterasi = %s WHERE id = %s;",
                         (val[2], val[3], int(val[4]), int(val[0]),))
        self.mydb.commit()

    def generateDataUji(self, val):
        # check exist
        mycursor = self.mydb.cursor()
        mycursor.execute(
            "SELECT * FROM sub_data_training WHERE id_jlm_training = %s;", (val,))
        myresult = mycursor.fetchall()

        if not myresult:
            mycursor.execute(
                "SELECT * FROM dt_jlm_training WHERE id = %s;", (val,))
            jml_test = mycursor.fetchone()
            id_random = np.sort(random.sample(range(1, 451), jml_test[1]))
            for y in range(len(id_random)):
                mycursor.execute(
                    "INSERT INTO sub_data_training (id_jlm_training, id_training) VALUES (%s, %s)", (int(jml_test[0]), int(id_random[y])))
                self.mydb.commit()

    def insertHasil(self, arr):
        val =tuple(np.vectorize(decimal.Decimal)(arr))
        #data = decimal.Decimal(arr)
        #print(val)
        #val = tuple(arr.astype(np.float32))
        mycursor = self.mydb.cursor()
        sql = "INSERT INTO tb_output (sensor1, sensor2, sensor3, sensor4, sensor5, sensor6, sensor7, sensor8, sensor9, v_dinamis,v_statis,hasil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        mycursor.execute(sql
            , val)
        self.mydb.commit()
