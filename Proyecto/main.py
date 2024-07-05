import os
import pandas as pd
import threading
import time
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
from log import Log
from supermarket import Carrefour
from mercadona import Mercadona
from consum import Consum

import tkinter as tk

class main_class():
    def __init__(self) -> None:
        self.log = Log()
        self.log.write_log("Program started")
        self.today_file = datetime.now().strftime("%d_%m_%y")
        self.today = datetime.now().strftime("%d/%m/%Y, %H:%M")
        self.today_time = datetime.now().strftime("%H:%M")
        self.window_data: dict[str, list] = {
            "last execution":[],
            "last duration": [],
            "next execution": []
        }
        self.running: bool = True

    def create_label(self, my_frame: tk.Frame, text_value: str,
                     row_n: int, column_n: int, background: str=None)->tk.Label:
        label: tk.Label = tk.Label(master=my_frame, text=text_value,
                                    padx=10, pady=10, background=background)
        label.grid(row=row_n, column=column_n)
        return label


    def create_button_thread(self, my_frame: tk.Frame, text_value: str,
                      action: str, row_n: int, column_n: int)->tk.Button:
        button: tk.Button = tk.Button(master=my_frame, text=text_value,
                                          cursor= "hand2",
                                          command=lambda: self.new_thread(action))
        button.grid(row=row_n, column=column_n)
        return button


    def create_button_dialog(self, my_frame: tk.Frame, text_value: str,
                      action: str, row_n: int, column_n: int, label: tk.Label)->tk.Button:
        button: tk.Button = tk.Button(master=my_frame, text=text_value,
                                          cursor= "hand2",
                                          command=lambda: self.open_dialog(action, label))
        button.grid(row=row_n, column=column_n)
        return button


    def frame_run(self, run_frame: tk.Frame)->None:
        top_labels_text: list[str] = ["State", "Actions", "Last execution", "Last duration",
                                      "Program execution", "Next execution"]
        run_buttons_text: list[str] = ["Run all", "Run Mercadona", "Run Consum", "Run Carrefour"]
        run_buttons_actions: list[str] = ["main", "mercadona_data", "consum_data", "carrefour_data"]

        #----------------LABELS---------------
        for label_text in top_labels_text:
            self.create_label(run_frame, label_text, 0, top_labels_text.index(label_text), "Gray")

        #----------------COL0 State
        self.label_st_all: tk.Label = self.create_label(run_frame, "Off", 1, 0)
        self.label_st_mercadona: tk.Label = self.create_label(run_frame, "Off", 2, 0)
        self.label_st_consum: tk.Label = self.create_label(run_frame, "Off", 3, 0)
        self.label_st_carrefour: tk.Label = self.create_label(run_frame, "Off", 4, 0)

        #------COL1----------BUTTONS---------------
        for n in range(0, len(run_buttons_text)):
            self.create_button_thread(run_frame, run_buttons_text[n], run_buttons_actions[n], n+1, 1)

        #----------------COL2 Last execution
        self.label_ex_all: tk.Label = self.create_label(run_frame, "01/01/1970", 1, 2)
        self.label_ex_mercadona: tk.Label = self.create_label(run_frame, "01/01/1970", 2, 2)
        self.label_ex_consum: tk.Label = self.create_label(run_frame, "01/01/1970", 3, 2)
        self.label_ex_carrefour: tk.Label = self.create_label(run_frame, "01/01/1970", 4, 2)

        #----------------COL3 Last duration
        self.label_du_all: tk.Label = self.create_label(run_frame, "0:40:00", 1, 3)
        self.label_du_mercadona: tk.Label = self.create_label(run_frame, "0:40:00", 2, 3)
        self.label_du_consum: tk.Label = self.create_label(run_frame, "0:40:00", 3, 3)
        self.label_du_carrefour: tk.Label = self.create_label(run_frame, "0:40:00", 4, 3)

        #----------------COL5 next exe
        self.label_next_all: tk.Label = self.create_label(run_frame, "Not set", 1, 5)
        self.label_next_mercadona: tk.Label = self.create_label(run_frame, "Not set", 2, 5)
        self.label_next_consum: tk.Label = self.create_label(run_frame, "Not set", 3, 5)
        self.label_next_carrefour: tk.Label = self.create_label(run_frame, "Not set", 4, 5)

        #------COL4----------Button---------------
        entry_all: tk.Button = self.create_button_dialog(run_frame, 'Set schedule',
                                                         "main", 1, 4, self.label_next_all)
        entry_mercadona: tk.Button = self.create_button_dialog(run_frame, 'Set schedule',
                                                               "mercadona_data", 2, 4, self.label_next_mercadona)
        entry_consum: tk.Button = self.create_button_dialog(run_frame, 'Set schedule',
                                                               "consum_data", 3, 4, self.label_next_consum)
        entry_carrefour: tk.Button = self.create_button_dialog(run_frame, 'Set schedule',
                                                               "carrefour_data", 4, 4, self.label_next_carrefour)

        def read_saved_data()->None:
            if (os.path.exists("saved_data//window_data.json")):
                df=pd.DataFrame(pd.read_json("saved_data//window_data.json"))
                self.label_ex_all.config(text=df.iloc[0,0])
                self.label_ex_mercadona.config(text=df.iloc[1,0])
                self.label_ex_carrefour.config(text=df.iloc[2,0])
                self.label_ex_consum.config(text=df.iloc[3,0])

                self.label_du_all.config(text=df.iloc[0,1])
                self.label_du_mercadona.config(text=df.iloc[1,1])
                self.label_du_carrefour.config(text=df.iloc[2,1])
                self.label_du_consum.config(text=df.iloc[3,1])

                self.label_next_all.config(text=df.iloc[0,2])
                self.label_next_mercadona.config(text=df.iloc[1,2])
                self.label_next_carrefour.config(text=df.iloc[2,2])
                self.label_next_consum.config(text=df.iloc[3,2])
        read_saved_data()


    def frame_log(self, log_frame: tk.Frame)->None:
        log_label: tk.Label = self.create_label(log_frame, "", 0, 2)

        log_date_entry = ttk.Entry(log_frame)
        log_date_entry.grid(column=0, row=1, padx=10, pady=10)

        log_button: tk.Button = tk.Button(master=log_frame,
                                    text='Load log',
                                    cursor= "hand2",
                                    command= lambda: self.load_recent_log(log_label, log_date_entry.get()))
        log_button.grid(row=0, column=0)

    def load_recent_log(self, log_label: tk.Label, date: str)->None:
        try:
            if date != "":
                datetime.strptime(date, '%d-%m-%Y')
            text_log: list[str] = self.log.read_log(date)
            log_label.config(text = text_log)
        except:
            log_label.config(text = "Date format not valid. Try dd-mm-yyy")


    def mainframe(self)->None:
        root: tk.Tk = tk.Tk(className="Ejecutador mejores precios")
        notebook = ttk.Notebook(root)
        notebook.pack(pady=10, expand=True)

        run_frame: tk.Frame = tk.Frame(master=notebook)
        run_frame.pack()
        log_frame: tk.Frame = tk.Frame(master=notebook)
        log_frame.pack()
        options_frame: tk.Frame = tk.Frame(master=notebook)
        options_frame.pack()

        notebook.add(run_frame, text='Execution')
        notebook.add(log_frame, text='Last log')
        notebook.add(options_frame, text='Options')

        self.frame_run(run_frame)
        self.frame_log(log_frame)

        def on_closing()->None:
            result = messagebox.askyesnocancel("Quit", "Do you want to save window's data?")
            if result is True:
                self.window_data["last execution"].append(self.label_ex_all.cget("text"))
                self.window_data["last execution"].append(self.label_ex_mercadona.cget("text"))
                self.window_data["last execution"].append(self.label_ex_carrefour.cget("text"))
                self.window_data["last execution"].append(self.label_ex_consum.cget("text"))
                self.window_data["last duration"].append(self.label_du_all.cget("text"))
                self.window_data["last duration"].append(self.label_du_mercadona.cget("text"))
                self.window_data["last duration"].append(self.label_du_carrefour.cget("text"))
                self.window_data["last duration"].append(self.label_du_consum.cget("text"))
                self.window_data["next execution"].append(self.label_next_all.cget("text"))
                self.window_data["next execution"].append(self.label_next_mercadona.cget("text"))
                self.window_data["next execution"].append(self.label_next_carrefour.cget("text"))
                self.window_data["next execution"].append(self.label_next_consum.cget("text"))
                df=pd.DataFrame(self.window_data)
                df.to_json("saved_data//window_data.json")
                self.running = False
                #root.destroy()
                exit()
            elif result is False:
                self.running = False
                #root.destroy()
                exit()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    def check_current_time(self, time_wait: float)->None:
        # Obtain current time HH:MM:SS
        print(f"Current time: {self.today_time}")
        try:
            print(f"Next...{self.label_next_mercadona.cget("text")}")
        except:
            self.log.write_log("Program closed")
            #Exit in case root is destroyed
            exit()
        if self.today_time in self.label_next_all.cget("text"):
            print("Run main")
            self.main()
        elif self.today_time in self.label_next_mercadona.cget("text"):
            print("Run Mercadona")
            self.mercadona_data()
        elif self.today_time in self.label_next_carrefour.cget("text"):
            self.carrefour_data()
        elif self.today_time in self.label_next_consum.cget("text"):
            print("Run Consum")
            self.consum_data()
        # Call function after 1000 miliseconds (60 seconds)
        time.sleep(time_wait)

    def open_dialog(self, option: str, label_next: tk.Label)->None:

        def check_input()->None:
            print(entry_message.get())
            try:
                datetime.strptime(entry_message.get(), '%H:%M')
                if(option=="main"):
                    label_next.config(text = entry_message.get())
                    self.label_next_consum.config(text = "Auto")
                    self.label_next_carrefour.config(text = "Auto")
                    self.label_next_mercadona.config(text = "Auto")
                else:
                    if self.label_next_all['text'] != "Individual mode":
                        self.label_next_consum.config(text = "Not set")
                        self.label_next_carrefour.config(text = "Not set")
                        self.label_next_mercadona.config(text = "Not set")
                        self.label_next_all.config(text = "Individual mode")
                    label_next.config(text = entry_message.get())

                label_ad.config(text = "Execution set")
                return True

            except ValueError:
                label_ad.config(text = "Option not valid")
                return False

        root = tk.Tk(className=f"Program execution {option}")

        my_frame=tk.Frame(master=root)
        my_frame.pack()
        label_message: tk.Label = tk.Label(master=my_frame,
                                            text="Input format hh:mm.\n Example: 10:30",
                                            padx=10,
                                            pady=10)
        label_message.grid(row=0,column=0, columnspan=2)
        entry_message: tk.Entry = tk.Entry(master=my_frame)
        entry_message.grid(row=1,column=0)

        accept: tk.Button = tk.Button(master=my_frame,
                                    text='Accept',
                                    cursor= "hand2",
                                    command= check_input)
        accept.grid(row=1,column=1)

        label_ad: tk.Label = tk.Label(master=my_frame,
                                        text="",
                                        padx=10,
                                        pady=10)
        label_ad.grid(row=2,column=0, columnspan=2)


    def new_thread(self, function: str)->None:
        process_thread: threading.Thread = threading.Thread(target=None)
        if (function=="main"):
            process_thread = threading.Thread(target=self.main, name="main")
        elif (function=="mercadona_data"):
            process_thread = threading.Thread(target=self.mercadona_data, name="mercadona")
        elif (function=="consum_data"):
            process_thread = threading.Thread(target=self.consum_data, name="consum")
        elif (function=="carrefour_data"):
            process_thread = threading.Thread(target=self.carrefour_data, name="carrefour")
        process_thread.start()

    def process_data(self, datos: list, obj_supermarket)->None:
        df = pd.DataFrame(datos)
        df.to_csv(obj_supermarket.name_csv)
        df.to_excel(obj_supermarket.name_xlsx)


    def consum_data(self)->None:
        self.log.write_log("RUNNING: Consum")
        try:
            starttime = time.perf_counter()
            self.label_st_consum.config(text = "Running..")
            self.label_ex_consum.config(text = self.today)

            obj_supermarket=Consum()
            obj_supermarket.main()
            self.log.write_log("RUNNING: main() Consum completed")
            self.process_data(obj_supermarket.obj_basket.data, obj_supermarket)
            self.log.write_log("RUNNING: process_data() Consum completed")

            self.label_du_consum.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
            self.label_st_consum.config(text = "Off")
        except Exception as e:
            self.label_st_consum.config(text = f"ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}")
            obj_supermarket.obj_browser.driver.close()

    def carrefour_data(self)->None:
        self.log.write_log("RUNNING: Carrefour")
        try:
            starttime = time.perf_counter()
            self.label_st_carrefour.config(text = "Running..")
            self.label_ex_carrefour.config(text = self.today)

            obj_supermarket=Carrefour()
            obj_supermarket.main()
            self.log.write_log("RUNNING: main() Consum completed")
            self.process_data(obj_supermarket.obj_basket.data, obj_supermarket)
            self.log.write_log("RUNNING: process_data() Consum completed")

            self.label_du_carrefour.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
            self.label_st_carrefour.config(text = "Off")
        except Exception as e:
            self.label_st_consum.config(text = f"ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}")
            obj_supermarket.obj_browser.driver.close()

    def mercadona_data(self)->None:
        self.log.write_log(f"RUNNING: Mercadona")
        try:
            starttime = time.perf_counter()
            self.label_st_mercadona.config(text = "Running..")
            self.label_ex_mercadona.config(text = self.today)

            obj_supermarket=Mercadona()
            obj_supermarket.main()
            self.log.write_log("RUNNING: main() Consum completed")
            self.process_data(obj_supermarket.obj_basket.data, obj_supermarket)
            self.log.write_log("RUNNING: process_data() Consum completed")

            self.label_du_mercadona.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
            self.label_st_mercadona.config(text = "Complete")
        except Exception as e:
            self.label_st_consum.config(text = f"ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}")
            obj_supermarket.obj_browser.driver.close()

    def reduce_data(self)->None:
        df_total = []
        supermarkets: list[str] = ["mercadona","carrefour","consum"]
        for supermarket in supermarkets:
            df=pd.DataFrame(pd.read_csv(f"data_csv//{supermarket}_{self.today_file}.csv", index_col=0))
            df_order_prices = df.sort_values(by=["price per quantity(€/quantity)"])
            print(df_order_prices)
            filtro_productos: list[str] = df_order_prices.drop_duplicates(subset=["product"])
            df_total.append(filtro_productos)

        df_final = pd.concat(df_total)
        df_final.reset_index(drop=True, inplace=True)
        print(df_final)
        df_final.to_csv('data_csv//supermarkets_'+self.today_file+'.csv')
        df_final.to_excel('data_excel//supermarkets_'+self.today_file+'.xlsx')

    def csv_a_json(self)->None:
        df=pd.DataFrame(pd.read_csv(f"data_csv//supermarkets_{self.today_file}.csv", index_col=0))
        df.to_json("saved_data//supermarkets.json", orient="records")

    #MAIN
    def main(self)->None:
        starttime = time.perf_counter()
        # update text label
        self.label_st_all.config(text = "Running..")
        self.label_ex_all.config(text = self.today)

        self.mercadona_data()
        self.carrefour_data()
        self.consum_data()

        self.label_st_all.config(text = "Reducing data..")
        self.reduce_data()
        self.csv_a_json()

        self.label_du_all.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
        self.label_st_all.config(text = "Complete")

if __name__== "__main__":
    obj_main = main_class()
    main_thread = threading.Thread(target=obj_main.mainframe, name="wait")
    main_thread.start()
    time.sleep(3)
    while obj_main.running:
        wait_thread = threading.Thread(target=obj_main.check_current_time(60), name="wait")
        wait_thread.start()