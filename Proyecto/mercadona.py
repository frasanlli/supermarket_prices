import random
import re
import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mozilla import Mozilla


class Mercadona(Mozilla):
    def __init__(self):
        super().__init__()
        self.nombre_super: str="mercadona"
        self.url: str= "https://tienda.mercadona.es/categories/"
        self.categories=r'category-menu__item'

        self.nombre_csv=f'datos_csv//{self.nombre_super}_'+self.hoy+'.csv'
        self.nombre_xlsx=f'datos_excel//{self.nombre_super}_'+self.hoy+'.xlsx'

    #Abrir página en navegador
    def go_page (self):
        try:
            self.driver.maximize_window()
            self.driver.get(self.url)
            self.driver.implicitly_wait(20)
            #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located("//div[@class='modal-content']"))

        except Exception as e:
            print(e)
            print(f"ERROR: not possible to open {self.nombre_super} in browser.\n Check computer connection and server status.")
            self.driver.quit()


    #obtener texto cantidad y precio/cantidad_estandar
    def get_item_quantity_and_stPrice(self, selected_text: list):
        product_quantity_prize_text= selected_text[1]
        product_quantity_stPrice_lines= re.split('[|]', product_quantity_prize_text)
        self.note_item_stPrice(product_quantity_stPrice_lines)
        self.note_item_quantity(product_quantity_stPrice_lines)


    #Anotar nombre del producto en la lista
    def note_item_name(self, selected_text: list, element_bl):
        product_name= selected_text[0]
        print(f"NOMBRE: {product_name}")
        self.data["nombre"].append(product_name)

        #filtro CLASIFICAR, Nombres coinciden pero hay subtipos
        if self.lista_mercadona[element_bl]["tipo_filtro"]==self.tipo_filtro[0]:
            for producto_simple in self.lista_mercadona[element_bl]["filtro"]:
                if (producto_simple in product_name):
                    self.data["producto"].append(f"{element_bl} {producto_simple}")
                    break
        elif self.lista_mercadona[element_bl]["tipo_filtro"]==self.tipo_filtro[2]:
            for producto_simple in self.lista_mercadona[element_bl]["filtro"]:
                if (producto_simple in product_name):
                    self.data["producto"].append(producto_simple)
                    break
        else:
            self.data["producto"].append(element_bl)


    #Anotar cantidad del producto en la lista
    def note_item_quantity(self, product_quantity_prize_lines: list):
        self.data["cantidad"].append(product_quantity_prize_lines[0])


    #Anotar precio/cantidad_estandar del producto en la lista
    def note_item_stPrice(self, product_quantity_prize: list):
        point_quantity_prize = product_quantity_prize[1].replace(",",".")
        product_quantity= re.findall(r"\d+\.\d+", point_quantity_prize)
        print(f"PRECIO/CANTIDAD(€/cantidad): {product_quantity}")
        self.data["precio por cantidad(€/cantidad)"].append(float(product_quantity[0]))


    #Anotar nombre del producto en la lista
    def note_item_unitary_prize(self, selected_text: list):
        point_unitary_price = selected_text[2].replace(",",".")
        point_unitary_price = re.split("€", point_unitary_price)
        if(len(point_unitary_price)>2):
            product_price= re.findall(r"\d+\.\d+", point_unitary_price[1])
        else:
            product_price= re.findall(r"\d+\.\d+", point_unitary_price[0])
        print(f"PRECIO UNDIAD(€): {product_price}")
        self.data["precio unitario(€)"].append(float(product_price[0]))


    #Filtro productos a clicar
    def get_item_list(self, element_bl):
        lista_filtrada: list=list()
        #comprobamos si la subcategoría tiene filtro o no (diccionario)
        #filtro CLASIFICAR, Nombres no deben coincidir con subtipos
        if self.lista_mercadona[element_bl]["tipo_filtro"]==self.tipo_filtro[0]:
            lista_filtrada=self.get_specific_list(element_bl, lista_filtrada)

        #filtro ELIMINAR, Nombres no deben coincidir con subtipos
        elif self.lista_mercadona[element_bl]["tipo_filtro"]==self.tipo_filtro[1]:
            for filtro in self.lista_mercadona[element_bl]["filtro"]:
                lista_filtrada=self.get_negated_list(filtro)

        #filtro SELECCIONAR, Nombres solo deben coincidir con subtipos
        elif self.lista_mercadona[element_bl]["tipo_filtro"]==self.tipo_filtro[2]:
            for filtro in self.lista_mercadona[element_bl]["filtro"]:
                lista_filtrada=self.get_specific_list(filtro, lista_filtrada)

        #sin filtro, entra todo
        else:
            lista_filtrada=self.get_complete_list()

        self.get_item(element_bl,lista_filtrada)


    #Abro celda de producto
    def get_item(self, element_bl, lista_filtrada: list):
        try:
            n=0
            for e in lista_filtrada:
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(e))
                e.click()
                product_web=self.get_element_by_attribute("div","data-testid","private-product-detail-info")
                product_text=product_web.text.lower()
                product_text_lines=re.split("\n", product_text)

                self.note_item_name(product_text_lines, element_bl)
                self.get_item_quantity_and_stPrice(product_text_lines)
                self.note_item_unitary_prize(product_text_lines)

                self.data["supermercado"].append(self.nombre_super)
                exit_button=self.get_element_by_attribute("button","class", "modal-content__close")
                exit_button.click()
                time.sleep(5)
                n+=1
                if(n== random.randrange(4, 6)):
                    time.sleep(5)
                    n=0
                #self.wait_dissapear(self.get_element_by_attribute("div", "class", "modal-content"))

        except Exception as e:
            print(e)
            print ("ERROR: list not found")

    #Obtener listado de todos productos
    def get_complete_list(self):
        xpath="//button[@class='product-cell__content-link']"
        try:
            filtered_list= list()
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            for e in list_of_elements:
                filtered_list.append(e)
            return filtered_list
        except Exception as e:
            print(e)
            print ("ERROR: list not found")

    #Obtener listado de productos filtrado
    def get_specific_list(self, filtro: str, filtered_list: list[str]):
        xpath="//button[@class='product-cell__content-link']"
        try:
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            for e in list_of_elements:
                product_text=e.text.lower()
                if filtro in product_text:
                    filtered_list.append(e)
            return filtered_list
        except Exception as e:
            print(e)
            print ("ERROR: list not found")

    #Obtener listado de productos filtrado
    def get_negated_list(self, filtro: str):
        xpath="//button[@class='product-cell__content-link']"
        try:
            filtered_list=[]
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            for e in list_of_elements:
                product_text=e.text.lower()
                if not filtro in product_text:
                    filtered_list.append(e)
            return filtered_list
        except Exception as e:
            print(e)
            print ("ERROR: list not found")


    #Obtener listado de categorías>subcategorías>elementos deseados
    def obtain_categories (self, locator_value)->list:
        try:
            #Obtenemos listado de categorias
            list_of_elements=self.get_list_elements_by_attribute(locator_value, "class", self.categories)

            #Recorremos listado de categorias, pulsando en cada una para ver subcategorias
            for e in list_of_elements:
                e.click()
                list_of_subcategories=self.get_list_elements_by_attribute("button", "class", "category-item__link")

                #Comprobamos si las subcategorías incluyen elementos de la cesta básica
                for subcat in list_of_subcategories:
                    print(subcat.text.lower())
                    for bl in self.lista_mercadona:
                        #Si las subcategorías incluyen elementos de la cesta, se abren clicando para pasar los elementos a CSS
                        if bl in subcat.text.lower() and "secos" not in subcat.text.lower():
                            subcat.click()
                            time.sleep(5)
                            self.get_item_list(bl)

            return self.data
        except Exception as e:
            print(e)
            print("ERROR: list of categories not found")
            self.driver.quit()

    def main(self) ->list:
        self.go_page()
        self.load_cookies(self.nombre_super)

        try:
            botones_cookies=self.get_list_elements_by_attribute("button", "class", "ui-button ui-button--small ui-button--tertiary ui-button--positive")
            botones_cookies[0].click()
        except:
            pass

        try:
            self.fill_input("name", "postalCode", "46019")
            self.press_button("data-testid","postal-code-checker-button")
            self.wait_dissapear(self.get_element_by_attribute("div", "class", "modal__click-outside"))
        except:
            pass

        data:list = self.obtain_categories ("li")
        return data


if __name__== "__main__":
    obj_supermercado=Mercadona()
    data = obj_supermercado.main()
    df=pd.DataFrame(data)
    df.to_csv(obj_supermercado.nombre_csv)
    df.to_excel(obj_supermercado.nombre_xlsx)
    obj_supermercado.save_cookies(obj_supermercado.nombre_super)
    obj_supermercado.driver.close()