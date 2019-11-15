import pytesseract
import urllib.request, urllib.parse
import logging
import base64
import json
from requests_toolbelt.multipart import decoder
ERRORMSG="Invalid parameters. Use [image](compulsory, can be array),lang,config,output_type,timeout"
def main(event,context):
    body=event["body"].encode()
    content_type=event["headers"]["Content-Type"]
    response = ''
    parts=decoder.MultipartDecoder(body,content_type).parts
    recieved={
        "images":[],
        "lang":"eng",
        "config":"",
        "output_type":"string"
    }
    
    #skip timeout
    #extract name, type from header; URL/binary from content
    for part in decoder.MultipartDecoder(body,content_type).parts:  
        # print("Content %s"%part.content)
        print("header %s"%part.headers)
        val=part.text # inside value- url or binary
        content_disp=part.headers[b'Content-Disposition']
        print("content disposition: %s"%content_disp) # b'form-data; name="image"; filename="1.jpeg"'
        if b'name="image"' in content_disp:
            recieved["images"].append(val)
        elif b'name="lang"' in content_disp:
            recieved["lang"]=val
        elif b'name="config"' in content_disp:
            recieved["config"]=val
        elif b'name="output_type"' in content_disp:
            recieved["output_type"]=val
        
        
        #extract name, filename from content_disp
        # content_type not needed. If filename present then file sent, otherwise URL
        
     #DO ocr
    resp_body=[]
    try:
        for image in recieved["images"]:
            with urllib.request.urlopen(image) as response, open("/tmp/img", 'wb') as out_file: #no .extension needed
                data = response.read() # a `bytes` object
                out_file.write(data)
            txt = pytesseract.image_to_string("/tmp/img",lang=recieved["lang"],config=recieved["config"],output_type=recieved["output_type"]) # type casting
            print(txt)
            resp_body.append(txt)
        return {"statusCode": 200, "body": str(resp_body)}
    except:
        return {"statusCode": 400, "body": ERRORMSG}

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps(recieved)
    # }
# def main(event, context):
#     body=urllib.parse.parse_qs(event["body"])
#     logging.info("Body: %s"%body)
#     images=body["image"]
#     try:
#         lang= body["lang"][0]
#     except:
#         lang="eng"
#     try:
#         config=body["config"][0]
#     except:
#         config=""
#     try:
#         output_type=body["output_type"][0]
#     except:
#         output_type="string"
#     try:
#         timeout=body["timeout"][0]
#     except:
#         timeout=20
#     resp_body=[]
#     try:
#         for image in images:
#             with urllib.request.urlopen(image) as response, open("/tmp/img", 'wb') as out_file: #no .extension needed
#                 data = response.read() # a `bytes` object
#                 out_file.write(data)
#             txt = pytesseract.image_to_string("/tmp/img",lang=lang,config=config,output_type=output_type,timeout=1) # type casting
#             print(txt)
#             resp_body.append(txt)
#         return {"statusCode": 200, "body": str(resp_body)}
#     except:
#         return {"statusCode": 400, "body": ERRORMSG}


