import re
import time

import pandas as pd
from selenium.webdriver.common.by import By

from browser import Browser
from basket import Basket

class Carrefour(Browser):
    def __init__(self):
        super().__init__()

        self.obj_cesta: Basket = Basket()
        self.nombre_super: str="carrefour"
        self.url: str= "https://www.carrefour.es/supermercado"

        self.xpath_product_card: str = "//div[@class='plp-food-view__list']"
        #self.xpath_product_card: str = "//div[@class='product-card__detail']"
        self.xpath_precio_unitario: str = self.xpath_product_card+"//div[@class='product-card__prices']"
        self.xpath_precio_cantidad: str = self.xpath_product_card+"//span[@class='product-card__price-per-unit']"
        self.xpath_nombre_producto: str = self.xpath_product_card+"//a[@class='product-card__title-link track-click']"

        self.url_list: list[str]=["https://www.carrefour.es/supermercado/productos-frescos/frutas/cat220006/c",
                                  "https://www.carrefour.es/supermercado/productos-frescos/frutas/manzanas-y-peras/cat220010/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/alimentacion/aceites-y-vinagres/cat20066/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/alimentacion/aceites-y-vinagres/cat20066/c?sort=active_price_pum%20asc&offset=24",
                                  "https://www.carrefour.es/supermercado/la-despensa/alimentacion/arroz-y-cous-cous/cat20068/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/alimentacion/harinas-y-levaduras/cat20070/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/alimentacion/legumbres/cat20071/c",
                                  "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/cat220014/c",
                                  "https://www.carrefour.es/supermercado/productos-frescos/verduras-y-hortalizas/hortalizas/cat220019/c",
                                  "https://www.carrefour.es/supermercado/productos-frescos/quesos/cat20020/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/lacteos/cat20011/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/huevos/cat20021/c"]
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
        #self.click_script("span", "class", "icon-cross-thin")

        for url in self.url_list:
            self.navegar(url)

            web_error = self.get_one_element_by_text("Hemos tenido un error")
            web_error_2 = self.get_one_element_by_text("Service Unavailable")
            if web_error or web_error_2:
                self.driver.refresh()
                self.navegar(url)
                time.sleep(5)

            self.press_button("class", "c-button sort-options__button c-button--tone-monochrome c-button--variation-secondary c-button--size-s")
            self.click_script_preciokilo("button", "class", "c-link sort-options__list__item__link c-link--size-m c-link--tone-monochrome")
            self.scroll_to_element()
            self.scroll_to_element()

            elementos_nombre = self.driver.find_elements(By.XPATH, self.xpath_nombre_producto)
            elementos_precio_cantidad = self.driver.find_elements(By.XPATH, self.xpath_precio_cantidad)
            lista_precio_unitario = self.precio_unitario_carrefour(self.xpath_precio_unitario)
            #elementos_precio_unitario = self.driver.find_elements(By.XPATH, self.xpath_precio_unitario)

            self.obtener_datos(elementos_nombre, elementos_precio_cantidad, lista_precio_unitario)

        return self.data


    def obtener_datos(self, elementos_nombre, elementos_precio_cantidad, lista_precio_unitario):
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
                        for producto_evitar in self.obj_cesta.lista_evitar:
                            if producto_evitar in nombre:
                                break
                        if basic_producto in nombre:
                            seleccionado = True
                            print("PRODUCTO: "+basic_producto)
                            self.data["producto"].append(basic_producto)
                            self.note_item_name(nombre)
                            self.data["supermercado"].append(self.nombre_super)

                    if seleccionado:
                        precio_cantidad: str = elementos_precio_cantidad[contador].text
                        self.note_item_stPrice(precio_cantidad)

                        precio_unitario: str = lista_precio_unitario[contador]
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
            point_quantity_prize = product_quantity_prize.replace(",",".")
            quantity_prize_num = float(re.findall("\d+\.\d+",point_quantity_prize)[0])
        except:
            quantity_prize_num = float(re.findall("\d",point_quantity_prize)[0])

        try:
            point_unitary_prize = unitary_prize.replace(",",".")
            unit_prize_num = float((re.findall("\d+\.\d+",point_unitary_prize)[0]))
        except:
            unit_prize_num = float((re.findall("\d",point_unitary_prize)[0]))

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
        print("PRECIO UNDIAD(€):"+str(unit_prize_num))
        self.data["precio unitario(€)"].append(unit_prize_num)


if __name__== "__main__":
    obj_supermercado= Carrefour()
    data = obj_supermercado.main()
    df = pd.DataFrame(data)
    df.to_csv(obj_supermercado.nombre_csv)
    df.to_excel(obj_supermercado.nombre_xlsx)
    obj_supermercado.save_cookies(obj_supermercado.nombre_super)
    print (data)