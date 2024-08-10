import inspect
import os
import re
from abc import ABC, abstractmethod
import time
from log import Log
from basket import Basket
from browser import Browser
from product import Product

class Supermarket(ABC):

    @abstractmethod
    def __init__(self, postal_code:str = "46135")->None:
        self.obj_basket: Basket = Basket()
        self.obj_browser: Browser = Browser()
        self.log = Log()
        self.log.write_log(f"Supermarket {self.name_supermarket} running", __file__, inspect.currentframe().f_lineno)
        self.postal_code=postal_code
        self.name_csv: str = f'data_csv//{self.name_supermarket}_'+self.obj_basket.today+'.csv'
        self.name_xlsx: str = f'data_xlsx//{self.name_supermarket}_'+self.obj_basket.today+'.xlsx'
        self.page_values_xpath: str = "//div[@class='pagination__main']"
        self.errors: list[str] = list()

    @property
    @abstractmethod
    def name_supermarket(self):
        ...

    @property
    @abstractmethod
    def url(self):
        ...

    @property
    @abstractmethod
    def product_card_xpath(self):
        ...

    @property
    @abstractmethod
    def product_name_xpath(self):
        ...

    @property
    @abstractmethod
    def unitary_price_xpath(self):
        ...

    @property
    @abstractmethod
    def price_quantity_xpath(self):
        ...

    @abstractmethod
    def note_item_st_price(self, product_quantity_price: str):
        """Note product price/quantity"""

    @abstractmethod
    def note_item_unitary_price(self, unitary_price: str):
        """Note product unitary price"""

    def go_supermarket (self, timeout: float)->None:
        try:
            self.obj_browser.driver.maximize_window()
            self.obj_browser.driver.get(self.url)
            self.obj_browser.driver.implicitly_wait(timeout)
        except Exception as e:
            self.errors.append(f"ERROR SUPERMARKET: not possible to open {self.name_supermarket} in browser.\n Check computer connection and server status.")
            self.errors.append(e)
            self.obj_browser.driver.quit()

    def accept_cookies (self, xpath_tag: str, xpath_attribute: str, xpath_att_value: str):
        loaded: bool = self.obj_browser.load_cookies(self.name_supermarket)
        if not loaded:
            try:
                button = self.obj_browser.get_element_by_attribute(xpath_tag, xpath_attribute, xpath_att_value)
                button.click()
                time.sleep(3)
                #self.obj_browser.wait_dissapear(button, 1)
                self.obj_browser.save_cookies(self.name_supermarket)
            except Exception as e:
                self.errors.append(f"ERROR SUPERMARKET: Button could not be clicked. \n {e}")
                self.obj_browser.driver.close()
        else:
            self.obj_browser.driver.refresh()

    def check_product(self, real_name: str)->bool:
        value: bool = False
        for product in self.obj_basket.products_list:
            for key_word in product.key_words:
                if key_word in real_name:
                    value = True
                    for avoid_word in product.avoid_words:
                        if avoid_word in real_name:
                            value = False
                            break
            if value:
                return value
        return value

    def get_product(self, real_name: str)->bool:
        for product in self.obj_basket.products_list:
            for key_word in product.key_words:
                if key_word in real_name:
                    for subproduct in product.subproduct_words:
                        if subproduct in real_name:
                            return subproduct
                    return key_word

    def check_subproduct (self, product: Product, real_name: str)->str:
        for subproduct in product.subproduct_words:
            if subproduct in real_name:
                return subproduct
        return real_name

    def get_products_cards(self):
        return self.obj_browser.get_elements_by_xpath(self.product_card_xpath)

    def note_item_name(self, product_name: str)->None:
        """Note product real name"""
        print("NAME "+product_name)
        self.obj_basket.data["name"].append(product_name)

    def note_item_quantity(self, product_quantity_price: str, unitary_price: str)->None:
        """Note product quantity using price per quantity and unitary price"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall(r"\d+\.\d+",point_quantity_price)[0])
            unit_price_num = float(unitary_price[0])
            quantity = unit_price_num/quantity_price_num
            print("QUANTITY:"+str("%.2f" % quantity))
            self.obj_basket.data["quantity"].append("%.2f" % quantity)
        except Exception as e:
            self.errors.append(f"ERROR SUPERMARKET: not possible to note item quantity: {e}")

    def get_card_names(self)-> tuple:
        "Returns cards names"
        card_names: list[str] = list()
        card_upper_names: list[str] = list()
        webelements: list = self.obj_browser.get_elements_by_xpath(self.product_name_xpath)
        if webelements:
            for card in webelements:
                card_names.append(card.text.lower())
                card_upper_names.append(card.text)
            return card_names, card_upper_names

    def check_path(self):
        paths: list[str] = ["cookies", "data_csv", "data_xlsx", "logs", "saved_data"]
        for path in paths:
            if not os.path.isdir(path):
                print(f"Creating path {path}...")
                os.mkdir(path)
                print("Created")

    def check_web_error(self, url: str)->None:
        web_error: list[str] = ["Hemos tenido un error", "Service Unavailable",
                                "Todos los caminos llevan a Carrefour", "trabajando para solucionarlo"]
        check: bool = self.obj_browser.check_web_error(web_error)
        if check:
            self.obj_browser.driver.refresh()
            self.obj_browser.go_page(url, self.name_supermarket)