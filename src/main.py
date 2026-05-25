import os
import sys
from database import Database
from api import API

def main():
    # Initialize database connection
    db = Database()

    # Initialize API
    api = API(db)

    # Start API server
    api.start()

if __name__ == "__main__":
    main()
