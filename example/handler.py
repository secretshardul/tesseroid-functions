from PIL import Image
import requests
import pytesseract
from io import BytesIO
import json

def main(event, context):
    url = event["body"]
    res = requests.get(url)
    img = Image.open(BytesIO(res.content))
    txt = pytesseract.image_to_string(img, lang="eng")
    # data=json.loads(event["body"])
    # txt=data["lang"]
    return {"statusCode": 200, "body": txt}

