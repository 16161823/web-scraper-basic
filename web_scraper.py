import requests
from bs4 import BeautifulSoup 
import os
import datetime


#url of page you want requests to get for you and a local variable of it called page
url = "http://alexhire.com/"
page = requests.get(url)

#If the request was without issue code 200, makes a beautfilsoup object
if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')
    #print(soup.prettify())

#soup.find() will find the first instance of the object and you use .get("") to retrieve more. .find("img") will get an image file
container = soup.find('div', class_="container-fluid bg-1 text-center")
image = container.find("img")
image_source = image.get('src')

image_url = url + image_source

#This header and referer will prevent an 403 FORBIDDEN error.
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
'referer': "http://www.alexhire.com/"}

#requests.get() requests the image from the website acting as your browser.
response = requests.get(image_url, headers=headers)
print('Single Image Download: ')
print( "Request Status Code: " + str(response.status_code) )
print("Time Waiting for Response: " + str(response.elapsed) + '\n')

if response.status_code == 200:
    #with open() creates a file as 'f'. with "wb+" meaning "write bytes" - Google: python "wb+" meaning.
    #the "with" keyword takes care of closing the file locally for us after you exit the indented bit of code
    with open('test.jpg', "wb+") as f:
       f.write(response.content)
       print("File written\n")

#Now we're gonna take a all images in the one pass.
images = soup("img")
start_time = datetime.datetime.now()

for image in images:
    #using image.get('src') returns the src name so it can be used as a filename locally
    with open(image.get('src'), 'wb+') as f:
        image_url = url + image.get('src')
        img = requests.get(image_url, headers=headers)
        f.write(img.content)

        print('Image Source: ' + image.get('src'))
        print('Time Waiting for Response: ' + str(img.elapsed) +'\n')
        #img.close is used to close connection with the site before making another enquiry
        img.close

end_time = datetime.datetime.now()
print('Total Time for Download: ' + str(end_time - start_time))



