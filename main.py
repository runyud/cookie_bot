from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import time

chrome_driver_path = ChromeDriverManager().install()  # Install the chromedriver executable local to your project

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)  # Keeps the browser open when the script finishes

service = ChromeService(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("http://orteil.dashnet.org/experiments/cookie/")

# find cookie to click on
cookie = driver.find_element(By.ID, "cookie")

# find upgrade item elements
upgrades = driver.find_elements(By.CSS_SELECTOR, "#store div")
upgrade_ids = [item.get_attribute("id") for item in upgrades]

timeout = time.time() + 5
# 5 minutes
five_min = time.time() + 60 * 5

while True:
    cookie.click()

    # every 5 sec
    if time.time() > timeout:

        # get all upgrade tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert text into an integer price
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # map item prices to their ids
        upgrades_dict = {}
        for n in range(len(item_prices)):
            upgrades_dict[item_prices[n]] = upgrade_ids[n]

        # get current cookie count
        money = driver.find_element(By.ID, "money").text
        if "," in money:
            money = money.replace(",", "")
        cookie_count = int(money)

        # find upgrades we can afford
        affordable_items = {}
        for cost, cookie_id in upgrades_dict.items():
            if cookie_count > cost:
                affordable_items[cost] = cookie_id

        # get the most expensive affordable item
        most_expensive_item = max(affordable_items)
        print(most_expensive_item)
        purchase_id = affordable_items[most_expensive_item]

        driver.find_element(By.ID, purchase_id).click()

        # increment another 5 seconds for timeout
        timeout = time.time() + 5

    # after 5 minutes stop the script and check cookies per second
    if time.time() > five_min:
        cookie_rate = driver.find_element(By.ID, "cps").text
        print(cookie_rate)
        break
