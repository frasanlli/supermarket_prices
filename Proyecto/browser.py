import json
import logging
import os
import random
import time

from pathlib import Path

"""from webdriver_manager.core.utils import read_version_from_cmd
from webdriver_manager.core.os_manager import PATTERN"""

from selenium.webdriver.firefox.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement

class Browser():
    def __init__(self)->None:
        #For some reason now it is not detecting the driver's path, so it is necessary to add it
        DRIVER_PATH = r"C:\Program Files (x86)\Drivers\geckodriver.exe"
        service: webdriver.FirefoxService = Service(executable_path=DRIVER_PATH)
        options: webdriver.FirefoxOptions = webdriver.FirefoxOptions()
        #options.add_argument("-headless")
        self.driver: webdriver.Firefox = webdriver.Firefox(service=service,
                                                           options=options)

    def find_inside_element (self, webelement, xpath: str) -> WebElement|None:
        #Returns WebElement's son
        #WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(webelement.find_element(By.XPATH, xpath)))
        element: WebElement|None = webelement.find_element(By.XPATH, xpath)
        return element


    def find_inside_element_text (self, webelement, xpath: str, text_input: str) -> WebElement|None:
        #Returns WebElement's son that contains specific text
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(webelement.find_element(By.XPATH, xpath)))
        elements=webelement.find_elements(By.XPATH, xpath)
        for element in elements:
            if element.text == text_input:
                return element

    def go_page (self, url: str, supermarket_name: str)->None:
        #Driver opens url
        wait: float = random.uniform(4, 6)
        try:
            self.driver.maximize_window()
            self.driver.get(url)
            self.driver.implicitly_wait(wait)
            #WebDriverWait(self.driver, 60).until(EC.presence_of_element_located("//div[@class='modal-content']"))

        except Exception as e:
            print(e)
            print("ERROR: not possible to open "+ supermarket_name + " in browser.\n Check computer connection and server status.")
            self.driver.quit()

    #Obtener lista empleando contenido que muestra como texto
    def get_elements_by_text (self, text_content: str)->list[WebElement]|None:
        #Returns
        xpath="//*[contains(text(),'"+text_content+"')]"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            list_of_elements: list[WebElement]|None = self.driver.find_elements(By.XPATH, xpath)
            return list_of_elements

        except Exception as e:
            print(e)
            print("ERROR: element not found by its text")
            #self.driver.quit()

    def get_element_by_xpath (self, xpath: str)-> WebElement|None:
        #Returns first WebElement found by its xpath
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            return element

        except Exception as e:
            print(e)
            print("ERROR: elements not found")
            #self.driver.quit()

    def get_elements_by_xpath (self, xpath: str)->list[WebElement]|None:
        #Returns a list of WebElements using an xpath
        try:
            #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            WebDriverWait(self.driver, 20).until(EC.visibility_of_all_elements_located((By.XPATH, xpath)))
            list_of_elements: list[WebElement]|None = self.driver.find_elements(By.XPATH, xpath)
            return list_of_elements

        except Exception as e:
            print(e)
            print("ERROR: elements not found")
            #self.driver.quit()

    def get_element_text_by_xpath (self, xpath: str)->str:
        #Returns first WebElement text content found using its xpath
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            return element.text()

        except Exception as e:
            print(e)
            print("ERROR: element not found")
            #self.driver.quit()

    def check_web_error (self, text_content: list[str])->bool:
        #Checks if error appears after loading website
        for text in text_content:
            xpath=f"//*[contains(text(),'{text}')]"
            try:
                WebDriverWait(self.driver, 1).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
                element: WebElement|None = self.driver.find_element(By.XPATH, xpath)
                if element:
                    return True
            except Exception as e:
                pass
        return False

    def get_one_element_by_text (self, text_content: str) -> WebElement|None :
        #Returns first WebElement found using its text content
        xpath=f"//*[contains(text(),'{text_content}')]"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element: WebElement|None =self.driver.find_element(By.XPATH, xpath)
            return element

        except Exception as e:
            print(e)
            print("ERROR: element not found by its text")
            #self.driver.quit()

    def get_elements_by_attribute (self,
                                   locator_value: str,
                                   attribute: str,
                                   attribute_content: str) -> list[WebElement]|None:
        #Returns list of WebElements using attribute and attribute content
        list_final: list[WebElement]|None = []
        xpath: str = "//"+locator_value

        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            list_of_elements: list[WebElement]|None = self.driver.find_elements(By.XPATH, xpath)
            for e in list_of_elements:
                if attribute_content in e.get_attribute(attribute):
                    list_final.append(e)

            return list_final

        except Exception as e:
            print(e)
            print("ERROR: element not found by its attribute")

    def press_element_parent(self, text_son: str)-> None:
        #Click over clickable WebElement's parent
        go_father: str = "//.."
        for i in range(1, 5):
            xpath: str = f'//*[contains(text(),"{text_son}")]{go_father*i}'
            try:
                self.driver.find_element(By.XPATH, xpath).click()
                break
            except Exception as e:
                print(e)
                print("Minor Error: element not clickable, trying next")

    def get_element_parent(self, text_son: str, ancestor_n: int, tag: str = "*")-> WebElement|None:
        #Returns WebElement's ancestor
        go_father: str = "//.."*ancestor_n
        xpath: str = f'//{tag}[contains(text(),"{text_son}")]{go_father}'
        try:
            WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            return self.driver.find_element(By.XPATH, xpath)
        except Exception as e:
            print(e)
            print("Minor Error: element not clickable, trying next")

    def get_card_carrefour(self, xpath_parent: str, text_son: str)-> WebElement|None:
        #Returns WebElement's ancestor limited to 22 characters (text_son)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath_parent)))
            elements_text = self.driver.find_elements(By.XPATH, xpath_parent)
            for e in elements_text:
                if text_son in e.text:
                    return e
            return None
        except Exception as e:
            print(e)
            print("Minor Error: element not clickable, trying next")

    def get_element_by_attribute (self, locator_value: str, attribute: str, attribute_content: str)-> WebElement|None:
        #Returns first WebElement found using tag+attribute+attribute_value
        xpath="//"+locator_value+"[@"+attribute+"='"+attribute_content+"']"

        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element: WebElement|None =self.driver.find_element(By.XPATH, xpath)
            return element

        except Exception as e:
            print(e)
            print("ERROR: element not found by its attribute")

    def click_script_preciokilo(self, tag: str, attribute: str, attribute_content: str)->None:
        xpath: str = f"//{tag}[@{attribute}='{attribute_content}']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button: WebElement|None = self.get_one_element_by_text("Precio por kilo")
            self.driver.execute_script("arguments[0].click();", button)
            self.driver.implicitly_wait(1.5)
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    def click_script(self, tag: str, attribute: str, attribute_content: str)->None:
        #Clicks webelement using javascript
        xpath: str = f"//{tag}[@{attribute}='{attribute_content}']"
        if (attribute==""):
            xpath=f"//{tag}"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].click();", button)
        except Exception as e:
            print(e)
            print("ERROR: not clicked")

    def press_button (self, attribute: str, attribute_content: str)->None:
        #Press button tag
        xpath: str = "//button[@"+attribute+"='"+attribute_content+"']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            button.click()
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    def press_element (self, element: str, attribute: str, attribute_content: str)->bool:
        #Click first WebElement found using tag+attribute+attribute_value
        xpath: str = f"//{element}[@{attribute}='{attribute_content}']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            button: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            button.click()
            return True
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")
            return False

    def press_href(self, link_value: str)->None:
        #Click link contained in a href attribute
        xpath: str = "//a[@href='"+link_value+"']"
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            link: WebElement|None= self.driver.find_element(By.XPATH, xpath)
            link.click()
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")

    def fill_input (self, attribute: str, attribute_value: str, input_text: str)->None:
        #Introduce data in an input tag
        xpath: str = "//input[@"+attribute+"='"+attribute_value+"']"
        WebDriverWait(self.driver, 60).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
        try:
            input_element: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            input_element.clear()
            input_element.send_keys(input_text)
        except Exception as e:
            print(e)
            print ("ERROR: search element not found")

    def wait_dissapear(self, element_web: WebElement|None, wait_time: int)->None:
        #Wait WebElement to dissapear
        n: int = 0
        while True or n<5:
            try:
                WebDriverWait(self.driver, wait_time).until_not(EC.element_to_be_clickable(element_web))
                break
            finally:
                n+=1

    def save_cookies(self, file_name: str) -> None:
        path_value: Path = Path(f'cookies//{file_name}_cookies.json')
        try:
            path_value.write_text(
                json.dumps(self.driver.get_cookies(), indent=2)
            )
        except Exception as e:
            print(f"Cookies could not be saved \n {e}")
            pass

    #https://heykush.hashnode.dev/add-cookies-in-selenium
    def load_cookies(self, file_name: str) -> bool:
        wait: float = random.uniform(8, 11)
        if (os.path.exists('cookies//{file_name}_cookies.json')):
            try:
                with open(f'cookies//{file_name}_cookies.json', 'r') as f:
                    cookies = json.load(f) #stoting cookies
                    for cookie in cookies:
                        #set the sameSite attribute to 'Strict' to avoid the error
                        if 'sameSite' in cookie:
                            cookie['sameSite'] = 'Strict'
                        self.driver.add_cookie(cookie) #add the cookies
                self.driver.refresh()
                time.sleep(wait) # add wait to load the cookies
                return True
            except Exception as e:
                print(f"Cookies could not be loaded \n {e}")
        return False

    def scroll_to_element(self, xpath)->None:
        """Scrolls bar to WebElement if exists"""
        wait: float = random.uniform(2.5, 3.5)
        try:
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.driver.find_element(By.XPATH, xpath)))
            element: WebElement|None = self.driver.find_element(By.XPATH, xpath)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            time.sleep(wait)
        except Exception as e:
            print(e)
            print("ERROR: button not clicked")
