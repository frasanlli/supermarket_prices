import re
import time

from supermarket import Supermarket

class Consum(Supermarket):
    def __init__(self)->None:
        super().__init__()
        self.url_list: list[str]=["https://tienda.consum.es/es/c/frescos/2812?orderById=5&page=1",
                                  "https://tienda.consum.es/es/c/despensa/2811?orderById=5&page=1"]
        self.next_page_xpath: str = "//a[@class='next-page']"
        self.current_page_xpath: str = "//span[@id='paginator-dropdown-text']"
        self.last_page_xpath: str = "//div[@class='d-flex align-items-center mx-4']//span[2]"
        self.attribute_quantity_class: str = "widget-prod__info-unitprice ng-tns-c"

    @property
    def name_supermarket (self)->str:
        return "consum"

    @property
    def url (self)->str:
        return "https://tienda.consum.es/es#!Home"

    @property
    def product_card_xpath(self)->str:
        return "//cmp-widget-product"

    @property
    def product_name_xpath(self)->str:
        return self.product_card_xpath+"//a[@id='grid-widget--descr']"

    @property
    def unitary_price_xpath(self)->str:
        #In this supermarket could be discounts, actual price is //*//p[1]
        return "//span[@id='grid-widget--price']"

    @property
    def price_quantity_xpath(self)->str:
        return self._price_quantity_xpath

    @price_quantity_xpath.setter
    def price_quantity_xpath(self, value):
        self._price_quantity_xpath = value

    def fill_postal_code(self, postal_code: str):
        pass

    def get_product_card(self, product_name_card_text):#->WebElement:
        return self.obj_browser.get_element_parent(product_name_card_text, 3)

    def note_item_st_price(self, product_quantity_price: str)->None:
        """Note product price/quantity"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall(r"\d+\.\d+",point_quantity_price)[0])
            print("PRICE(€/quantity):"+str(quantity_price_num))
            self.obj_basket.data["price per quantity(€/quantity)"].append(quantity_price_num)
        except Exception as e:
            self.errors.append(f"ERROR CONSUM: not possible to note item's price/quantity\n {e}")

    def note_item_unitary_price(self, unitary_price: str)->None:
        """Note product unitary price"""
        try:
            unitary_price: str = unitary_price.replace(" €", "")
            unit_price_num: float = float(unitary_price.replace(",", "."))
            print("unitary price(€)"+str(unit_price_num))
            self.obj_basket.data["unitary price(€)"].append(unit_price_num)
        except Exception as e:
            self.errors.append(f"ERROR CONSUM: not possible to note item's unitary price\n {e}")

    def note_item_quantity(self, product_quantity_price: str, unitary_price: str)->None:
        """Note product quantity using price per quantity and unitary price"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall(r"\d+\.\d+",point_quantity_price)[0])
            unitary_price: str = unitary_price.replace(" €", "")
            unit_price_num: float = float(unitary_price.replace(",", "."))
            quantity = unit_price_num/quantity_price_num
            print("QUANTITY:"+str("%.2f" % quantity))
            self.obj_basket.data["quantity"].append("%.2f" % quantity)
        except Exception as e:
            self.errors.append(f"ERROR CONSUM: not possible to note item's unitary quanitity\n {e}")

    def change_quantity_price_class(self, card_class)->None:
        ending_value: list[str] = re.findall(r"\d+-\d+",card_class)
        attribute_class: str = self.attribute_quantity_class + ending_value[0]
        self.price_quantity_xpath = f"//div[@class='{attribute_class}']"

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
            card = self.get_product_card(products_upper_names[products_names.index(product_name_card)])
            if card:
                self.obj_basket.data["product"].append(self.get_product(product_name_card))
                print(f"PRODUCT_NAME: {product_name_card}")
                self.obj_basket.data["supermarket"].append(self.name_supermarket)
                card_class: str = card.get_attribute("class")
                self.change_quantity_price_class(card_class)
                card = self.obj_browser.get_element_by_attribute("div", "class", card_class)
                unitary_price = self.obj_browser.get_element_by_xpath(f"//div[@class='{card_class}']{self.unitary_price_xpath}").text

                product_quantity_price = self.obj_browser.get_element_by_xpath(f"//div[@class='{card_class}']{self.price_quantity_xpath}").text
                self.note_item_st_price(product_quantity_price)
                self.note_item_unitary_price(unitary_price)
                self.note_item_quantity(product_quantity_price, unitary_price)
        time.sleep(2)

    def press_next_page(self)->None:
        next_page: bool = True
        last_page_str: str = self.obj_browser.get_element_by_xpath(self.last_page_xpath).text
        last_page_str = last_page_str.replace('de ', '')
        last_page: int = int(last_page_str)
        while next_page:
            current_page_str: str = self.obj_browser.get_element_by_xpath(self.current_page_xpath).text
            current_page: int = int(current_page_str)
            self.obtain_data()
            if current_page != last_page:
                self.obj_browser.click_script("cmp-icon", "id", "paginator-dropdown-icon-right")
                time.sleep(2)
            else:
                next_page=False

    def main(self) -> None:
        self.go_supermarket(20)
        self.accept_cookies("button", "id", "onetrust-reject-all-handler")
        for url in self.url_list:
            self.obj_browser.go_page(url, self.name_supermarket)
            self.check_web_error(url)
            self.obj_browser.scroll_to_element("//cmp-icon[@id='paginator-dropdown-icon-right']")
            self.press_next_page()
        self.obj_browser.driver.close()
        self.log.write_log(self.errors)
        self.log.write_log(f"RUNNING: {self.name_supermarket}.main() completed")

if __name__== "__main__":
    obj_supermarket= Consum()
    obj_supermarket.check_path()
    obj_supermarket.main()