# list of functions
1. get_tesseract_version
2. image_to_string: image,lang,config,nice,output_type(string,dict,byte),timeout
3. image_to_boxes
4. image_to_data 
5. image_to_osd 
6. image_to_pdf_or_hocr
7. run_and_get_output 
8.
# fields
image, lang, config, 
# architecture
1. separate endpoint for each
2. Parameters send through form-data
3. 
# approaches
1. Lambda proxy: Parameter extraction in lambda.
2. Lambda+API gateway: build templates in API gateway.
3. Find in both cases if single lambda can be used.
4. 
# integration request> 
```
{
    "image" : $input.json("$.image"),
    "lang" : $input.json("$.lang"),
    "config" : $input.json("$.config"),
    "nice" : $input.json("$.nice"),
    "output_type" : $input.json("$.output_type"),
    "timeout" : $input.json("$.timeout")
    
}
```
# Types of POST requests
They are set by header -H 'Content-Type:____'
1. **application/x-www-form-urlencoded**: Default and supported by browser. Used for text.     
~~~  -d 'image=https%3A%2F%2Fmedia3.giphy.com%2Fmedia%2FD0Uhua2Z1PC8w%2Fsource.gif&lang=eng'
~~~

2. **application/JSON**: form data can't be JSONified without javascript    
```
-d '{
	"image":"https://media3.giphy.com/media/D0Uhua2Z1PC8w/source.gif",
	"lang":"eng"
    }' 
```

3. **multipart/form-data**: Files can be sent. Both files and text fields have -F instead of -D. Not supported by API gateway. It will need S3.
```
-F image=@/home/shardul/sci_capthas/1.jpeg \
-F lang=eng
```
## mapping template to convert x-www-form to JSON
```
{
    #foreach( $token in $input.path('$').split('&') )
        #set( $keyVal = $token.split('=') )
        #set( $keyValSize = $keyVal.size() )
        #if( $keyValSize >= 1 )
            #set( $key = $util.urlDecode($keyVal[0]) )
                #if( $keyValSize >= 2 )
                    #set( $val = $util.urlDecode($keyVal[1]) )
                #else
                    #set( $val = '' )
                #end
            "$key": "$val"#if($foreach.hasNext),#end
        #end
    #end
}
```
## template to extract fields
fields image(array), lang, config
```
{
    "image": {
        
    }
}