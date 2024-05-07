"""This module defines the base Model class used to interact with the database."""

import sqlite3
from config import config

class Model:
    """Base model to be extended for implementing other models."""
    db_path = "ADIChain"

    def __init__(self):
        """Constructor that initializes the database connection."""
        self.conn = sqlite3.connect(config.config["db_path"])
        self.cur = self.conn.cursor()

    def save(self):
        """Virtual method to save the model. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method.")
    
    def delete(self):
        """Virtual method to delete the model. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement this method")
    
    def __del__(self):
        """Destructor that closes the database connection."""
        self.conn.close()
