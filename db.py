import mysql.connector
import hashlib

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
 
    def authorrized(self, request):
        auth = request.authorization
        username = auth.username
        password = auth.password
        password=(hashlib.sha256(password.encode('utf-8')).hexdigest())
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT password FROM user WHERE login = '{username}'"
        cursor.execute(req)
        data = cursor.fetchone()
        conn.close()
        if data and (data[0] == password):
            return True
        else:
            return False
        
    def connect(self):
        mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
            )
        return mydb
    
    def create(self, nom, prenom, email, telephone):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"INSERT INTO etudiant (nom, prenom, email, telephone) \
        VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')"    
        cursor.execute(req)
        conn.commit()
        etudiant_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return etudiant_id

    def delete(self, id):
        conn = self.connect()
        cursor = conn.cursor()

        req = f"DELETE FROM etudiant WHERE idetudiant = {id}"
        
        try:
            cursor.execute(req)
            if cursor.rowcount == 0:
                return False 
            conn.commit()
            cursor.close()
            conn.close()

            return True
        except mysql.connector.Error as err:
            print(f"Erreur lors de la suppression : {err}")
            conn.rollback()
            cursor.close()
            conn.close()

            return False  

    def readall(self):
        conn = self.connect()
        cursor = conn.cursor()
        req = "SELECT * FROM etudiant"
        cursor.execute(req)
        #print(req)
        data = cursor.fetchall()
        conn.close()
        return data
    
    def readone(self, id):
        conn = self.connect()
        cursor = conn.cursor()
        req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        data = cursor.fetchone()
        conn.close()
        return data
    
    def update(self, id, nom=None, prenom=None, email=None, telephone=None):
        conn = self.connect()
        cursor = conn.cursor()
        req = "UPDATE etudiant SET "
        updates = []
        if nom is not None:
            updates.append(f"nom = '{nom}'")
        if prenom is not None:
            updates.append(f"prenom = '{prenom}'")
        if email is not None:
            updates.append(f"email = '{email}'")
        if telephone is not None:
            updates.append(f"telephone = '{telephone}'")
        if updates:
            req += ", ".join(updates) + f" WHERE idetudiant = {id}"
            try:
                cursor.execute(req)
                if cursor.rowcount == 0:
                    return False
                conn.commit()
                cursor.close()
                conn.close()
                return True 
            except mysql.connector.Error as err:
                print(f"Erreur lors de la mise à jour : {err}")
                conn.rollback()
                cursor.close()
                conn.close()
                return False  
        else:
            cursor.close()
            conn.close()
            return False
        
    def log(self, request):
        try:
            auth = request.authorization
            username = auth.username
            password = auth.password
            password=(hashlib.sha256(password.encode('utf-8')).hexdigest())
        except:
            return 401
        try:
            conn = self.connect()
            curs = conn.cursor()
        except:
            return 500
        try:
            curs.execute(f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'")
            data = curs.fetchone()
            if data:
                return data
            else:
                return 401
        except:
            return(401)
        finally:
            conn.close()
