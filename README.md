# Tripadvisor-Scraper
Python program for collection hotel information into JSON

## Hotel Information extracted
* Name
* URL (Tripadvisor)
* Aggregate rating
  * Rating value
  * Review count
* Address
* Description
* Price range
* Hotel Services
  * Property amenities
  * Room features
* Image URLs

## How to use
```
git clone https://github.com/dRoid17x/Tripadvisor-Scraper.git
cd Tripadvisor-Scraper
python main.py
```
Provide the input as particular hotel link, as follows:
```
python main.py
>200
>Enter Tripadvisor Hotel Url- https://www.tripadvisor.in/Hotel_Review-g304551-d3510307-Reviews-The_Leela_Ambience_Convention_Hotel_Delhi-New_Delhi_National_Capital_Territory_of_Delh.html
```
Output created in `output` directory. (JSON adn HTML files)<br/>
Additionally if you would like to store images as a whole (as JSON string) to JSON just uncomment lines 128 to 138.<br/>
You can convert these JSON strings into image file using function `json2im(jstr)`