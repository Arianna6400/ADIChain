import sqlite3

#Modello di base da estendere per l'implementazione degli altri Models
class Model:
    db_path = "ADIChain"

    #Costruttore della classe
    def __init__(self):
        self.con = sqlite3.connect(Model.db_path)
        self.cur = self.con.cursor()

    #Metodi virtuali, con le sottoclassi che implementano i metodi (classi che derivano dal modello)
    def save(self):
        raise NotImplementedError("Subclasses must implement this method.")
    
    def delete(self):
        raise NotImplementedError("Sublcasses must implement this method")
    
    #Distruttore della classe
    def __del__(self):
        self.con.close()