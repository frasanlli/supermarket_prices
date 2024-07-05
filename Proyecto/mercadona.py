import re
import time

from supermarket import Supermarket

class Mercadona (Supermarket):
    def __init__(self):
        super().__init__()

    @property
    def name_supermarket (self)->str:
        return "mercadona"

    @property
    def url (self)->str:
        return "https://tienda.mercadona.es/categories/"

    @property
    def product_card_xpath(self)->str:
        return "//button[@class='product-cell__content-link']"

    @property
    def product_name_xpath(self)->str:
        return "//h4[@class='subhead1-r product-cell__description-name']"

    @property
    def unitary_price_xpath(self)->str:
        #In this supermarket could be discounts, actual price is //*//p[1]
        return "//div[@class='product-price']//p"

    @property
    def price_quantity_xpath(self)->str:
        return "//div[@class='product-format product-format__size']//span[1]"

    def fill_postal_code(self, postal_code: str):
        try:
            self.obj_browser.fill_input("name", "postalCode", postal_code)
            button = self.obj_browser.get_element_by_attribute("button", "data-testid", "postal-code-checker-button")
            button.click()
            self.obj_browser.wait_dissapear(button, 1)
        except:
            print("Cookies loaded. Step not necessary")
            pass

    def get_product_card(self, product_name_card):
        self.obj_browser.press_element_parent(product_name_card)

    def obtain_data(self):
        products_names: list[str] = list()
        products_upper_initial: list[str] = list()
        products_upper_names: list[str] = list()
        products_names, products_upper_initial = self.get_card_names()
        products_names = list(filter(self.check_product, products_names))

        for e in products_upper_initial:
            if e.lower() in products_names:
                products_upper_names.append(e)

        for product_name_card in products_names:
            #print(products_names)
            #print(products_upper_names)
            self.get_product_card(products_upper_names[products_names.index(product_name_card)])
            product_web = self.obj_browser.get_element_by_attribute("div","data-testid","private-product-detail-info")

            if product_web is not None:
                self.obj_basket.data["product"].append(self.get_product(product_name_card))
                product_text = product_web.text.lower()
                product_text_lines =re.split("\n", product_text)
                self.note_item_name(product_text_lines[0])

                point_unitary_price = product_text_lines[2].replace(",",".")
                point_unitary_price = re.split("€", point_unitary_price)
                if(len(point_unitary_price)>2):
                    point_unitary_price = re.split("€", point_unitary_price[1])
                else:
                    point_unitary_price = re.split("€", point_unitary_price[0])
                self.note_item_unitary_price(point_unitary_price[0])

                product_quantity_prize_text= product_text_lines[1]
                product_quantity_st_price_lines= re.split('[|]', product_quantity_prize_text)
                self.note_item_quantity(product_quantity_st_price_lines[1], point_unitary_price)
                self.note_item_st_price(product_quantity_st_price_lines[1])
                self.obj_basket.data["supermarket"].append(self.name_supermarket)

                exit_button=self.obj_browser.get_element_by_attribute("button","class", "modal-content__close")
                time.sleep(1)
                exit_button.click()

                time.sleep(3)

    def open_subcategory_products(self):
        list_of_categories = self.obj_browser.get_elements_by_attribute("li", "class", "category-menu__item")
        for category in list_of_categories:
            category.click()
            list_of_subcategories=self.obj_browser.get_elements_by_attribute("button", "class", "category-item__link")
            for subcategory in list_of_subcategories:
                subcategory.click()
                self.obtain_data()


    def note_item_st_price(self, product_quantity_price: str):
        """Note product price/quantity"""
        try:
            point_quantity_price = product_quantity_price.replace(",",".")
            quantity_price_num = float(re.findall("\d+\.\d+",point_quantity_price)[0])
            print("PRICE(€/quantity):"+str(quantity_price_num))
            self.obj_basket.data["price per quantity(€/quantity)"].append(quantity_price_num)
        except Exception as e:
            print(e)
            #quantity_price_num = float(re.findall("\d",point_quantity_price)[0])


    def note_item_unitary_price(self, unitary_price: str):
        """Note product unitary price"""
        try:
            unit_price_num = float(unitary_price.replace(" ", ""))
            self.obj_basket.data["unitary price(€)"].append(unit_price_num)
        except Exception as e:
            print(e)
            #unit_price_num = float((re.findall("\d",point_unitary_price)[0]))


    def main(self):
        self.go_supermarket(20)
        self.fill_postal_code(self.postal_code)
        self.accept_cookies("button", "class", "ui-button ui-button--small ui-button--tertiary ui-button--positive")
        self.open_subcategory_products()

        self.obj_browser.driver.close()

if __name__== "__main__":
    obj_supermarket=Mercadona()
    obj_supermarket.check_path()
    obj_supermarket.main()