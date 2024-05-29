# DocOwl Model deployment


### Installation
    install potery
    ''' pip install potery'''
    Install and build envoiranment
    ''' potery install '''
    Download Model File
        1. create chatmodel directory
        2. python md.py
    Run API
    ''' potery run python app.py'''


### Create docker image  
    install potery
    ''' pip install potery'''
    Install and build envoiranment
    ''' potery install '''
    Download Model File
        1. create chatmodel directory
        2. python md.py
    Build docker
    docker build -t docowl:latest .
    docker run -p 7860:7860 docowl:latest

    Intrective docker conatiner run
    docker run -it -p 7860:7860 docowl:latest /bin/bash
