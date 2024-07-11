import os
import firebase_admin
from firebase_admin import db, credentials

from _data import db_https
from log import Log

class Database():
    def __init__(self) -> None:
        self.log = Log()
        cred: credentials.Certificate = credentials.Certificate(os.getcwd()+"\\credentials.json")
        firebase_admin.initialize_app(cred, {"databaseUrl": db_https})
        ref = db.reference("\\")
        ref.get()

    def get_db(self, db_ref: str = "\\") -> None:
        try:
            self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE set error:\n {e}")

    def set_db(self, update_val: any, db_ref: str = "\\") -> None:
        try:
            db.reference(db_ref).set(update_val)
            self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE set error:\n {e}")

    def update_db(self, tag: str, update_val: any, db_ref: str = "\\") -> None:
        try:
            db.reference(db_ref).update({f"{tag}: {update_val}"})
            self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE update error:\n {e}")

    def push_db(self, tag: str, update_val: any, db_ref: str) -> None:
        if (db_ref !="\\"):
            try:
                db.reference(db_ref).push().set({f"{tag}: {update_val}"})
                self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
            except Exception as e:
                self.log.write_log(f"DATABASE update error:\n {e}")


if __name__== "__main__":
    obj_db: Database = Database()

    print("END")