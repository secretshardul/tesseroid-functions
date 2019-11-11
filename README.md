# POST request example
```sh
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://i.imgur.com/zGRdhAT.jpg"
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://i.etsystatic.com/16235847/r/il/b1e59b/2011957531/il_570xN.2011957531_p39l.jpg"
# gif
curl -X POST https://mcbn0jkd8l.execute-api.eu-central-1.amazonaws.com/dev/ocr -d "https://media.giphy.com/media/xULW8tKMugzsC8A4MM/giphy.gif"
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

# uninstall
serverless plugin uninstall --n serverless-python-requirements
```

# shenanigans
1. don't upgrade python runtime to 3.7, it's causing PIL error