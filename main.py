#!/usr/bin/python3

import os
from models.Database import DATABASE_NAME
import CreateDB as db_creator

if __name__ == '__main__':
    
    db_existed = os.path.exists(DATABASE_NAME)
    if not db_existed:
        db_creator.create_database()

# посмотреть табличку в приложении
#* sqlitebrowser test.s3db