from model_base import Model

#Costruttore e attributi della tabella Credentials
class Credentials(Model):
    def __init__(self, username, hash_password, role, public_key, private_key, id=None):
        super().__init__()
        self.id = id
        self.username = username
        self.hash_password = hash_password
        self.role = role
        self.public_key = public_key
        self.private_key = private_key

    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username
    
    def get_hash_password(self):
        return self.hash_password
    
    def get_role(self):
        return self.role
    
    def get_public_key(self):
        return self.public_key
    
    def get_private_key(self):
        return self.private_key

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id is None:
            self.cur.execute('''INSERT INTO Credentials (username, hash_password, role, public_key, private_key)
                                VALUES (?, ?, ?, ?, ?)''', (self.username, self.hash_password, self.role, self.public_key, self.private_key)) 
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE Credentials SET username=?, hash_password=?, role=?, public_key=?, private_key=? WHERE id=?''',
                             (self.username, self.hash_password, self.role, self.public_key, self.private_key, self.id))
        self.conn.commit()
        self.id = self.cur.lastrowid

    def delete(self):
        if self.id is not None:
            self.cur.execute('DELETE FROM Credentials WHERE id=?', (self.id,))
            self.conn.commit()
