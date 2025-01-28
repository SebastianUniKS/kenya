import requests
from requests.exceptions import ConnectionError

from superSecret import superSecretToken

startDate = "2024-11-01 00:00:01"
endDate = "2025-01-15 23:59:59"


def getImageList(startDate, endDate):
    headers = {
            'Accept': 'application/json',
            'Authorization': superSecretToken
            }
    files = []

    url = "http://compwiz.co.ke:11083/api/images"
    params = {"from": startDate, "to": endDate }
    try:
        response = requests.get(url, headers=headers, params=params, files=files, timeout=5)
        response.raise_for_status()
        print(response.json())
        imageList = response.json()
        return imageList
    except ConnectionError as e:
        print(f"Connection error: {e}")

#getImageList(startDate, endDate)

def getImages(imageList):
    for item in imageList['images']:
        #print(item['url'])
        brian
        image_name = item['url'].split('/')
        brian_img = requests.request("GET", item['url'], headers=headers)
        print(item['url'], image_name[5])
        img = Image.open(BytesIO(brian_img.content))
        #img.save(imagename_full)
        img.save('downloadedImages/'+image_name[5])
        
        image_count += 1
        if image_count % 25 == 0:
            print("Pausing for 5 minutes after downloading 25 images...")
            time.sleep(300)  # Pause for 5 minutes (300 seconds)
        time.sleep(4)

startDate = "2025-01-01 00:00:00"
endDate = "2025-01-19 23:59:59"

def getGPSdata(startDate, endDate):

    headers = {
            'Accept': 'application/json',
            'Authorization': superSecretToken
            }
    files = []

    url = "http://compwiz.co.ke:11083/api/location-history"
    
    params = {"start": startDate, "end": endDate }
    try:
        response = requests.get(url, headers=headers, params=params, files=files, timeout=10)
        #response.raise_for_status()
        print(response.json())
        return response.json()
        
    except ConnectionError as e:
        print(f"Connection error: {e}")

#getGPSdata(startDate, endDate)