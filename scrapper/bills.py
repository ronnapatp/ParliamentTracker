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

    stage = ""

    allStages = {
        "ขอยืนยันร่าง พ.ร.บ. ค้างสภาก่อน": "billsFromTheLastParliamentaryTerm",
        "การริเริ่มเสนอร่าง": "",
        "การร่วมเสนอร่าง": "",
        "รอวินิจฉัยการเงิน": "waitingForTheFinancialBillOrNotDecision",
        "ไม่เป็นร่างการเงิน /รับฟังความคิดเห็น": "notAFinancialBillAndCurrentlyListeningToThePublic",
        "เป็นร่างการเงิน/ส่ง นรม. ให้คำรับรอง/รับฟังความคิดเห็น": "",
        "รอเข้าบรรจุวาระ": "waitingForTheSchedule",
        "สส.วาระ 1": "representativesFirstReading",
        "สส.วาระ 2": "representativesSecondReading",
        "สส.วาระ 3": "representativesThirdReading",
        "สว.วาระ 1": "senatorsFirstReading",
        "สว.วาระ 2": "senatorsSecondReading",
        "สว.วาระ 3": "senatorsThirdReading",
        "ทูลเกล้าพิจารณา": "considerationFromHisMajesty",
        "ประกาศราชกิจจา (Gazette)": "royalGazette",
        "ที่ประชุมมีมติถอนร่าง พ.ร.บ.ออกจากระเบียบวาระฯ": "",
        "ร่างพรบ.ค้าง สภา ที่ตกไปตาม ม.147 ของรัฐธรรมนูญ": "dropBillsFromTheLastParliamentaryTermByTheSection147OfTheConstitution"
    }

    if list_name == "N/A":
        stage = list_after_name
    elif list_after_name == "N/A":
        stage = list_name
    else:
        stage = "Stage Not Found"

    if name != "N/A" and name not in unique_names:

        purposer = des[0].replace("ผู้เสนอ","").replace("\n","")

        data.append({
            "Name": name,
            "Purposer": purposer,
            "Status": stage
        })

        unique_names.add(name)

with open(outputFilePath, 'w', encoding='utf-8') as output_file:
    json.dump(data, output_file, ensure_ascii=False, indent=4)

print(f"Filtered data has been written to {outputFilePath}")
