# POST request example
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://i.imgur.com/zGRdhAT.jpg"

# API architecture for POST 
1. parameters: config,extension
2. Use form-data instead of x-www-form because it supports files also.
3. pytesseract directly accepts image files, not URLs. But tesseract command line takes url path

# languages needed
chi_sim,chi_tra,jpn,kor,spa,eng,fra,nld,deu,rus,lat,grc,ell,ara,hin,ben,