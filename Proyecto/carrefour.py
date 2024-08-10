import random
import re
import time
import inspect

from supermarket import Supermarket

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
        except Exception as e:
            self.errors.append(f"CARREFOUR: not possible to get product card {product_name}:\n {e}")
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
            self.errors.append(f"ERROR CARREFOUR: not possible to note item's quantity\n {e}")

    def note_item_st_price(self, product_quantity_price: str)->str:
        """Note product price/quantity"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall(r"\d+\.\d+",point_quantity_price)[0])
            print("PRICE(€/quantity):"+str(quantity_price_num))
            self.obj_basket.data["price per quantity(€/quantity)"].append(quantity_price_num)
            return str(quantity_price_num)
        except Exception as e:
            self.errors.append(f"ERROR CARREFOUR: not possible to note item's price/quantity\n {e}")

    def note_item_unitary_price(self, unitary_price: str)->str:
        """Note product unitary price"""
        try:
            point_unit_price = unitary_price.replace(",",".")
            unit_price_num = float(re.findall(r"\d+\.\d+",point_unit_price)[0])
            print("unitary price(€)"+str(unit_price_num))
            self.obj_basket.data["unitary price(€)"].append(unit_price_num)
            return str(unit_price_num)
        except Exception as e:
            self.errors.append(f"ERROR CARREFOUR: not possible to note item's unitary price \n {e}")

    def check_current_page(self, used_url: str)->None:
        web: str = "https://www.carrefour.es/supermercado"
        current_web: str = self.obj_browser.driver.current_url
        if web == current_web:
            self.obj_browser.driver.back()
            self.obj_browser.scroll_to_element("//span[@class='c-button__loader__container']")
            self.obj_browser.scroll_to_element("//span[@class='c-button__loader__container']")
            self.obj_browser.press_element("span",
                                            "class",
                                            "pagination__next icon-right-arrow-thin")
            current_web = self.obj_browser.driver.current_url

        if current_web == used_url:
            text_url: list[str] = used_url.split("category&offset=")
            page_num: int = int(re.findall(r"\d+",used_url)[-1]) + 24
            self.obj_browser.go_page(text_url[0]+ "category&offset=" + str(page_num),
                                    self.name_supermarket)
        if "la-despensa" in current_web:
            print(current_web)
        time.sleep(random.uniform(3, 5))
        print(current_web)

    def obtain_data(self)->None:
        products_names: list[str] = list()
        products_upper_initial: list[str] = list()
        products_upper_names: list[str] = list()
        unitary_price: str = ""
        product_quantity_price: str = ""
        products_names, products_upper_initial = self.get_card_names()
        products_names = list(filter(self.check_product, products_names))
        if products_names:
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

    def press_next_page(self)->str:
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
                used_page: str = self.obj_browser.driver.current_url
                self.obj_browser.scroll_to_element("//span[@class='c-button__loader__container']")
                clicked = self.obj_browser.press_element("span",
                                                        "class",
                                                        "pagination__next icon-right-arrow-thin")
                if clicked:
                    self.check_current_page(used_page)
                else:
                    exit()
                time.sleep(wait)
                self.check_web_error(used_page)
            else:
                next_page=False

    def main(self) -> None:
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
        self.log.write_log(self.errors, __file__, inspect.currentframe().f_lineno)
        self.log.write_log(f"RUNNING, {self.name_supermarket}.main() completed", __file__, inspect.currentframe().f_lineno)

if __name__== "__main__":
    obj_supermarket = Carrefour()
    obj_supermarket.check_path()
    obj_supermarket.main()
    exit()