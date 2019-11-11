import pytesseract
import urllib

def main(event, context):
    url = event["body"]
    # better save to /tmp/img then use OCR
    with urllib.request.urlopen(url) as response, open("/tmp/img", 'wb') as out_file: #no .extension needed
        data = response.read() # a `bytes` object
        out_file.write(data)
    txt = pytesseract.image_to_string("/tmp/img", lang="eng")

    # print(txt)
    return {"statusCode": 200, "body": txt}

# if __name__=="__main__":
#     main(0,0)

