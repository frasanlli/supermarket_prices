import pandas as pd
from datetime import datetime
from carrefour import Carrefour
from consum import Consum
from mercadona import Mercadona

class main_class():
    def __init__(self) -> None:
        self.hoy = datetime.now().strftime("%d_%m_%y")


    def procesar_datos(datos: list, obj_supermercado):
        df = pd.DataFrame(datos)
        df.to_csv(obj_supermercado.nombre_csv)
        df.to_excel(obj_supermercado.nombre_xlsx)


    def consum_data(self):
        obj_supermercado=Consum()
        datos_brutos= obj_supermercado.main()
        self.procesar_datos(datos_brutos, obj_supermercado)
        obj_supermercado.driver.close()


    def carrefour_data(self):
        obj_supermercado=Carrefour()
        datos_brutos= obj_supermercado.main()
        self.procesar_datos(datos_brutos, obj_supermercado)
        obj_supermercado.driver.close()


    def mercadona_data(self):
        obj_supermercado=Mercadona()
        datos_brutos= obj_supermercado.main()
        self.procesar_datos(datos_brutos, obj_supermercado)
        obj_supermercado.driver.close()


    def reducir_datos(self):
        df_total = []
        supermercados: list[str] = ["mercadona","carrefour","consum"]

        for supermercado in supermercados:
            df=pd.DataFrame(pd.read_csv(f"datos_csv//{supermercado}_{self.hoy}.csv", index_col=0))
            df_ordenar_precio = df.sort_values(by=['precio por cantidad(€/cantidad)'])

            print(df_ordenar_precio)

            filtro_productos: list[str] = df_ordenar_precio.drop_duplicates(subset=["producto"])
            df_total.append(filtro_productos)

        df_final = pd.concat(df_total)
        df_final.reset_index(drop=True, inplace=True)

        print(df_final)
        df_final.to_csv('datos_csv//supermercados_'+self.hoy+'.csv')
        df_final.to_excel('datos_excel//supermercados_'+self.hoy+'.xlsx')
        self.csv_a_json()


    def csv_a_json(self):
        df=pd.DataFrame(pd.read_csv(f"datos_csv//supermercados_{self.hoy}.csv", index_col=0))
        df.to_json("supermercados.json")


    #MAIN
    def main(self):
        self.mercadona_data()
        self.carrefour_data()
        self.consum_data()

        self.reducir_datos()
        self.csv_a_json()

if __name__== "__main__":
    obj_main = main_class()
    obj_main.main()