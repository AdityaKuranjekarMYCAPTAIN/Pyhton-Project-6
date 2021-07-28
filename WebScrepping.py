import pandas
import requests
import pandas as pd
from bs4 import BeautifulSoup

oyo_url = "https://www.oyorooms.com/hotels-in-bangalore/?page="
page_num_MAX = 3

scraped_info_list = []
for page_num in range(1, page_num_MAX):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36'}

    req = requests.get(oyo_url+str(page_num), headers=headers)
    content = req.content

    soup = BeautifulSoup(content, "html.parser")

    all_hotels = soup.find_all("div",{"class":"hotelCardListing"})



    for hotel in all_hotels:
        hotel_dict = {}
        hotel_dict["name"] = hotel.find("h3",{"class":"listingHotelDescription__hotelName"}).text
        hotel_dict["address"] = hotel.find("span", {"itemprop": "streetAddress"}).text
        hotel_dict["price"] = hotel.find("span", {"class": "listingPrice__finalPrice"}).text
        try:
             hotel_dict["rating"] = hotel.find("span", {"class": "hotelRating__ratingSummary"}).text
        except AttributeError:
            pass

        parent_amenities_element = hotel.find("div",{"class":"amenityWrapper"})

        amenities_list = []
        for amenity in parent_amenities_element.find_all("div",{"class":"amenityWrapper__amenity"}):
            amenities_list.append(amenity.find("span",{"class":"d-body-sm"}).text.strip())

        hotel_dict["amenities"] = ', '.join(amenities_list[:-1])

        scraped_info_list.append(hotel_dict)

        # print(hotel_name, hotel_address, hotel_price, hotel_rating, amenities_list )

dataFrame = pandas.DataFrame(scraped_info_list)
dataFrame.to_csv("Oyo.csv")
#..................>>>>>>>>>>>>>>HAPPY CODING<<<<<<<<<<<<<<<<.................
