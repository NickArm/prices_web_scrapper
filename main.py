from market_sklavenitis import scrape_sklavenitis
from market_ab import scrape_ab
# Import other market modules as needed
# from market_other import scrape_other_market
from product_names import products  # Importing the product array

def main():
    # Scrape products from Sklavenitis
    print("Starting scrape for Sklavenitis...")
    scrape_sklavenitis(products)

    print("Starting scrape for Ab...")
    scrape_ab(products)

    # If you have other markets to scrape, you can call them here
    # print("Starting scrape for Other Market...")
    # scrape_other_market(products)

    print("Scraping complete.")

if __name__ == "__main__":
    main()
