import os
import threading
import time
import inspect
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime, timedelta
import pandas as pd
from database import Database
from log import Log
from carrefour import Carrefour
from mercadona import Mercadona
from consum import Consum

class main_class():
    def __init__(self) -> None:
        self.log = Log()
        self.obj_db: Database = Database()
        self.log.write_log("Program started", __file__, inspect.currentframe().f_lineno)
        self.today_file = datetime.now().strftime("%d_%m_%y")
        self.today = datetime.now().strftime("%d/%m/%Y, %H:%M")
        self.window_data: dict[str, list] = {
            "last execution":[],
            "last duration": [],
            "next execution": []
        }
        self.running_selenium: bool = False

    def create_label(self, my_frame: tk.Frame, text_value: str,
                     row_n: int, column_n: int, background: str=None)->tk.Label:
        label: tk.Label = tk.Label(master=my_frame, text=text_value,
                                    padx=10, pady=10, background=background)
        label.grid(sticky="NSEW", row=row_n, column=column_n)
        return label


    def create_button_thread(self, my_frame: tk.Frame, text_value: str,
                      action: str, row_n: int, column_n: int)->tk.Button:
        button: tk.Button = tk.Button(master=my_frame, text=text_value,
                                          cursor= "hand2",
                                          command=lambda: self.new_thread(action))
        button.grid(sticky="NSEW", row=row_n, column=column_n)
        return button


    def create_button_dialog(self, my_frame: tk.Frame, text_value: str,
                      action: str, row_n: int, column_n: int, label: tk.Label)->tk.Button:
        button: tk.Button = tk.Button(master=my_frame, text=text_value,
                                          cursor= "hand2",
                                          command=lambda: self.open_dialog(action, label))
        button.grid(sticky="NSEW", row=row_n, column=column_n)
        return button

    def delete_text(self, text_box: tk.Text):
        text_box.delete("1.0", "end")

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
        self.label_ex_all: tk.Label = self.create_label(run_frame, "dd/mm/YYYY", 1, 2)
        self.label_ex_mercadona: tk.Label = self.create_label(run_frame, "dd/mm/YYYY", 2, 2)
        self.label_ex_consum: tk.Label = self.create_label(run_frame, "dd/mm/YYYY", 3, 2)
        self.label_ex_carrefour: tk.Label = self.create_label(run_frame, "dd/mm/YYYY", 4, 2)

        #----------------COL3 Last duration
        self.label_du_all: tk.Label = self.create_label(run_frame, "-:--:--", 1, 3)
        self.label_du_mercadona: tk.Label = self.create_label(run_frame, "-:--:--", 2, 3)
        self.label_du_consum: tk.Label = self.create_label(run_frame, "-:--:--", 3, 3)
        self.label_du_carrefour: tk.Label = self.create_label(run_frame, "-:--:--", 4, 3)

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


    def frame_log(self, frame: tk.Frame)->None:
        row_span_val: int = 3
        frame.grid_rowconfigure([0, 2], weight=1, minsize=10)
        frame.grid_columnconfigure([1], weight=1, minsize=20)
        log_text = tk.Text(frame, height=10, state="disabled")
        log_text.grid(row=0, column=1, columnspan=2, sticky=tk.NSEW, rowspan=row_span_val)

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=log_text.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS, rowspan=row_span_val)
        log_text['yscrollcommand'] = scrollbar.set

        log_button: tk.Button = tk.Button(master=frame,
                                    text='Load log',
                                    cursor= "hand2",
                                    command= lambda: get_log(log_date_entry.get()))
        log_button.grid(column=0, row=0, padx=10, pady=10, sticky=tk.S)

        log_info_label: tk.Label = tk.Label(master=frame,
                                            text="Introduce a date with format dd-mm-yyyy.\n Example: 30-10-2024")
        log_info_label.grid(column=0, row=1, padx=10, pady=10)
        log_date_entry = ttk.Entry(frame)
        log_date_entry.grid(column=0, row=2, padx=10, pady=10, sticky=tk.N)

        def get_log(date: str)->None:
            text: str =""
            log_text.config(state="normal")
            self.delete_text(log_text)
            try:
                if date != "":
                    datetime.strptime(date, '%d-%m-%Y')
                text_log: list[str] = self.log.read_log(date)
                for text_line in text_log:
                    text+=text_line+"\n"
                log_text.insert('1.0', text)
                log_text.config(state="disabled")
            except Exception as e:
                self.log.write_log(f"Tried to load Log with no valid date format. \n {e}", __file__, inspect.currentframe().f_lineno)
                log_text.insert('1.0',"Date format not valid. Try dd-mm-yyyy")

    def frame_db(self, frame: tk.Frame)->None:
        row_span_val: int = 7
        frame.grid_rowconfigure([3], weight=1, minsize=10)
        frame.grid_columnconfigure([2], weight=1, minsize=20)

        self.create_label(frame, "Supermarket:", 0, 0)
        self.create_label(frame, "Product's category:", 1, 0)
        self.create_label(frame, "Product's name:", 2, 0)
        """self.create_label(frame, "Product's price:", 3, 0)
        self.create_label(frame, "Cheapest product:", 4, 0)"""
        results: tk.Label = self.create_label(frame, "", 4, 2)

        db_text = tk.Text(frame, height=10)
        db_text.grid(row=0, column=2, sticky=tk.NSEW, rowspan=row_span_val)
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=db_text.yview)
        scrollbar.grid(row=0, column=3, sticky=tk.NS, rowspan=row_span_val)
        db_text['yscrollcommand'] = scrollbar.set

        supermarket_ety = ttk.Entry(frame)
        supermarket_ety.grid(sticky="NSEW", column=1, row=0, padx=10, pady=10)
        product_g_ety = ttk.Entry(frame)
        product_g_ety.grid(sticky="NSEW", column=1, row=1, padx=10, pady=10)
        product_n_ety = ttk.Entry(frame)
        product_n_ety.grid(sticky="NSEW", column=1, row=2, padx=10, pady=10)
        """product_pz_ety = ttk.Entry(frame)
        product_pz_ety.grid(sticky="NSEW", column=1, row=3, padx=10, pady=10)
        product_min = ttk.Checkbutton(frame, onvalue=True, offvalue=False)
        product_min.grid(sticky="NSEW", column=1, row=4, padx=10, pady=10)"""

        def get_filters():
            search_list: list[str] = list()
            search_list.append(supermarket_ety.get())
            search_list.append(product_g_ety.get())
            search_list.append(product_n_ety.get())
            """search_list.append(product_pz_ety.get())
            search_list.append(product_min.cget("state"))"""
            get_product(search_list)

        search_product_btn: tk.Button = tk.Button(master=frame,
                                    text='Search product',
                                    cursor= "hand2",
                                    command= get_filters)
        search_product_btn.grid(row=6, column=0, columnspan=2, pady=20)

        def get_product(value_list: list[str]) -> None:
            #Need to add a load screen
            matches: int = 0
            db_text.config(state="normal")
            self.delete_text(db_text)
            try:
                #Need to get number of products in db to avoid errors
                for n in range(0, 45):
                    product: str = self.obj_db.get_db_filters(f"{n}", value_list)
                    if product:
                        db_text.insert('1.0', f"{product}\n\n")
                        matches+=1
                results.config(text=f"Matches found {matches}")
                db_text.config(state="disabled")
            except Exception as e:
                self.log.write_log(f"Tried to get value. \n {e}", __file__, inspect.currentframe().f_lineno)
                db_text.insert('1.0',"ERROR")

    def mainframe(self)->None:
        root: tk.Tk = tk.Tk(className="Supermarket's prices comparator")
        notebook: ttk.Notebook = ttk.Notebook(root)
        notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        run_frame: tk.Frame = tk.Frame(master=notebook)
        run_frame.pack(fill=tk.BOTH, expand=True)
        log_frame: tk.Frame = tk.Frame(master=notebook)
        log_frame.pack(fill=tk.BOTH, expand=True)
        db_frame: tk.Frame = tk.Frame(master=notebook)
        db_frame.pack(fill=tk.BOTH, expand=True)

        notebook.add(run_frame, text='Execution')
        notebook.add(log_frame, text='Check logs')
        notebook.add(db_frame, text='Search in database')

        self.frame_run(run_frame)
        self.frame_log(log_frame)
        self.frame_db(db_frame)

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
                #root.destroy()
                exit()
            elif result is False:
                #root.destroy()
                exit()
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()

    def check_current_time(self, time_wait: float)->None:
        today_time = datetime.now().strftime("%H:%M")
        # Obtain current time HH:MM:SS
        print(f"Current time: {today_time}")
        try:
            print(f"Next...{self.label_next_mercadona.cget("text")}")
        except Exception as e:
            self.log.write_log("Program closed", __file__, inspect.currentframe().f_lineno)
            self.log.write_log(f"Tried to get label value, but program is not running. \n {e}", __file__, inspect.currentframe().f_lineno)
            exit()
        if not self.running_selenium:
            if today_time in self.label_next_all.cget("text"):
                print("Run main")
                self.main()
            elif today_time in self.label_next_mercadona.cget("text"):
                print("Run Mercadona")
                self.mercadona_data()
            elif today_time in self.label_next_carrefour.cget("text"):
                self.carrefour_data()
            elif today_time in self.label_next_consum.cget("text"):
                print("Run Consum")
                self.consum_data()
        # Call function after 1000 miliseconds (60 seconds)
        time.sleep(time_wait)
        self.check_current_time(time_wait)

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
                self.log.write_log("Programmed execution time is not valid.", __file__, inspect.currentframe().f_lineno)
                return False

        root = tk.Tk(className=f"Program execution {option}")
        root.resizable(False, False)

        my_frame=tk.Frame(master=root)
        my_frame.pack()
        label_message: tk.Label = tk.Label(master=my_frame,
                                            text="Input format hh:mm.\n Example: 10:30",
                                            padx=10,
                                            pady=10)
        label_message.grid(sticky="NSEW", row=0, column=0, columnspan=2)
        entry_message: tk.Entry = tk.Entry(master=my_frame)
        entry_message.grid(sticky="NSEW", row=1, column=0)

        accept: tk.Button = tk.Button(master=my_frame,
                                    text='Accept',
                                    cursor= "hand2",
                                    command= check_input)
        accept.grid(sticky="NSEW", row=1,column=1)

        label_ad: tk.Label = tk.Label(master=my_frame,
                                        text="",
                                        padx=10,
                                        pady=10)
        label_ad.grid(sticky="NSEW", row=2,column=0, columnspan=2)


    def new_thread(self, function: str)->None:
        process_thread: threading.Thread = threading.Thread(target=None)
        if not self.running_selenium:
            if (function=="main"):
                process_thread = threading.Thread(target=self.main, name="main", daemon=True)
            elif (function=="mercadona_data"):
                process_thread = threading.Thread(target=self.mercadona_data, name="mercadona", daemon=True)
            elif (function=="consum_data"):
                process_thread = threading.Thread(target=self.consum_data, name="consum", daemon=True)
            elif (function=="carrefour_data"):
                process_thread = threading.Thread(target=self.carrefour_data, name="carrefour", daemon=True)
            process_thread.start()
            self.running_selenium = True

    def process_data(self, datos: list, obj_supermarket, label: tk.Label)->None:
        try:
            df = pd.DataFrame(datos)
            df.to_csv(obj_supermarket.name_csv)
            df.to_excel(obj_supermarket.name_xlsx)
        except Exception as e:
            label.config(text = "ERROR: Check log file")
            self.log.write_log(f"ERROR {e}", __file__, inspect.currentframe().f_lineno)

    def consum_data(self)->None:
        self.running_selenium = True
        try:
            starttime = time.perf_counter()
            self.label_st_consum.config(text = "Running..")
            self.label_ex_consum.config(text = self.today)
            obj_supermarket=Consum()
            obj_supermarket.main()
        except Exception as e:
            self.label_st_consum.config(text = "ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}", __file__, inspect.currentframe().f_lineno)
            obj_supermarket.obj_browser.driver.close()

        self.process_data(obj_supermarket.obj_basket.data, obj_supermarket, self.label_st_consum)
        #self.obj_db.update_csv_to_db(self.today_file, obj_supermarket.name_supermarket)
        self.log.write_log("RUNNING: process_data() Consum completed", __file__, inspect.currentframe().f_lineno)
        self.label_du_consum.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
        self.label_st_consum.config(text = "Off")
        self.running_selenium = False

    def carrefour_data(self)->None:
        self.running_selenium = True
        try:
            starttime = time.perf_counter()
            self.label_st_carrefour.config(text = "Running..")
            self.label_ex_carrefour.config(text = self.today)
            obj_supermarket=Carrefour()
            obj_supermarket.main()
        except Exception as e:
            self.label_st_carrefour.config(text = "ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}", __file__, inspect.currentframe().f_lineno)
            obj_supermarket.obj_browser.driver.close()

        self.process_data(obj_supermarket.obj_basket.data, obj_supermarket, self.label_st_carrefour)
        #self.obj_db.update_csv_to_db(self.today_file, obj_supermarket.name_supermarket)
        self.log.write_log("RUNNING: process_data() Carrefour completed", __file__, inspect.currentframe().f_lineno)
        self.label_du_carrefour.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
        self.label_st_carrefour.config(text = "Off")
        self.running_selenium = False

    def mercadona_data(self)->None:
        self.running_selenium = True
        try:
            starttime = time.perf_counter()
            self.label_st_mercadona.config(text = "Running..")
            self.label_ex_mercadona.config(text = self.today)
            obj_supermarket=Mercadona()
            obj_supermarket.main()
        except Exception as e:
            self.label_st_mercadona.config(text = "ERROR: Check log file")
            self.log.write_log(f"ERROR: {e}", __file__, inspect.currentframe().f_lineno)
            obj_supermarket.obj_browser.driver.close()

        self.process_data(obj_supermarket.obj_basket.data, obj_supermarket, self.label_st_mercadona)
        #self.obj_db.update_csv_to_db(self.today_file, obj_supermarket.name_supermarket)
        self.log.write_log("RUNNING: process_data() Mercadona completed", __file__, inspect.currentframe().f_lineno)
        self.label_du_mercadona.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
        self.label_st_mercadona.config(text = "Off")
        self.running_selenium = False

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
        self.label_st_all.config(text = "Running..")
        self.label_ex_all.config(text = self.today)
        self.mercadona_data()
        self.carrefour_data()
        self.consum_data()
        self.label_st_all.config(text = "Reducing data..")
        self.reduce_data()
        self.csv_a_json()
        self.label_du_all.config(text= (timedelta(seconds=time.perf_counter()-starttime)))
        self.label_st_all.config(text = "Off")

if __name__== "__main__":
    obj_main = main_class()
    main_thread = threading.Thread(target=obj_main.mainframe, name="wait", daemon=True)
    main_thread.start()
    time.sleep(3)
    wait_thread = threading.Thread(target=obj_main.check_current_time(60), name="wait", daemon=True)
    wait_thread.start()