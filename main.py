import asyncio
import orjson as json
from scripts.webServer import WebServer
from scripts.cypher import Cipher
from scripts.database import Database
from scripts.logger import Logger
from pathlib import Path

SERVER_SETTINGS = json.loads(open('./settings.json', 'r').read())

def main():
    for directory in SERVER_SETTINGS['DIRECTORIES']:
        Path(directory).mkdir(parents=True, exist_ok=True)

    logger = Logger('logger', datetime_format=SERVER_SETTINGS['DATETIME_FORMAT'])
    Database(SERVER_SETTINGS['DATABASE_PATHS']['users'], 'users', logger).create_table(
        'users', {
            'id': 'TEXT NOT NULL PRIMARY KEY UNIQUE',
            'email': 'TEXT NOT NULL UNIQUE',
            'password_hash': 'TEXT NOT NULL',
            'token': 'TEXT NOT NULL',
            'register_date': 'TEXT NOT NULL',
            'password_change_date': 'TEXT NOT NULL',
            'public_key': 'TEXT NOT NULL',
            'verified': 'BOOLEAN NOT NULL',
            'verification_code': 'TEXT'
        }
    )

    cipher = Cipher(SERVER_SETTINGS['SEPARATOR'], False)
    cipher.generate_keys(SERVER_SETTINGS['KEY_LENGTH'])

    def start_asyncio():
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_forever()
    
    ws = WebServer(cipher=cipher, logger=logger)
    ws.run(port=SERVER_SETTINGS['HTTP_PORT'])
    start_asyncio()

if __name__ == "__main__":
    main()
