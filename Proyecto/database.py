from datetime import datetime
import os
import re
import firebase_admin
import pandas as pd
from firebase_admin import db, credentials

from _data import db_https
from log import Log

class Database():
    def __init__(self) -> None:
        self.log = Log()
        self.today_file = datetime.now().strftime("%d_%m_%y")
        self.cred: credentials.Certificate = credentials.Certificate(os.getcwd()+"\\credentials.json")
        firebase_admin.initialize_app(self.cred, {"databaseURL": db_https})

    def get_db(self, db_ref_n: str = "/", db_ref_key: str = "", value: str = "") -> str|None:
        try:
            ref = db.reference(db_ref_n+db_ref_key)
            if value.lower() == ref.get():
                return db.reference(db_ref_n).get()
            else:
                return None
        except Exception as e:
            self.log.write_log(f"DATABASE set error:\n {e}")

    def set_db(self, tag: str, update_val: any, db_ref: str = "/") -> None:
        try:
            db.reference(db_ref).set({tag : update_val})
            #self.log.write_log(f"File set:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE set error:\n {e}")

    def update_db(self, tag: str, update_val: any, db_ref: str = "/") -> None:
        try:
            ref = db.reference(db_ref)
            ref.update({tag : update_val})
            #self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE update error:\n {e}")

    def push_db(self, tag: str, update_val: any, db_ref: str = "/") -> None:
        try:
            db.reference(db_ref).push().set({tag : update_val})
            #self.log.write_log(f"File updated:{db.reference(db_ref).get()}")
        except Exception as e:
            self.log.write_log(f"DATABASE update error:\n {e}")

    def update_csv_to_db(self, file_date: str) -> None:
        df: pd.DataFrame = pd.read_csv(os.getcwd()+f"\\data_csv\\supermarkets_{file_date}.csv")
        for i in range(len(df)):
            self.update_db("name", (df.iloc[i])["name"], f"{i}")
            self.update_db("product", (df.iloc[i])["product"], f"{i}")
            self.update_db("unitary price(€)", (df.iloc[i])["unitary price(€)"], f"{i}")
            self.update_db("quantity", (df.iloc[i])["quantity"], f"{i}")
            self.update_db("price per quantity",(df.iloc[i])["price per quantity(€/quantity)"], f"{i}")
            self.update_db("supermarket", (df.iloc[i])["supermarket"], f"{i}")
            self.update_db("last update", file_date, f"{i}")

if __name__== "__main__":
    obj_db: Database = Database()
    obj_db.update_csv_to_db("07_06_24")
    print("END")