import json

input_file_path = './format/data/unformattedData.json'
output_file_path = './format/data/formattaedData.json'  

with open(input_file_path, 'r', encoding='utf-8') as file:
    thai_json = file.read()

jsonF = json.loads(thai_json)

filtered_data = []

unique_names = set()

for action in jsonF.get("actions", []):
    card_data = action.get("data", {}).get("card", {})
    name = card_data.get("name", "N/A")
    des = card_data.get("desc", "N/A").splitlines(True)
    list_name = action.get("data", {}).get("list", {}).get("name", "N/A")
    list_after_name = action.get("data", {}).get("listAfter", {}).get("name", "N/A")

    if name != "N/A" and name not in unique_names:

        filtered_data.append({
            "Name": name,
            "Purposer": des[0],
            "List": list_name,
            "List After": list_after_name
        })

        unique_names.add(name)

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(filtered_data, output_file, ensure_ascii=False, indent=4)

print(f"Filtered data has been written to {output_file_path}")
