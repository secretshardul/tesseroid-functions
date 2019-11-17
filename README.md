# POST request example
```sh
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://i.imgur.com/zGRdhAT.jpg"
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://i.etsystatic.com/16235847/r/il/b1e59b/2011957531/il_570xN.2011957531_p39l.jpg"
# webp- works
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://www.online-convert.com/downloadfile/e1faa392-54fc-4aa3-96e8-764b872f6c5f/180d9d302f6308358ec8b8faaed7e74e"
# tiff - works
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://www.online-convert.com/downloadfile/eefcbca6-e32f-4746-b48c-b79eab426c2d/5e98fef3ab27e890f09bb70257584ec0"
# gif- works
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://media3.giphy.com/media/D0Uhua2Z1PC8w/source.gif"

# hebrew post
curl -X POST  https://4a4tavwbnd.execute-api.us-east-1.amazonaws.com/dev/ocr -d "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdUtag90lRt2LVqV0MCHiO-w-FCbEpkjSOrOaNB6_3wVvr1kj0"

# multipart/form-data
curl -X POST \
  http://localhost:3000/ocr \
  -H 'content-type: multipart/form-data' \
  -F image=https://i.imgur.com/zGRdhAT.jpg \
  -F image=https://media3.giphy.com/media/D0Uhua2Z1PC8w/source.gif
```

# API architecture for POST 
1. parameters: config,extension
2. Use form-data instead of x-www-form because it supports files also.
3. pytesseract directly accepts image files, not URLs. But tesseract command line takes url path

# serverless plugins
```sh
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-pseudo-parameters

# uninstall
serverless plugin uninstall --n serverless-python-requirements
```
# error handling
In python code add 
```py
raise Exception("msg")
```
In method response add desired HTTP code, eg 400. In integration response add regex as "msg"(same as returned by lambda error) for given HTTP code. Add custom message in mapping template.
# shenanigans
1. don't upgrade python runtime to 3.7, it's causing PIL error- fixed with pipenv
2. 

