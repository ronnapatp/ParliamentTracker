import json
import requests

url = 'https://trello.com/b/1LjIXpMK.json'

response = requests.get(url)

if response.status_code == 200:
    jsonContent = response.json()
    outputFile = './format/data/unformattedData.json'

    with open(outputFile, 'w', encoding='utf-8') as file:
        json.dump(jsonContent, file, indent=4, ensure_ascii=False)

    print('JSON formatted and saved to', outputFile)
else:
    print('Failed to retrieve JSON content from the URL.')
