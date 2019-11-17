# application/octet-stream
{
    "type": "img_file",
    "image": "$input.body",
    "lang": "$input.params('lang')",
    "config": "$input.params('config')",
    "output_type": "$input.params('output_type')"
}

# application/zip
{
    "type": "zip",
    "zip": "$input.body",
    "lang": "$input.params('lang')",
    "config": "$input.params('config')",
    "output_type": "$input.params('output_type')"
}
# application/json
{
    "type": "json",
    "image": $input.json('$.image'),
    "lang": "$input.params('lang')",
    "config": "$input.params('config')",
    "output_type": "$input.params('output_type')"
}

# handler code
```py
import pytesseract
import urllib.request
import base64
from io import BytesIO
import logging
import json
import zipfile
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# from PIL import Image
def main(event, context):
    logger.info("event:%s"%event)
    # image = Image.open(BytesIO(base64.b64decode(event["image"])))
    # integration request ensures the 3 are always present. In exception just value is absent
    lang="eng"
    config=""
    output_type="string" #bytes type not supported
    
    if event["lang"]!="":
        lang=event["lang"]
    if event["config"]!="":
        config=event["config"]
    if event["output_type"]!="":
        output_type=event["output_type"]

    
   
    txt=[]
    if(event["type"]=="img_file"):
        # zip file for batch
        file1=open(r"/tmp/img","wb")
        image=base64.b64decode(event["image"])
        file1.write(image)
        file1.close()  
        ocr = pytesseract.image_to_string("/tmp/img",lang=lang,config=config,output_type=output_type)
        txt.append(ocr)

    elif(event["type"]=="zip"):
        # decode, save, unzip
        file1=open(r"/tmp/compressed.zip","wb")
        file1.write(base64.b64decode(event["zip"]))
        file1.close() 
        zfile = zipfile.ZipFile("/tmp/compressed.zip")
        file_list = [( name, 
                   '/tmp/' + os.path.basename(name)) 
                for name in zfile.namelist()]
        # logger.info("got names {}".format("; ".join([n for n,b in file_list])))
        for name,path in file_list:
            logger.info("%s in %s"%(name,path))
            with open(path, 'wb') as f:
                f.write(zfile.read(name))
                f.close()
            ocr = pytesseract.image_to_string(path,lang=lang,config=config,output_type=output_type)
            txt.append(ocr)

    elif(event["type"]=="json"):
        if event["image"]=="":
           raise Exception('Malformed Image field')
        for url in event["image"]:
            file1=open(r"/tmp/img","wb")
            response = urllib.request.urlopen(url)
            # requests.get(event["image"][0])  
            image=response.read()
            file1.write(image)
            file1.close()  
            ocr = pytesseract.image_to_string("/tmp/img",lang=lang,config=config,output_type=output_type)
            
            txt.append(ocr)
    
    return txt
    

# if __name__=="__main__":
#     main(0,0)

```
