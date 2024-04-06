import time
import re
import pandas as pd
import selenium as sl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

mercadona = {
    "name": "Mercadona",
    "url" : "https://tienda.mercadona.es/"
}
carrefour= {
    "name": "Carrefour",
    "url" : "https://www.carrefour.es/supermercado"
}
consum= {
    "name": "Consum",
    "url" : "https://tienda.consum.es/es#!Home"
}

listColumns=["mercadona", "carrefour", "consum"]
listRows=["precio(€)", "precio por kg(€/kg)", "nombre"]
obtainedInfo=[]
df1 = pd.DataFrame(obtainedInfo, index=listRows, columns=listColumns)
d = pd.DataFrame()

def goPage (url, supermarket_name):
    try:
        driver.get(url)
    except:
        print("ERROR: not possible to open "+ supermarket_name + " in browser.\n Check computer connection and server status.")
        driver.quit()

def waitForElement (by_locator, locator_value):
    wait = WebDriverWait(driver, 10)
    try:
        wait.until(EC.element_to_be_clickable(driver.find_element(by_locator, locator_value)))
    except:
        print("ERROR: waiting element not found")

def getElementByItsText (by_locator, locator_value, locator_content):
    waitForElement(by_locator, locator_value)
    try:
        list_of_elements=driver.find_elements(by_locator, locator_value)
        for e in list_of_elements:
            #print (e.text.lower())
            if locator_content in e.text.lower():
                element = e
                break
        return element
    except:
        print("ERROR: element not found by its text")
        #driver.quit()


def getElementByAttribute (by_locator, locator_value, attribute, attribute_content):
    waitForElement(by_locator, locator_value)
    try:
        list_of_elements=driver.find_elements(by_locator, locator_value)
        for e in list_of_elements:
            if attribute_content in e.get_attribute(attribute):
                element = e
                break
        return element
    except:
        print("ERROR: element not found by its attribute")
        #driver.quit()


def pressButton (locator_content):
    try:
        button=getElementByItsText(By.XPATH, '//button', locator_content)
        button.click()
    except:
        print("ERROR: button not clicked")

def pressLink(locator_content):
    link=getElementByAttribute (By.XPATH, '//a', "href", locator_content)
    try:
        #link=getElementByItsText(By.XPATH, '//a', locator_content)
        link.click()
    except:
        print("ERROR: button not clicked")


def input_bar (inputValue, attribute, attribute_content):
    time.sleep(2)
    waitForElement(By.XPATH, '//input')
    try:
        input_element=getElementByAttribute (By.XPATH, '//input', attribute, attribute_content)
        input_element.clear()
        input_element.click()
        input_element.send_keys(inputValue)
    except:
        print ("ERROR: search element not found")

def changeWord(word):
    for letter in word:
        if "," in letter:
            word = word.replace(letter,".")
    return word

def get_list_filtered(by_locator, locator_value, filter):
    time.sleep(2)
    waitForElement(by_locator, locator_value)
    try:
        filtered_list=[]
        list_of_elements=driver.find_elements(by_locator, locator_value)
        for e in list_of_elements:
            product_text=e.text.lower()
            product_text_lines=re.split("\n", product_text)
            if filter in product_text:
                if "monodosis" not in product_text:
                    filtered_list.append(e)
        return filtered_list
    except:
        print ("ERROR: list not found")

def get_item_value(by_locator, locator_value, filter, cantidad):
    list_filtered=get_list_filtered(by_locator, locator_value, filter)
    data = {
    "nombre": [],
    "precio unitario(€)": [],
    "cantidad("+cantidad+")": [],
    "precio por cantidad(€/"+cantidad+")": []
    }
    try:
        for e in list_filtered:
            product_text=e.text.lower()
            product_text_lines=re.split("\n", product_text)
            #https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
            product_name= product_text_lines[0]
            #print(product_name)
            product_quantity_line= product_text_lines[1]
            #print(product_quantity_line)
            product_price_string = changeWord(re.findall("\d+\,\d+", product_text_lines[2])[0])
            product_price=float(product_price_string)
            if "ml" in product_quantity_line:
                product_quantity_string= changeWord(re.split("\s", product_quantity_line)[1])
                product_quantity=(float(product_quantity_string))/1000
            else:
                product_quantity_string= changeWord(re.split("\s", product_quantity_line)[1])
                product_quantity=float(product_quantity_string)
            product_price_quantity=product_price/product_quantity
            data["nombre"].append(product_name)
            data["precio unitario(€)"].append("%.2f" % product_price)
            data["cantidad("+cantidad+")"].append(product_quantity)
            data["precio por cantidad(€/"+cantidad+")"].append("%.2f" % product_price_quantity)
            data["supermercado)"].append("Mercadona")
        return data
    except:
        print ("ERROR: list not found")

def get_lowest_prized():
    time.sleep(1)

#MAIN
#Mercadona
driver = webdriver.Firefox()
goPage(mercadona.get("url"), mercadona.get("name"))
pressButton ("rechazar")
waitForElement(By.XPATH, '//form')
input_bar("46019", "name", "postal")
pressButton ("continuar")
#input_bar("aceite", "id", "search")
pressLink("categories")

df = pd.DataFrame(get_item_value(By.CLASS_NAME, 'product-cell__info', 'aceite', 'L'))

df.to_csv('aceite.csv')