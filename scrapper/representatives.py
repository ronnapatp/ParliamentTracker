import requests
from bs4 import BeautifulSoup
import html
import json
import time  
import re

BASE_URL = 'https://hris.parliament.go.th/'
URL = 'https://hris.parliament.go.th/ss_th.php'

data = []

def scrapeRepresentativeDetails(link):
    try:
        responseInd = requests.get(link)
        if responseInd.status_code == 200:
            htmlContent = responseInd.content.decode('utf-8', errors='ignore')
            soup = BeautifulSoup(htmlContent, 'html.parser')
            
            divElement = soup.find('div', class_='span3')
            
            for img in divElement.find_all('img'):
                img.extract()
            
            detailsText = divElement.get_text(strip=True)
            
            return detailsText
        else:
            print(f"Failed to fetch details page. Status code: {responseInd.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching details: {str(e)}")
        return None

try:
    responseMain = requests.get(URL)
    if responseMain.status_code == 200:
        htmlContent = responseMain.content.decode('utf-8', errors='ignore')

        soup = BeautifulSoup(htmlContent, 'html.parser')

        liElements = soup.find_all('li')

        for idx, li in enumerate(liElements):
            nameElement = li.find('a', class_='sl_name')
            idElement = li.find('span', class_='label label-info')
            linkElement = li.find('a', class_='sl_name') 

            nameOriginal = nameElement.text.strip()
            nameFormatted = re.sub(f"\s+", " ", nameOriginal)
            idNum = idElement.text.strip()

            imgElement = li.find('img')
            imageURL = imgElement['src']

            link = BASE_URL + linkElement['href']

            detailsText = str(scrapeRepresentativeDetails(link))

            if "แบบบัญชีรายชื่อ" in detailsText:
                constituencyOriginal = "บัญชีรายชื่อ"
                partyNameOriginal = detailsText[15:]
                constituencyNumber = "Party-list member"
            elif "จังหวัด" in detailsText:
                constituencyPattern = r'^(.*?) เขต (\d{1,2})(.*)$'
                match = re.search(constituencyPattern, detailsText)
                constituencyOriginal = match.group(1).strip()
                constituencyNumber = match.group(2)
                partyNameOriginal = match.group(3).strip()

            partyName = partyNameOriginal.replace("พรรค", "")
            constituency = constituencyOriginal.replace("จังหวัด","")
            
            data.append({
                "id": idNum.split()[2],
                "name": nameFormatted,
                "image": imageURL,
                "link": link,
                "constituency": constituency,
                "district": int(constituencyNumber) if "จังหวัด" in detailsText else constituencyNumber,
                "party": partyName
            })

            print(idx)

            if idx < len(liElements) - 1:
                time.sleep(1)

        try:
            with open('./data/representatives.json', 'w', encoding='utf-8') as outputFile:
                json.dump(data, outputFile, ensure_ascii=False, indent=4)
            
            print('File saved')
        except Exception as error:
            print(error)

    else:
        print(f"Failed to fetch HTML source code. Status code: {responseMain.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
