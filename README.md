# DocOwl Model deployment
## Badges  
[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)  
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://choosealicense.com/licenses/gpl-3.0/)  
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](https://choosealicense.com/licenses/gpl-3.0/)  

# Project Title  
A brief description of what this project does and who it's for  


### Installation
  install potery
  ~~~bash  
  pip install potery
  potery install 
  
~~~ 
  Download Model File
  ~~~bash  
        mkdir chatmodel
        python md.py
        potery run python app.py
  ~~~ 


### Create docker image  
  install potery
     pip install potery modelscope 


  
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

