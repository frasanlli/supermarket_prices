import pandas as pd
from datetime import datetime
from carrefour import Carrefour
from consum import Consum
from mercadona import Mercadona

class main_class():
    def __init__(self) -> None:
        self.hoy = datetime.now().strftime("%d_%m_%y")

    def consum_data(self):
        obj_supermercado_cs=Consum()
        data= obj_supermercado_cs.main()
        df = pd.DataFrame(data)
        df.to_csv(obj_supermercado_cs.nombre_csv)
        df.to_excel(obj_supermercado_cs.nombre_xlsx)
        obj_supermercado_cs.driver.close()

    def carrefour_data(self):
        obj_supermercado_cr=Carrefour()

        data = obj_supermercado_cr.main()
        df = pd.DataFrame(data)
        df.to_csv(obj_supermercado_cr.nombre_csv)
        df.to_excel(obj_supermercado_cr.nombre_xlsx)
        obj_supermercado_cr.driver.close()

    def mercadona_data(self):
        obj_supermercado_md=Mercadona()
        obj_supermercado_md.go_page()
        obj_supermercado_md.load_cookies("mercadona")

        try:
            botones_cookies=obj_supermercado_md.get_list_elements_by_attribute("button", "class", "ui-button ui-button--small ui-button--tertiary ui-button--positive")
            botones_cookies[0].click()
        except:
            pass
        try:
            obj_supermercado_md.fill_input("name", "postalCode", "46019")
            obj_supermercado_md.press_button("data-testid","postal-code-checker-button")
            obj_supermercado_md.wait_dissapear(obj_supermercado_md.get_element_by_attribute("div", "class", "modal__click-outside"))
        except:
            pass

        data:list = obj_supermercado_md.obtain_categories ("li")
        df=pd.DataFrame(data)
        df.to_csv('mercadona_'+self.hoy+'.csv')
        df.to_excel('mercadona_'+self.hoy+'.xlsx')
        obj_supermercado_md.save_cookies("mercadona")
        obj_supermercado_md.driver.close()

    def reducir_datos(self):
        df_total = []
        supermercados: list[str] = ["mercadona","carrefour","consum"]

        for supermercado in supermercados:
            df=pd.DataFrame(pd.read_csv(f"datos_csv//{supermercado}_{self.hoy}.csv", index_col=0))
            df_ordenar_precio = df.sort_values(by=['precio por cantidad(€/cantidad)'])

            filtro_productos: list[str] = df_ordenar_precio.drop_duplicates(subset=["producto"])
            df_total.append(filtro_productos)

        df_final = pd.concat(df_total)
        df_final.reset_index(drop=True, inplace=True)

        print(df_final)
        df_final.to_csv('datos_csv//supermercados_'+self.hoy+'.csv')
        df_final.to_excel('datos_excel//supermercados_'+self.hoy+'.xlsx')
        #df.to_csv('supermercados.csv')


    #MAIN
    def main(self):
        #self.mercadona_data()
        #self.carrefour_data()
        #self.consum_data()

        self.reducir_datos()


if __name__== "__main__":
    obj_main = main_class()
    obj_main.main()