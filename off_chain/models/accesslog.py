from models.model_base import Model

#Modello e attributi per la tabella AccessLog
class AccessLog(Model):
    def __init__(self, id_utente, action, timestamp, id_access=None):
        super().__init__()
        self.id_access = id_access
        self.id_utente = id_utente
        self.action = action
        self.timestamp = timestamp

    def get_id_access(self):
        return self.id_access
    
    def get_id_utente(self):
        return self.id_utente
    
    def get_action(self):
        return self.action
    
    def get_timestamp(self):
        return self.timestamp

#Metodi ORM per interagire con il db SQLite per operazioni CRUD
    def save(self):
        if self.id_access is None:
            self.cur.execute('''INSERT INTO AccessLog (id_utente, action, timestamp)
                                VALUES (?, ?, ?)''',
                             (self.id_utente, self.action, self.timestamp))
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            self.cur.execute('''UPDATE AccessLog SET id_utente=?, action=?, timestamp=? WHERE id_access=?''',
                             (self.id_utente, self.action, self.timestamp, self.id_access))
        self.conn.commit()
        self.id_access = self.cur.lastrowid

    def delete(self):
        if self.id_access is not None:
            self.cur.execute('DELETE FROM AccessLog WHERE id_access=?', (self.id_access,))
            self.conn.commit()
