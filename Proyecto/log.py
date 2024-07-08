from datetime import datetime
import os

class Log():
    def __init__(self) -> None:
        self.now: datetime = datetime.now().strftime('%d-%m-%Y')
        self.doc_name: str = f"logs//log_{self.now}.txt"
        if not os.path.exists(self.doc_name):
            open(self.doc_name, "w")

    def get_time_now(self)->datetime:
        return datetime.now().strftime("%d-%m-%Y, [%H:%M] : ")

    def write_log(self, text: str) -> None:
        f = open(self.doc_name, "a")
        final_text: str = f"{self.get_time_now()} {text}"
        f.write(final_text+"\n")
        f.close()

    def read_log(self, date: str)->list[str]:
        try:
            if not date:
                with open(self.doc_name) as f:
                    lines: list[str] = f.readlines()
            else:
                with open(f"logs//log_{date}.txt") as f:
                    lines: list[str] = f.readlines()
            f.close()
            return lines
        except:
            return ["Log with date: "+date+" does not exist"]
