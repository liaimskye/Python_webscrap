from bs4 import BeautifulSoup
import requests
import pandas as pd


grocery_list = ["broccoli", "peach"]

search_url = "https://www.checkers.co.za/search?q="
page_extension = "%3AsearchRelevance%3AbrowseAllStoresFacetOff%3AbrowseAllStoresFacetOff&page="
df = pd.DataFrame(columns = ["product", "price"])
page_number = 0



for i in range(0,len(grocery_list)):
    
    while True:
        product_and_price = []
        full_url = f"{search_url}{grocery_list[i]}{page_extension}{page_number}"
        page = requests.get(full_url)

        soup = BeautifulSoup(page.text, 'html.parser')
        product_names = soup.find_all("h3", class_ = "item-product__name")
        product_price_standard = soup.find_all('span', class_="now")
        price_list = [price.get_text().strip() for price in product_price_standard]
        product_list = [ item.get_text().strip() for item in product_names]
        


        for r in range(len(product_list)):
            product_and_price.append([product_list[r], price_list[r]])

        print(product_and_price)
        
        if len(product_list) > 0:
            page_number += 1

        
            for row in product_and_price:
                length = len(df)
                df.loc[length] = row

        
        else:
            print("all pages read")
            break
            


# write price list to a csv file
# I am considering using df.to_sql instead to create a sql database of prices
print(df)
with open("product_price_list.csv", 'w') as text:
    df_string = df.to_csv(header=False,index=False)
    text.write(df_string)