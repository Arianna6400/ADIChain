from models.model_base import Model

class Credentials(Model):
    """
    This class represents the Credentials model that stores user authentication and authorization information,
    extending the functionality provided by the Model class.
    """

    def __init__(self, id, username, hash_password, role, public_key, private_key):
        """
        Initializes a new instance of Credentials with the provided user details.
        
        Parameters:
        - id: Unique identifier for the credentials record
        - username: Username associated with the credentials
        - hash_password: Hashed password for user authentication
        - role: The role assigned to the user (e.g., admin, user, etc.)
        - public_key: The public key associated with the user
        - private_key: The private key associated with the user; kept secure and private
        """
        super().__init__()
        self.id = id
        self.username = username
        self.hash_password = hash_password
        self.role = role
        self.public_key = public_key
        self.private_key = private_key

    # Getter methods for each attribute
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

    def save(self):
        """
        Saves a new or updates an existing Credentials record in the database.
        Implements SQL queries to insert or update credentials based on the presence of an ID.
        """
        if self.id is None:
            # Insert new credentials record
            self.cur.execute('''INSERT INTO Credentials (username, hash_password, role, public_key, private_key)
                                VALUES (?, ?, ?, ?, ?)''', (self.username, self.hash_password, self.role, self.public_key, self.private_key)) 
                                #I punti interrogativi come placeholder servono per la prevenzione di attacchi SQL Injection
        else:
            # Update existing credentials record
            self.cur.execute('''UPDATE Credentials SET username=?, hash_password=?, role=?, public_key=?, private_key=? WHERE id=?''',
                             (self.username, self.hash_password, self.role, self.public_key, self.private_key, self.id))
        self.conn.commit()
        self.id = self.cur.lastrowid # Update the ID with the last row inserted ID if new record

    def delete(self):
        """
        Deletes a Credentials record from the database based on its ID.
        """
        if self.id is not None:
            self.cur.execute('DELETE FROM Credentials WHERE id=?', (self.id,))
            self.conn.commit()
