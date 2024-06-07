import re
import time

import pandas as pd
from selenium.webdriver.common.by import By

from mozilla import Mozilla
from cesta import Cesta

class Consum(Mozilla):
    def __init__(self):
        super().__init__()
        self.nombre_super: str="consum"
        self.url: str= "https://tienda.consum.es/es#!Home"
        self.obj_cesta: Cesta = Cesta()

        self.xpath_product_card: str = ""#"//div[@class='d-flex flex-column flex-grow-1 w-100 widget-prod__body ng-tns-c233-11']"
        self.xpath_precio_unitario: str = self.xpath_product_card+"//span[@id='grid-widget--price']"
        self.xpath_precio_cantidad: str = self.xpath_product_card+"//p[@id='grid-widget--unitprice']"
        self.xpath_nombre_producto: str = self.xpath_product_card+"//a[@id='grid-widget--descr']"

        self.url_list: list[str]=["https://tienda.consum.es/es/c/despensa/lacteos-huevos/mantequilla-margarina/2094?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/lacteos-huevos/huevos/2065?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/arroz-pastas-legumbres/pastas/1659?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/conservas-aceites-y-condimentos/aceite-vinagre/1526?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/conservas-aceites-y-condimentos/aceite-vinagre/1526?orderById=11&page=2",
                                  "https://tienda.consum.es/es/c/despensa/arroz-pastas-legumbres/arroz/1640?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/frescos/frutas/2179?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/frescos/verduras/2187?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/arroz-pastas-legumbres/legumbres-secas/1649?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/harina-levadura-pan-rallado/1646?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/frescos/verduras/pepino-pimiento/2211?orderById=11&page=1",
                                  "https://tienda.consum.es/es/c/despensa/lacteos-huevos/mantequilla-margarina/2094?orderById=11&page=1"]
        self.nombre_csv=f'datos_csv//{self.nombre_super}_'+self.obj_cesta.hoy+'.csv'
        self.nombre_xlsx=f'datos_excel//{self.nombre_super}_'+self.obj_cesta.hoy+'.xlsx'

    #Abrir página en navegador
    def go_page (self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            self.driver.implicitly_wait(20)
            #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located("//div[@class='modal-content']"))

        except Exception as e:
            print(e)
            print("ERROR: not possible to open "+ self.nombre_super + " in browser.\n Check computer connection and server status.")
            self.driver.quit()

    def navegar(self, url):
        self.driver.get(url)

    def main(self)->list:
        self.go_page()
        self.load_cookies(self.nombre_super)

        try:
            self.press_button("id", "onetrust-reject-all-handler")
        except:
            pass

        for url in self.url_list:
            self.navegar(url)

            web_error = self.get_one_element_by_text("Hemos tenido un error")
            web_error_2 = self.get_one_element_by_text("Service Unavailable")
            if web_error or web_error_2:
                self.driver.refresh()
                self.navegar(url)
                time.sleep(5)

            #self.driver.find_element(By.CLASS_NAME, "grid__order form-control dropdown-toggle a-btn-dropdown u-rounded u-form--hide-icon ng-tns-c312-142 ng-pristine ng-valid ng-touched").click()
            #time.sleep(1)
            #self.get_elements_by_text("Más barato primero (precio/kilo)").click()
            self.scroll_bottom()
            self.scroll_bottom()

            elementos_nombre = self.driver.find_elements(By.XPATH, self.xpath_nombre_producto)
            elementos_precio_cantidad = self.driver.find_elements(By.XPATH, self.xpath_precio_cantidad)
            lista_precios_cantidad: list[str]= []
            for elemento_precio_cantidad in elementos_precio_cantidad:
                if elemento_precio_cantidad.text != "" :
                    lista_precios_cantidad.append(elemento_precio_cantidad.text)
            #lista_precio_unitario = self.precio_unitario_carrefour(self.xpath_precio_unitario)
            elementos_precio_unitario = self.driver.find_elements(By.XPATH, self.xpath_precio_unitario)

            self.obtener_datos(elementos_nombre, lista_precios_cantidad, elementos_precio_unitario)

        return self.data


    def obtener_datos(self, elementos_nombre, lista_precios_cantidad, elementos_precio_unitario):
        contador: int = -1
        for producto_nombre in elementos_nombre:
            seleccionado: bool = False
            evitar: bool = False
            nombre: str = producto_nombre.text.lower()

            if nombre != "":
                contador+=1
                for producto_evitar in self.obj_cesta.lista_evitar:
                    if producto_evitar in nombre:
                        evitar = True

                if not evitar:
                    #for basic_producto in self.basic_list:
                    for basic_producto in self.obj_cesta.lista_todos:
                        if basic_producto in nombre:
                            seleccionado = True
                            print("PRODUCTO "+basic_producto)
                            self.data["producto"].append(basic_producto)
                            self.note_item_name(nombre)
                            self.data["supermercado"].append(self.nombre_super)

                    if seleccionado:
                        precio_cantidad: str = lista_precios_cantidad[contador]
                        self.note_item_stPrice(precio_cantidad)

                        precio_unitario: str = elementos_precio_unitario[contador].text
                        self.note_item_unitary_prize(precio_unitario)
                        self.note_item_quantity(precio_cantidad, precio_unitario)
        time.sleep(2)

    #Anotar nombre del producto
    def note_item_name(self, selected_text: str):
        product_name= selected_text
        print("NOMBRE "+product_name)
        self.data["nombre"].append(product_name)


    #Anotar cantidad del producto
    def note_item_quantity(self, product_quantity_prize: str, unitary_prize: str):
        try:
            quantity_prize_num = float((re.findall("\d+\,\d+",product_quantity_prize)[0]).replace(",","."))
        except:
            quantity_prize_num = float((re.findall("\d",product_quantity_prize)[0]).replace(",","."))

        try:
            unit_prize_num = float((re.findall("\d+\,\d+",unitary_prize)[0]).replace(",","."))
        except:
            unit_prize_num = float((re.findall("\d",unitary_prize)[0]).replace(",","."))

        cantidad = unit_prize_num/quantity_prize_num
        print("CANTIDAD:"+str("%.2f" % cantidad))
        self.data["cantidad"].append("%.2f" % cantidad)


    #Anotar precio/cantidad_estandar del producto
    def note_item_stPrice(self, product_quantity_prize: str):
        try:
            point_quantity_prize = product_quantity_prize.replace(",",".")
            quantity_prize_num = float(re.findall("\d+\.\d+",point_quantity_prize)[0])
        except:
            quantity_prize_num = float(re.findall("\d",point_quantity_prize)[0])
        print("PRECIO(€/cantidad):"+str(quantity_prize_num))
        self.data["precio por cantidad(€/cantidad)"].append(quantity_prize_num)

    #Anotar nombre del producto
    def note_item_unitary_prize(self, unitary_prize: str):
        try:
            point_unitary_prize = unitary_prize.replace(",",".")
            unit_prize_num = float((re.findall("\d+\.\d+",point_unitary_prize)[0]))
        except:
            unit_prize_num = float((re.findall("\d",point_unitary_prize)[0]))
        print("PRECIO UNDIDAD(€):"+str(unit_prize_num))
        self.data["precio unitario(€)"].append(unit_prize_num)


if __name__== "__main__":
    obj_supermercado= Consum()
    data = obj_supermercado.main()
    df = pd.DataFrame(data)
    df.to_csv(obj_supermercado.nombre_csv)
    df.to_excel(obj_supermercado.nombre_xlsx)
    obj_supermercado.save_cookies(obj_supermercado.nombre_super)
    obj_supermercado.driver.close()
    print(data)