# POST request example
```sh
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://i.imgur.com/zGRdhAT.jpg"
# hebrew post
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQdUtag90lRt2LVqV0MCHiO-w-FCbEpkjSOrOaNB6_3wVvr1kj0"
```

# API architecture for POST 
1. parameters: config,extension
2. Use form-data instead of x-www-form because it supports files also.
3. pytesseract directly accepts image files, not URLs. But tesseract command line takes url path

# serverless plugins
```sh
sls plugin install -n serverless-python-requirements
sls plugin install -n serverless-pseudo-parameters
```