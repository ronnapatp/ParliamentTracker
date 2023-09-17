import requests
from bs4 import BeautifulSoup
import html
import json

url = 'https://hris.parliament.go.th/ss_th.php'

data = []

try:
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.content.decode('utf-8', errors='ignore')

        soup = BeautifulSoup(html_content, 'html.parser')

        li_elements = soup.find_all('li')

        for li in li_elements:
            name_element = li.find('a', class_='sl_name')
            id_element = li.find('span', class_='label label-info')

            name = name_element.text.strip()
            idNum = id_element.text.strip()
            decoded_name = html.unescape(name)

            img_element = li.find('img')
            image_url = img_element['src']

            data.append({
                "ID": idNum.split()[2],
                "Name": name,
                "Image": image_url
            })

        try:
            with open('./representatives/data.json', 'w', encoding='utf-8') as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)
            
            print('File saved')
        except Exception as error:
            print(error)

        def mdData(item):
            return f'| {item["ID"]} | {item["Name"]} | ![]({item["Image"]}) |\n'
        
        markdown_content = ""
        for item in data:
            markdown_content += mdData(item)


        try:
            with open("./representatives/README.md", "w", encoding="utf-8") as file:
                contents = f"""# Representatives List
This is a list of member of the House of Representatives in the 26th paliament. List from [parliament.go.th](https://hris.parliament.go.th/ss_th.php)
| ID | Name | Image |
| ---- | ------- | -------- |
{markdown_content}
            """
                file.write(contents)
        except Exception as error:
            print(error)


    else:
        print(f"Failed to fetch HTML source code. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {str(e)}")
