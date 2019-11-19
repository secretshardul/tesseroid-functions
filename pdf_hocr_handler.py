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
BUCKET_NAME = 'com.shardul.tesseroid.pdfhocr'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# from PIL import Image
def main(event, context):
    logger.info("event:%s"%event)
    # image = Image.open(BytesIO(base64.b64decode(event["image"])))
    # integration request ensures the 3 are always present. In exception just value is absent
    lang="eng"
    config=""
    extension="pdf" #bytes type not supported
    if event["lang"]!="":
        lang=event["lang"]
    if event["config"]!="":
        config=event["config"]
    if event["extension"]!="":
        func=event["extension"]
    
    if(event["type"]=="img_file"):
        # zip file for batch
        file1=open(r"/tmp/img","wb")
        image=base64.b64decode(event["image"])
        file1.write(image)
        file1.close()  
        # ocr = select_func("/tmp/img",lang=lang,config=config,output_type=output_type,func=func)
        image_to_pdf_or_ocr = pytesseract.image_to_pdf_or_hocr("/tmp/img",lang=lang,config=config,extension=extension)
        f = open("/tmp/tesseroid.%s"%extension, "w+b")
        f.write(bytearray(image_to_pdf_or_ocr))
        f.close()
        s3.upload_file("/tmp/tesseroid.%s"%extension, BUCKET_NAME, "tesseroid.%s"%extension)

    # how to redirect to multiple files? Maybe compress to ZIP
    # don't try until then
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
            # ocr = select_func(path,lang=lang,config=config,output_type=output_type,func=func)
            # txt.append(ocr)
            image_to_pdf_or_ocr = pytesseract.image_to_pdf_or_hocr(path,lang=lang,config=config,extension=extension)
            f = open("%s.%s"%(path,extension), "w+b") # /tmp/hello.jpg.pdf will be saved
            f.write(bytearray(image_to_pdf_or_ocr))
            f.close()
            s3.upload_file("%s.%s"%(path,extension), BUCKET_NAME, "%s.%s"%(name,extension))

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
            
            image_to_pdf_or_ocr = pytesseract.image_to_pdf_or_hocr("/tmp/img",lang=lang,config=config,extension=extension)
            f = open("/tmp/tesseroid.%s"%extension, "w+b")
            f.write(bytearray(image_to_pdf_or_ocr))
            f.close()
            s3.upload_file("/tmp/tesseroid.%s"%extension, BUCKET_NAME, "tesseroid.%s"%extension)
    
    return json.dumps("check thine bucket")