from datetime import datetime, timedelta

class Log():
    def __init__(self) -> None:
        self.now: datetime = datetime.now().strftime('%d-%m-%Y')
        open(f"logs//log_{self.now}.txt", "w")

    def get_time_now(self)->datetime:
        return datetime.now().strftime("%d-%m-%Y, [%H:%M] : ")

    def write_log(self, text: str):
        f = open(f"logs//log_{self.now}.txt", "a")
        final_text: str = f"{self.get_time_now()} {text}"
        f.write(final_text+"\n")
        f.close()

    def read_log(self, date: str)->list[str]:
        try:
            if not date:
                with open(f"logs//log_{self.now}.txt") as f:
                    lines: list[str] = f.readlines()
            else:
                with open(f"logs//log_{date}.txt") as f:
                    lines: list[str] = f.readlines()
            f.close()
            return lines
        except:
            return ["Log with date: "+date+" does not exist"]
