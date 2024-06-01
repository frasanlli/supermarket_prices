import pandas as pd
from datetime import datetime
from carrefour import Carrefour
from consum import Consum
from mercadona import Mercadona
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class main_class():
    def __init__(self) -> None:
        self.hoy = datetime.now().strftime("%d_%m_%y")

    def consum_data(self):
        obj_navegador_cs=Consum()
        data= obj_navegador_cs.main()
        df = pd.DataFrame(data)
        df.to_csv(obj_navegador_cs.nombre_csv)
        df.to_excel(obj_navegador_cs.nombre_xlsx)
        obj_navegador_cs.driver.close()

    def carrefour_data(self):
        obj_navegador_cr=Carrefour()

        data = obj_navegador_cr.main()
        df = pd.DataFrame(data)
        df.to_csv(obj_navegador_cr.nombre_csv)
        df.to_excel(obj_navegador_cr.nombre_xlsx)
        obj_navegador_cr.driver.close()

    def mercadona_data(self):
        obj_navegador_md=Mercadona()
        obj_navegador_md.go_page()
        obj_navegador_md.load_cookies("mercadona")

        try:
            botones_cookies=obj_navegador_md.get_list_elements_by_attribute("button", "class", "ui-button ui-button--small ui-button--tertiary ui-button--positive")
            botones_cookies[0].click()
        except:
            pass
        try:
            obj_navegador_md.fill_input("name", "postalCode", "46019")
            obj_navegador_md.press_button("data-testid","postal-code-checker-button")
            obj_navegador_md.wait_dissapear(obj_navegador_md.get_element_by_attribute("div", "class", "modal__click-outside"))
        except:
            pass

        data:list = obj_navegador_md.obtain_categories ("li")
        df=pd.DataFrame(data)
        df.to_csv('mercadona'+self.hoy+'.csv')
        df.to_excel('mercadona'+self.hoy+'.xlsx')
        obj_navegador_md.save_cookies("mercadona")
        obj_navegador_md.driver.close()

    def reducir_datos(self):
        df_total = []
        supermercados: list[str] = ["mercadona","carrefour","consum"]

        for supermercado in supermercados:
            df=pd.DataFrame(pd.read_csv(f"{supermercado}{self.hoy}.csv", index_col=0))
            df_ordenar_precio = df.sort_values(by=['precio por cantidad(€/cantidad)'])

            filtro_productos: list[str] = df_ordenar_precio.drop_duplicates(subset=["producto"])
            df_total.append(filtro_productos)

        df_final = pd.concat(df_total)
        df_final.reset_index(drop=True, inplace=True)

        print(df_final)
        #df.to_csv('supermercados'+self.hoy+'.csv')
        df.to_csv('supermercados.csv')


    #MAIN
    #Mercadona
    def main(self):
        self.mercadona_data()
        self.carrefour_data()
        self.consum_data()

        self.reducir_datos()


if __name__== "__main__":
    obj_main = main_class()
    obj_main.main()