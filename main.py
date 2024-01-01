import string
import time
import difflib

import mysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from db_connector import connect, close
from product_names import products  # Importing the product array

# Initialize the WebDriver and navigate to the website
service_obj = Service()
driver = webdriver.Chrome(service=service_obj)
driver.get("https://www.sklavenitis.gr/")
print(driver.title)
print(driver.current_url)
time.sleep(5)
driver.find_element(By.CLASS_NAME, "consent-give").click()

# Loop through each product and perform actions
for product_name in products:
    # Search for the product
    driver.find_element(By.ID, "search").clear()  # Clear the previous search
    driver.find_element(By.ID, "search").send_keys(product_name)
    time.sleep(2)
    product_elements = driver.find_elements(By.CSS_SELECTOR, "li[class='ui-menu-item']")

    # Initialize a variable to track the best match
    best_match_element = None
    highest_similarity = 0.0  # Ensure this is a float for comparison

    # Normalize the search term for comparison
    normalized_search_query = product_name.lower().translate(str.maketrans('', '', string.punctuation))

    # Debugging: Print out the normalized search query
    print("Normalized Search Query:", normalized_search_query)

    # Check each product for the best match to the search query
    for product_element in product_elements:
        product_text = product_element.text.lower().translate(str.maketrans('', '', string.punctuation))
        similarity = difflib.SequenceMatcher(None, normalized_search_query, product_text).ratio()

        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match_element = product_element

    if best_match_element and highest_similarity > 0.5:  # Assuming you want at least a 50% match to proceed
        print('Best match found:', best_match_element.text)
        best_match_element.click()
        time.sleep(2)  # Allow time for the product details page to load

        # Fetch product details from the product details page
        product_title = driver.find_element(By.CLASS_NAME, "product-detail__title").text
        product_main_price = driver.find_element(By.CLASS_NAME, "main-price").text

        # Connect to MySQL Database and Insert Data
        db_connection = connect()
        if db_connection:
            try:
                cursor = db_connection.cursor()
                query = "INSERT INTO Products (title, main_price_sklavenitis) VALUES (%s, %s)"
                values = (product_title, product_main_price)
                cursor.execute(query, values)
                db_connection.commit()
                print("Data saved to MySQL DB - ID:", cursor.lastrowid)
            except mysql.connector.Error as error:
                print("Failed to insert record into MySQL table {}".format(error))
            finally:
                close(db_connection)
    else:
        print('No match found for:', product_name)

        # Add a delay if necessary to prevent rapid-fire requests that might look like a DDoS attack to the server
    time.sleep(2)

# Close the driver after the loop is complete
driver.quit()
