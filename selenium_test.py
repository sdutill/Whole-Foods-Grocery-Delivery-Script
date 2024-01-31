import json
import sys
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service as EdgeService

def pause_until_continue(elementName):
    print(f"Looking for {elementName}")
    user_input = input("Enter \"cont\" to continue:")
    while user_input.lower() != "cont":
        print("Invalid input. Please enter \"cont\" to continue.")
        user_input = input("Enter \"cont\" to continue:")

    print("Continuing...")

INGREDIENTS_FILE = "ingredients.txt"
def load_ingredients(path=INGREDIENTS_FILE):
    with open(INGREDIENTS_FILE, "r") as f:
        ingredients = f.readlines()
        ingredients = [i.strip() for i in ingredients]
        return ingredients

def real_human_type(elt, text):
    for c in text:
        elt.send_keys(c)
        time.sleep(random.randint(1, 15) / 100) # sleep a bit between keypresses

def get_ingredients():
    baseIngredients = load_ingredients()
    # filter out common ingredients i have already
    excludeList = [
        "salt",
        "pepper",
        "olive oil",
        "extra-virgin olive oil",
        "garlic",
        "garlic cloves",
        "garlic powder",
        "cumin",
        "paprika",
        "smoked paprika",
        "honey"
    ]
    ingredients = [ i for i in baseIngredients if i.lower() not in excludeList ] # would be way faster to do this with sets but eh
    return ingredients

def load_cookie(driver, path):
    with open(path, 'r') as cookiesfile:
        cookies = json.load(cookiesfile)
    for cookie in cookies:
        driver.add_cookie(cookie)

def order(driver):
    print("Starting ordering process.")
    ingredients = get_ingredients()
    print(ingredients)
    wait = WebDriverWait(driver, 10)
    print("OK NOW IT IS TIME TO GO TO AMAZON AND ORDER")
    driver.get("https://www.amazon.com/alm/storefront?almBrandId=VUZHIFdob2xlIEZvb2Rz")
    load_cookie(driver, "cookies.json")

    # if True:
    for i in ingredients:
        print(f"Searching for {i}")
        ingredientAddedToOrder = False
        searchbar = driver.find_element(By.XPATH, "//input[@placeholder='Search Amazon']")
        searchbar.clear()
        real_human_type(searchbar, i)
        searchbar.send_keys(Keys.RETURN)

        # Wait for the search results to load
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "s-card-container")))

        # Find and click the first non-sponsored product
        productContainers = driver.find_elements(By.CLASS_NAME, "s-card-container")

        for p in productContainers:
            if "Sponsored" not in p.get_attribute('innerHTML'):
                # Click on the first non-sponsored product
                p.find_element(By.CLASS_NAME, "s-product-image-container").click()

                # Wait for the product page to load
                wait.until(EC.presence_of_element_located((By.ID, "freshAddToCartButton")))

                # Press the "freshAddToCartButton" button
                freshAddToCartButton = driver.find_element(By.ID, "freshAddToCartButton")
                freshAddToCartButton.click()

                print(f'Clicked the button to add {i} to the cart')
                ingredientAddedToOrder = True
                break

        if not ingredientAddedToOrder:
            print(f"No non-sponsored product found for {i}")

    # Wait for the product page to load
    wait.until(EC.presence_of_element_located((By.ID, "nav-cart-count-container")))

    # Press the "freshAddToCartButton" button
    nav_cart_count_container = driver.find_element(By.ID, "nav-cart-count-container")
    nav_cart_count_container.click()

    proceed_to_checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "sc-alm-buy-box-ptc-button-VUZHIFdob2xlIEZvb2Rz")))
    proceed_to_checkout_button.click()

    wait.until(EC.presence_of_element_located((By.ID, "a-autoid-0")))
    a_autoid_0 = driver.find_element(By.ID, "a-autoid-0")
    a_autoid_0.click()

    # Started getting a prompt to sign in here
    # pause_until_continue("subsContinueButton")
    time.sleep(5)
    proceed_to_checkout_button = wait.until(EC.element_to_be_clickable((By.ID, "subsContinueButton")))
    proceed_to_checkout_button.click()

    # after that substition menu
    # pause_until_continue("orderSummaryPrimaryActionBtn")
    time.sleep(5)
    proceed_to_checkout_button_1 = wait.until(EC.element_to_be_clickable((By.ID, "orderSummaryPrimaryActionBtn")))
    proceed_to_checkout_button_1.click()

    # after that, time slot pick menu, just take next
    # pause_until_continue("orderSummaryPrimaryActionBtn")
    time.sleep(10)
    proceed_to_checkout_button_2 = wait.until(EC.element_to_be_clickable((By.ID, "orderSummaryPrimaryActionBtn")))
    proceed_to_checkout_button_2.click()

    time.sleep(10)
    # pause_until_continue("submitOrderButtonId")
    submitButton = wait.until(EC.element_to_be_clickable((By.ID, "submitOrderButtonId")))
    if submitButton:
        print("Found the Submit Order Button. We ain't buying this shit tho")
    sys.exit()
    # DANGER DANGER DO NOT UNCOMMENT THIS CLICK unless you want to submit for real and actually pay real money
    ### submitButton.click()

def main():
    # Specify the path to the Edge webdriver executable
    edge_driver_path = "C:\\Program Files\\msedgedriver.exe"
    # Initialize the Edge webdriver using the Edge service
    edge_service = EdgeService(executable_path=edge_driver_path)
    edge_options = Options()
    edge_options.add_argument("--enable-chrome-browser-cloud-management")
    driver = webdriver.Edge(service=edge_service, options=edge_options)

    # Regular runs
    if True:
        order(driver)
    # First-time setup:
    # - Set the above boolean to false
    # - Start the driver, then manually navigate to Bing, sign in, go to the chat page.
    # - Wait for cookies to save.
    # - Do the same for Amazon; manually navigate and sign in, wait for cookies to save.
    else:
        print("GO SIGN IN TO BING! 60 seconds to do so.")
        time.sleep(60)
        save_cookie(driver, "bingcookies.json")
        print("SAVED BING COOKIES (hopefully)!")
        print("GO SIGN IN TO AMAZON! 60 seconds to do so.")
        time.sleep(60)
        save_cookie(driver, "cookies.json")

main()