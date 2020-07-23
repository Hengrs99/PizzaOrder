from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
import time
import unidecode

loc1XPATH = "/html/body/div[2]/div[5]/a[1]"
loc2XPATH = "/html/body/div[2]/div[5]/a[2]"
loc3XPATH = "/html/body/div[2]/div[5]/a[3]"
understandButtonXPATH = "/html/body/div[4]/div/div[8]/div[5]/div[7]/button"
filterButtonXPATH = "/html/body/div[4]/div/div[8]/div[5]/div[5]/button"
rawPizzaHeaderXPATH = "/html/body/div[4]/div/div[8]/div[5]/div[6]/div[0]/div[1]/a/div/div[2]/h4"
addToBasketButtonXPATH = "/html/body/div[4]/div/div[8]/div[8]/div[1]/div/div[4]/input[1]"
goToBasketButtonXPATH = "/html/body/div[4]/div/div[6]/div[1]/div[4]/div[2]/a"
continueButtonXPATH = "/html/body/div[4]/div/div[8]/div[6]/div/div[6]/div[1]/div[4]/div[2]/a"
continueButton2XPATH = "/html/body/div[4]/div/div[8]/div[10]/div[1]/div[4]/div/div[5]/div[2]/a"
continueButton3XPATH = "/html/body/div[4]/div/div[8]/form/div[1]/div[1]/div[2]/div/div[7]/div[2]/a"
toggleButtonXPATH = "/html/body/div[4]/div/div[8]/form/div[2]/div[1]/div[1]/div/div[7]/div[2]/label/div"

pizzaTypes = ["margherita", "syrova", "sunkova", "capricciosa", "hawaii", "olivova", "marinara", "tunakova",
              "vegetariana", "salamova", "zampionova", "americana", "dabelska", "fantastico", "farmarska", "sedlacka",
              "kureci", "crudo", "brusinkova exclusive", "provensalska exclusive", "albori exclusive",
              "kureci special exclusive"]


def ask_for_loc_xpath():
    global locXPATH

    loc1 = "Roztoky"
    loc2 = "Děčín"
    loc3 = "Příbram"

    loc = unidecode.unidecode(input("Enter shop location (" + loc1 + ", " + loc2 + ", " + loc3 + "): ").lower())

    if loc == unidecode.unidecode(loc1).lower():
        locXPATH = loc1XPATH
    elif loc == unidecode.unidecode(loc2).lower():
        locXPATH = loc2XPATH
    elif loc == unidecode.unidecode(loc3).lower():
        locXPATH = loc3XPATH
    elif loc == "":
        locXPATH = loc1XPATH
    else:
        print("Invalid location")
        time.sleep(1)
        print()
        ask_for_loc_xpath()

    return locXPATH


def ask_for_pizza_name():
    global isPizzaValid
    wantedPizza = unidecode.unidecode(input("Enter pizza name: ")).lower()
    for pizza in pizzaTypes:
        if pizza == wantedPizza:
            isPizzaValid = True
    if isPizzaValid:
        return wantedPizza
    else:
        print("Invalid pizza name")
        time.sleep(1)
        print()
        ask_for_pizza_name()


def find_pizza_xpath():
    for pizza in pizzaTypes:
        if pizza == selectedPizza:
            return rawPizzaHeaderXPATH.replace(rawPizzaHeaderXPATH[47], str(pizzaTypes.index(pizza) + 2))


def wait_for_element_xpath(element_name, element_xpath):
    try:
        return (WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.XPATH, element_xpath))
        ))

    except:
        print("Error: couldn't click on --> " + element_name)
        driver.quit()


def wait_for_element_id(element_name, element_id):
    try:
        return (WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, element_id))
        ))

    except:
        print("Error: couldn't click on --> " + element_name)
        driver.quit()


locXPATH = ask_for_loc_xpath()
selectedPizza = ask_for_pizza_name()

PATH = "C:\Program Files (x86)\chromedriver"
driver = webdriver.Chrome(PATH)
driver.maximize_window()
driver.get("https://www.pizzafantastico.cz/")

city = driver.find_element_by_xpath(locXPATH)
city.click()

understandButton = wait_for_element_xpath("understandButton", understandButtonXPATH)
understandButton.click()

filterButton = wait_for_element_xpath("filterButton", filterButtonXPATH)
filterButton.click()

searchField = driver.find_element_by_id("filter-name-input")
searchField.send_keys(selectedPizza)
searchField.send_keys(Keys.RETURN)

pizzaHeaderXPATH = find_pizza_xpath()

pizzaHeader = wait_for_element_xpath("pizzaHeader", pizzaHeaderXPATH)
# TODO Pizza sometimes doesn't show up, needs to be fixed
pizzaHeader.click()

addToBasketButton = wait_for_element_xpath("addToBasketButton", addToBasketButtonXPATH)
# TODO User should be able to choose amount of pizzas he wants
addToBasketButton.click()

goToBasketButton = driver.find_element_by_xpath(goToBasketButtonXPATH)
goToBasketButton.click()

time.sleep(3)

continueButton = wait_for_element_xpath("continueButton", continueButtonXPATH)
# TODO User should be able to choose amount of pizzas he wants
continueButton.click()

continueButton2 = wait_for_element_xpath("continueButton2", continueButton2XPATH)
# TODO User should be able to choose where he wants to pick up pizza (home or shop)
continueButton2.click()

continueButton3 = wait_for_element_xpath("continueButton3", continueButton3XPATH)
# TODO User should be able to pay either with cash or online
continueButton3.click()

name = wait_for_element_id("name", "name")

# TODO Personal info should be customizable by user

name.send_keys("Petr")
surname = driver.find_element_by_id("surmane")
surname.send_keys("Jeřábek")
email = driver.find_element_by_id("email")
email.send_keys("hengrs99@seznam.cz")
telephone = driver.find_element_by_id("telephone")
telephone.send_keys("736601539")

toggleButton = driver.find_element_by_xpath(toggleButtonXPATH)
toggleButton.click()
