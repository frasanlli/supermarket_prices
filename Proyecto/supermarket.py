from abc import ABC, abstractmethod
import os
import random
import re
import time

from basket import Basket
from browser import Browser
from product import Product

class Supermarket(ABC):

    @abstractmethod
    def __init__(self, postal_code:str = "46135")->None:
        self.obj_basket: Basket = Basket()
        self.obj_browser: Browser = Browser()
        self.postal_code=postal_code
        self.name_csv: str = f'data_csv//{self.name_supermarket}_'+self.obj_basket.today+'.csv'
        self.name_xlsx: str = f'data_xlsx//{self.name_supermarket}_'+self.obj_basket.today+'.xlsx'
        self.page_values_xpath: str = "//div[@class='pagination__main']"

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
            #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located("//div[@class='modal-content']"))
        except Exception as e:
            print(e)
            print(f"ERROR: not possible to open {self.name_supermarket} in browser.\n Check computer connection and server status.")
            self.obj_browser.driver.quit()

    def accept_cookies (self, xpath_tag: str, xpath_attribute: str, xpath_att_value: str):
        loaded: bool = self.obj_browser.load_cookies(self.name_supermarket)
        if not loaded:
            try:
                button = self.obj_browser.get_element_by_attribute(xpath_tag, xpath_attribute, xpath_att_value)
                button.click()
                self.obj_browser.wait_dissapear(button, 1)
                self.obj_browser.save_cookies(self.name_supermarket)
            except Exception as e:
                print(f"Button could not be clicked. \n {e}")
                self.obj_browser.driver.close()

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
            print(e)
            #unit_price_num = float((re.findall(r"\d",point_unitary_price)[0]))


    def get_card_names(self)-> tuple:
        "Returns cards names"
        card_names: list[str] = list()
        card_upper_names: list[str] = list()
        webelements: list = self.obj_browser.get_elements_by_xpath(self.product_name_xpath)
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
        web_error: list[str] = ["Hemos tenido un error", "Service Unavailable"]
        check: bool = self.obj_browser.check_web_error(web_error)
        if check:
            self.obj_browser.driver.refresh()
            self.obj_browser.go_page(url, self.name_supermarket)

class Carrefour (Supermarket):
    def __init__(self)->None:
        super().__init__()
        self.url_list: list[str]=["https://www.carrefour.es/supermercado/productos-frescos/cat20002/c",
                                  "https://www.carrefour.es/supermercado/la-despensa/cat20001/c"]

    @property
    def name_supermarket (self)->str:
        return "carrefour"

    @property
    def url (self)->str:
        return "https://www.carrefour.es/supermercado"

    @property
    def product_card_xpath(self)->str:
        return "//ul[@class='product-card-list__list']//div[@class='product-card__parent']"

    @property
    def product_name_xpath(self)->str:
        return self.product_card_xpath+"//a[@class='product-card__title-link track-click']"

    @property
    def unitary_price_xpath(self)->str:
        #In this supermarket could be discounts, actual price is //*//p[1]
        return "//div[@class='product-card__price']"

    @property
    def price_quantity_xpath(self)->str:
        return "//span[@class='product-card__price-per-unit']"

    def fill_postal_code(self, postal_code: str)->None:
        pass

    def get_product_card(self, product_name: str):#->webElement:
        try:
            element = self.obj_browser.get_card_carrefour(self.product_card_xpath, product_name)
            if element:
                self.obj_basket.data["product"].append(self.get_product(product_name))
                print(f"PRODUCT_NAME: {product_name}")
            return element
        except:
            return None

    def note_item_quantity(self, product_quantity_price: str, unitary_price: str)->None:
        """Note product quantity using price per quantity and unitary price"""
        try:
            quantity_price_num = float(product_quantity_price)
            unit_price_num = float(unitary_price)
            quantity = unit_price_num/quantity_price_num
            print("QUANTITY:"+str("%.2f" % quantity))
            self.obj_basket.data["quantity"].append("%.2f" % quantity)
        except Exception as e:
            print(e)

    def note_item_st_price(self, product_quantity_price: str)->str:
        """Note product price/quantity"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall(r"\d+\.\d+",point_quantity_price)[0])
            print("PRICE(€/quantity):"+str(quantity_price_num))
            self.obj_basket.data["price per quantity(€/quantity)"].append(quantity_price_num)
            return str(quantity_price_num)
        except Exception as e:
            print(e)
            #quantity_price_num = float(re.findall(r"\d",point_quantity_price)[0])

    def note_item_unitary_price(self, unitary_price: str)->str:
        """Note product unitary price"""
        try:
            point_unit_price = unitary_price.replace(",",".")
            unit_price_num = float(re.findall(r"\d+\.\d+",point_unit_price)[0])
            print("unitary price(€)"+str(unit_price_num))
            self.obj_basket.data["unitary price(€)"].append(unit_price_num)
            return str(unit_price_num)
        except Exception as e:
            print(e)
            #unit_price_num = float((re.findall(r"\d",point_unitary_price)[0]))

    def check_current_page(self)->None:
        web: str = "https://www.carrefour.es/supermercado"
        current_web: str = self.obj_browser.driver.current_url
        if web == current_web:
            self.obj_browser.driver.back()

    def obtain_data(self)->None:
        products_names: list[str] = list()
        products_upper_initial: list[str] = list()
        products_upper_names: list[str] = list()
        unitary_price: str = ""
        product_quantity_price: str = ""
        products_names, products_upper_initial = self.get_card_names()
        products_names = list(filter(self.check_product, products_names))

        for e in products_upper_initial:
            if e.lower() in products_names:
                products_upper_names.append(e)

        for product_name_card in products_names:
            while True:
                card = self.get_product_card(products_upper_names[products_names.index(product_name_card)])
                if card:
                    break
            self.obj_basket.data["supermarket"].append(self.name_supermarket)
            unitary_price = card.get_attribute("app_price")
            product_quantity_price = card.get_attribute("app_price_per_unit")
            product_quantity_price = self.note_item_st_price(product_quantity_price)
            unitary_price = self.note_item_unitary_price(unitary_price)
            self.note_item_quantity(product_quantity_price, unitary_price)

    def press_next_page(self)->None:
        wait: float = 0
        next_page: bool = True
        while next_page:
            clicked: bool = False
            pages_text: str = self.obj_browser.get_element_by_xpath(self.page_values_xpath).text
            pages_text_list: list[str] = re.findall(r'\d+', pages_text)
            last_page: int = int(pages_text_list[1])
            current_page_str: str = pages_text_list[0]
            current_page: int = int(current_page_str)
            self.obtain_data()
            if current_page != last_page:
                wait = random.uniform(2.5, 3.6)
                for i in range(1, 3):
                    self.obj_browser.scroll_to_element("//span[@class='c-button__loader__container']")
                    clicked = self.obj_browser.press_element("span",
                                                            "class",
                                                            "pagination__next icon-right-arrow-thin")
                    if clicked:
                        break
                    elif not clicked and i==3:
                        print("error")
                time.sleep(wait)
                self.check_current_page()
                time.sleep(wait)
            else:
                next_page=False

    def main(self)->None:
        self.go_supermarket(20)
        self.accept_cookies("button", "id", "onetrust-reject-all-handler")
        self.obj_browser.click_script("span","class","icon-cross-thin")
        for url in self.url_list:
            self.obj_browser.go_page(url, self.name_supermarket)
            self.check_web_error(url)
            self.obj_browser.scroll_to_element("//span[@class='pagination__results-item']")
            self.obj_browser.scroll_to_element("//span[@class='pagination__next icon-right-arrow-thin']")
            self.press_next_page()
        self.obj_browser.driver.close()

if __name__== "__main__":
    obj_supermarket = Carrefour()
    obj_supermarket.check_path()
    obj_supermarket.main()
    exit()