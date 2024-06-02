import json
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

from cesta import Cesta

class Mozilla(Cesta):
    def __init__(self):
        super().__init__()
        options = webdriver.FirefoxOptions()
        #options.add_argument("-headless")
        self.data = {
            "producto":[],
            "nombre": [],
            "precio unitario(€)": [],
            "cantidad": [],
            "precio por cantidad(€/cantidad)":[],
            "supermercado":[]
            }

        self.driver=webdriver.Firefox(options=options)

    def find_inside_element (self, webelement, xpath):
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(webelement.find_element(By.XPATH, xpath)))
        return webelement.find_element(By.XPATH, xpath)

    def find_inside_element_nombre (self, webelement, xpath):
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(webelement.find_element(By.XPATH, xpath)))
        elements=webelement.find_elements(By.XPATH, xpath)
        for element in elements:
            if element.text == "Precio por kilo":
                return element

    #Abrir página en navegador
    def go_page (self, url: str, supermarket_name: str):
        try:
            self.driver.maximize_window()
            self.driver.get(url)
            self.driver.implicitly_wait(20)
            #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located("//div[@class='modal-content']"))

        except Exception as e:
            print(e)
            print("ERROR: not possible to open "+ supermarket_name + " in browser.\n Check computer connection and server status.")
            self.driver.quit()


    #Obtener lista empleando contenido que muestra como texto
    def get_elements_by_text (self, text_content: str)->list:
        xpath="//*[contains(text(),"+text_content+"')]"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            return list_of_elements

        except Exception as e:
            print(e)
            print("ERROR: element not found by its text")
            #self.driver.quit()

    def get_elements_by_xpath (self, xpath: str)->str:
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            return list_of_elements

        except Exception as e:
            print(e)
            print("ERROR: elements not found")
            #self.driver.quit()

    def get_element_text_by_xpath (self, xpath: str)->str:
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element=self.driver.find_element(By.XPATH, xpath)
            return element.text()

        except Exception as e:
            print(e)
            print("ERROR: element not found")
            #self.driver.quit()

    #Obtener WebElement empleando contenido que muestra como texto
    def get_one_element_by_text (self, text_content: str):
        xpath=f"//*[contains(text(),'{text_content}')]"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element=self.driver.find_element(By.XPATH, xpath)
            return element

        except Exception as e:
            print(e)
            print("ERROR: element not found by its text")
            #self.driver.quit()


    #Obtener lista WebElement empleando datos del elemento
    def get_list_elements_by_attribute (self, locator_value: str, attribute: str, attribute_content: str):
        #VARIABLES
        list_final=[]
        xpath="//"+locator_value

        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            list_of_elements=self.driver.find_elements(By.XPATH, xpath)
            for e in list_of_elements:
                if attribute_content in e.get_attribute(attribute):
                    list_final.append(e)

            return list_final

        except Exception as e:
            print(e)
            print("ERROR: element not found by its attribute")


    #Obtener WebElement empleando datos del elemento
    def get_element_by_attribute (self, locator_value: str, attribute: str, attribute_content: str):
        #VARIABLES
        xpath="//"+locator_value+"[@"+attribute+"='"+attribute_content+"']"

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element=self.driver.find_element(By.XPATH, xpath)

            return element

        except Exception as e:
            print(e)
            print("ERROR: element not found by its attribute")

    def click_script_preciokilo(self, tag: str, attribute: str, attribute_content: str):
        xpath=f"//{tag}[@{attribute}='{attribute_content}']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button = self.get_one_element_by_text("Precio por kilo")
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    def click_script(self, tag: str, attribute: str, attribute_content: str):
        xpath=f"//{tag}[@{attribute}='{attribute_content}']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button = self.driver.find_element(xpath)
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    #Presionar botón
    def press_button (self, attribute: str, attribute_content: str):
        xpath="//button[@"+attribute+"='"+attribute_content+"']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button=self.driver.find_element(By.XPATH, xpath)
            button.click()
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    def press_element (self, element: str, attribute: str, attribute_content: str):
        xpath=f"//{element}[@{attribute}='{attribute_content}']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button=self.driver.find_element(By.XPATH, xpath)
            button.click()
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    #Presionar href
    def press_href(self, link_value: str):
        xpath="//a[@href='"+link_value+"']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            link= self.driver.find_element(By.XPATH, xpath)
            link.click()
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    #Intrododucir datos en campo
    def fill_input (self, attribute: str, attribute_value: str, input_text: str):
        xpath="//input[@"+attribute+"='"+attribute_value+"']"
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
        try:
            input_element= self.driver.find_element(By.XPATH, xpath)
            input_element.clear()
            input_element.send_keys(input_text)
        except Exception as e:
            print(e)
            print ("ERROR: search element not found")


    def wait_dissapear(self, element_web):
        try:
            WebDriverWait(self.driver, 1).until_not(EC.element_to_be_clickable(element_web))
        except:
            pass

    def save_cookies(self, fichero: str):
        try:
            Path(f'cookies//{fichero}_cookies.json').write_text(
                json.dumps(self.driver.get_cookies(), indent=2)
            )
        except:
            pass

    #https://heykush.hashnode.dev/add-cookies-in-selenium
    def load_cookies(self, fichero: str):
        try:
            with open(f'cookies//{fichero}_cookies.json', 'r') as f:
                cookies = json.load(f) #stoting cookies
                for cookie in cookies:
                    #set the sameSite attribute to 'Strict' to avoid the error
                    if 'sameSite' in cookie:
                        cookie['sameSite'] = 'Strict'
                    self.driver.add_cookie(cookie) #add the cookies
            self.driver.refresh()
            time.sleep(10) # add wait to load the cookies
        except Exception as e:
            pass

    def scroll_bottom(self):
        self.driver.execute_script("window.scrollTo(100,document.body.scrollHeight);")
        time.sleep(10)

    def precio_unitario_carrefour(self, xpath_precio_unitario: str)->list[str]:
        xpath = xpath_precio_unitario+"//span"
        lista_precios: list[str] = []
        master_precio = self.driver.find_elements(By.XPATH, xpath)

        for precio in master_precio:
            if (precio.get_attribute("class") == "product-card__price--current"):
                lista_precios.append(precio.text)
            elif (precio.get_attribute("class") == "product-card__price"):
                lista_precios.append(precio.text)

        return lista_precios


