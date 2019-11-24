# -*- coding: utf-8 -*-
import urllib
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
from skimage import io
import bs4
import ssl
import json
import re
import sys
import warnings
import urlopen
import random
import base64
import pickle


def im2json(im):
    """Convert a Numpy array to JSON string"""
    imdata = pickle.dumps(im)
    jstr = json.dumps({"image": base64.b64encode(imdata).decode('ascii')})
    return jstr

def json2im(jstr):
    """Convert a JSON string back to a Numpy array"""
    load = json.loads(jstr)
    imdata = base64.b64decode(load['image'])
    im = pickle.loads(imdata)
    return im

if not sys.warnoptions:
    warnings.simplefilter("ignore")


#For ignoring SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# url = input('Enter url - ' )
url=input("Enter Tripadvisor Hotel Url- ")
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'html.parser')

html = soup.prettify("utf-8")
hotel_json = {}

for line in soup.find_all('script',attrs={"type" : "application/ld+json"}):
    details = line.text.strip()
    details = json.loads(details)
    hotel_json["name"] = details["name"]
    hotel_json["url"] = "https://www.tripadvisor.in"+details["url"]
    hotel_json["images"] = details["image"]
    #details["priceRange"] = details["priceRange"].replace("₹ ","Rs ")
    #details["priceRange"] = details["priceRange"].replace("₹","Rs ")
    #hotel_json["priceRange"] = details["priceRange"]
    hotel_json["aggregateRating"]={}
    hotel_json["aggregateRating"]["ratingValue"]=details["aggregateRating"]["ratingValue"]
    hotel_json["aggregateRating"]["reviewCount"]=details["aggregateRating"]["reviewCount"]
    hotel_json["address"]={}
    hotel_json["address"]["Street"]=details["address"]["streetAddress"]
    hotel_json["address"]["Locality"]=details["address"]["addressLocality"]
    hotel_json["address"]["Region"]=details["address"]["addressRegion"]
    hotel_json["address"]["Zip"]=details["address"]["postalCode"]
    hotel_json["address"]["Country"]=details["address"]["addressCountry"]["name"]
    break

#rgx = re.compile('common-photo-carousel-PhotoCarousel__photo--11M-m common-photo-carousel-PhotoCarousel__crop')
det = []
amen = soup.find_all('div', attrs={'class' : 'ssr-init-26f'})
for l in amen[0]:
	if type(l) is not bs4.element.NavigableString and  bs4.element.Tag :
		det.append(l.find_all(text=True))
        
hotel_json["description"] = max(det[1], key=len)

rgx = re.compile('ssr-init-26f hotels-hotel-review-layout-Section__plain')
price = soup.find_all('div', attrs={'class' : 'ssr-init-26f'})

pricerng = []
for i in price:
	if 'PRICE RANGE' in i.text: 
		pricerng.append(i.find_all(text=True))

finalprice = []
for i in pricerng[0]:
	if i.startswith('₹'):
		finalprice.append(i)

hotel_json["priceRange"] = {}
hotel_json["priceRange"]["lower"] = finalprice[0]
hotel_json["priceRange"]["upper"] = finalprice[1]
hotel_json["numberRooms"] = pricerng[0][len(pricerng[0])-1]


details = det[1]
idx1 = details.index('Property amenities') + 1
idx2 = details.index('Room features') - 1
propertyamen = details[idx1 : idx2]
idx1 = details.index('Room features') + 1
idx2 = details.index('Good to know') - 1
roomfeatures = details[idx1:idx2 ]
hotel_json["hotelServices"] = {}
hotel_json["hotelServices"]["propertyAmenities"] = propertyamen
hotel_json["hotelServices"]["roomFeatures"] = roomfeatures


getph = []
for i in price:
	if 'Contact' in i.text:
		getph.append(i.find_all(text=True))
contactlist = getph[0]
phone = contactlist.index('Contact') + 2
hotel_json["address"]["phNumber"] = contactlist[phone]


response = html
img = re.findall(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", str(response))
imgs = [x for x in img
		if x[1].endswith('.jpg')]
rand_imgs = random.sample(imgs, 7)
img_urls = []
img_arrays = []
for i in rand_imgs:
	img_urls.append(i[1])
for url in img_urls:
	url = 'https://media-cdn.tripadvisor.com'+url
	image = io.imread(url)
	img_arrays.append(image)

jstr = []
for arr in img_arrays:
	jstr.append(im2json(arr))
	
hotel_json["images"] = jstr


with open(hotel_json["name"]+".html", "wb") as file:
    file.write(html)

with open(hotel_json["name"]+".json", 'w') as outfile:
    json.dump(hotel_json, outfile, indent=4)
	