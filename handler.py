import pytesseract
import urllib.request, urllib.parse
import logging
ERRORMSG="Invalid parameters. Use [image](compulsory, can be array),lang,config,output_type,timeout"
def main(event, context):
    body=urllib.parse.parse_qs(event["body"])
    logging.info("Body: %s"%body)
    images=body["image"]
    try:
        lang= body["lang"][0]
    except:
        lang="eng"
    try:
        config=body["config"][0]
    except:
        config=""
    try:
        output_type=body["output_type"][0]
    except:
        output_type="string"
    try:
        timeout=body["timeout"][0]
    except:
        timeout=20
    resp_body=[]
    try:
        for image in images:
            with urllib.request.urlopen(image) as response, open("/tmp/img", 'wb') as out_file: #no .extension needed
                data = response.read() # a `bytes` object
                out_file.write(data)
            txt = pytesseract.image_to_string("/tmp/img",lang=lang,config=config,output_type=output_type,timeout=1) # type casting
            print(txt)
            resp_body.append(txt)
        return {"statusCode": 200, "body": str(resp_body)}
    except:
        return {"statusCode": 400, "body": ERRORMSG}


