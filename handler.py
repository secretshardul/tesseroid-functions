import pytesseract
import urllib.request
import base64
from io import BytesIO
import logging
import json
import zipfile
import os
import boto3

s3 = boto3.client('s3')
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def main(event, context):
    global txt
    txt=[]
    logger.info("event:%s"%event)
    # image = Image.open(BytesIO(base64.b64decode(event["image"])))
    # integration request ensures the 3 are always present. In exception just value is absent
    lang="eng"
    config=""
    output_type="string" #bytes type not supported
    func="string"
    if event["lang"]!="":
        lang=event["lang"]
    if event["config"]!="":
        config=event["config"]
    if event["output_type"]!="":
        output_type=event["output_type"]
    if event["func"]!="":
        func=event["func"]
    
   
    
    if(event["type"]=="img_file"):
        # zip file for batch
        file1=open(r"/tmp/img","wb")
        image=base64.b64decode(event["image"])
        file1.write(image)
        file1.close()  
        select_func("/tmp/img",lang=lang,config=config,output_type=output_type,func=func)
        

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
            select_func(path,lang=lang,config=config,output_type=output_type,func=func)


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
            select_func("/tmp/img",lang=lang,config=config,output_type=output_type,func=func)
            
    logger.info("txt:%s"%txt)
    return json.dumps(txt)
  
  
# string,boxes,data,osd,pdf,hocr    
def select_func(image,lang,config,output_type,func):
    global txt
    if (func=="string"):
        txt.append(pytesseract.image_to_string(image,lang=lang,config=config,output_type=output_type))
    elif (func=="boxes"):
        txt.append(pytesseract.image_to_boxes(image,lang=lang,config=config,output_type=output_type))
    elif (func=="data"):
       txt.append(pytesseract.image_to_data(image,lang=lang,config=config,output_type=output_type))
    elif (func=="osd"):
        txt.append(pytesseract.image_to_osd(image,config=config,output_type=output_type)) #no lang
    elif (func in ["pdf","hocr"]):
        image_to_pdf_or_ocr = pytesseract.image_to_pdf_or_hocr("/tmp/img",lang=lang,config=config,extension=func)
        f = open("/tmp/tesseroid.%s"%func, "w+b")
        f.write(bytearray(image_to_pdf_or_ocr))
        f.close()
        s3.upload_file("/tmp/tesseroid.%s"%func, os.environ["BUCKET_NAME"], "tesseroid.%s"%func)

