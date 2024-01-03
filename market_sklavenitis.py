import time
import string
import difflib
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from db_connector import connect, close
from utils import find_best_match

def scrape_sklavenitis(products):
    # Initialize the WebDriver and navigate to the Sklavenitis website
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

        # Use the utility function to find the best match
        best_match_element, highest_similarity = find_best_match(product_elements, product_name)

        if best_match_element and highest_similarity > 0.5:  # Assuming you want at least a 50% match to proceed
            print('Best match found:', best_match_element.text)
            best_match_element.click()
            time.sleep(2)  # Allow time for the product details page to load

            # Fetch product details from the product details page
            product_title = driver.find_element(By.CLASS_NAME, "product-detail__title").text
            product_main_price = driver.find_element(By.CLASS_NAME, "price").get_attribute("data-price")

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

if __name__ == "__main__":
    from product_names import products  # Importing the product array for standalone testing
    scrape_sklavenitis(products)
