
detailsText = "จังหวัดหนองคาย เขต 1พรรคพลังประชารัฐ"
if "แบบบัญชีรายชื่อ" in detailsText:
    constituency = "บัญชีรายชื่อ"
    party = detailsText[15:]
else:
    constituency = detailsText.split()[0] + " เขต " + list(detailsText.split()[2])[0]
    party = detailsText.split()[2][1:]

print(party)