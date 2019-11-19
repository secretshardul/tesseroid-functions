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
    func="string"
    if event["lang"]!="":
        lang=event["lang"]
    if event["config"]!="":
        config=event["config"]
    if event["output_type"]!="":
        output_type=event["output_type"]
    if event["func"]!="":
        func=event["func"]
    
   
    txt=[]
    if(event["type"]=="img_file"):
        # zip file for batch
        file1=open(r"/tmp/img","wb")
        image=base64.b64decode(event["image"])
        file1.write(image)
        file1.close()  
        ocr = select_func("/tmp/img",lang=lang,config=config,output_type=output_type,func=func)
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
            ocr = select_func(path,lang=lang,config=config,output_type=output_type,func=func)
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
            ocr = select_func("/tmp/img",lang=lang,config=config,output_type=output_type,func=func)
            
            txt.append(str(ocr))
    
    return json.dumps(txt)
    
def select_func(image,lang,config,output_type,func):
    if (func=="string"):
        return pytesseract.image_to_string(image,lang=lang,config=config,output_type=output_type)
    elif (func=="boxes"):
        return pytesseract.image_to_boxes(image=image,config="box")
        # return image_to_boxes(image,lang,config,output_type)
    elif (func=="data"):
        return pytesseract.image_to_data(image,lang=lang,config=config,output_type=output_type)
    elif (func=="osd"):
        return pytesseract.image_to_osd(image,config=config,output_type=output_type) #no lang

# def image_to_boxes(image,lang,config,output_type):
#     config += ' batch.nochop makebox'
#     args = [image, 'box', lang, config, 0, 0]
#     return pytesseract.run_and_get_output(*args)
    
# if __name__=="__main__":
#     main(0,0)

