import json
import requests
import pytz, time, datetime

url = 'https://trello.com/b/1LjIXpMK.json'

response = requests.get(url)
jsonContent = response.json()

thailandTimeZone = pytz.timezone("Asia/Bangkok")
utcDateTime = datetime.datetime.utcfromtimestamp(time.time())
localizedDatetime = utcDateTime.replace(tzinfo=pytz.utc).astimezone(thailandTimeZone)
formattedTime = localizedDatetime.strftime('%Y-%m-%d %H:%M:%S %Z')

outputFilePath = "./data/bills.json"
data = [
    {
        "Latest update": formattedTime,
    }
]

unique_names = set()

for action in jsonContent.get("actions", []):
    card_data = action.get("data", {}).get("card", {})
    name = card_data.get("name", "N/A")
    des = card_data.get("desc", "N/A").splitlines(True)
    list_name = action.get("data", {}).get("list", {}).get("name", "N/A")
    list_after_name = action.get("data", {}).get("listAfter", {}).get("name", "N/A")

    status = ""

    if list_name == "N/A":
        status = list_after_name
    elif list_after_name == "N/A":
        status = list_name
    else:
        status = "Status Not Found"

    if name != "N/A" and name not in unique_names:

        data.append({
            "Name": name,
            "Purposer": des[0],
            "Status": status
        })

        unique_names.add(name)

with open(outputFilePath, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Filtered data has been written to {outputFilePath}")
