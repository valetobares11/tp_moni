# Technical test for Moni Online
Develop a website that allows users to make loan applications.
An administration site should also be developed where loan requests can be listed with the option to edit and delete them. 
This site can only be accessed by administrator users.

## Author
Valentin Tobares

## Instructions for running docker 
1. Install docker
2. compile the image with the following command: "docker build -t tp_moni_image ."
3. run the image with this command : "docker run -p 8000:8000 tp_moni_image."

## Instructions to run locally
1. Have python 3.8 or later installed.
2. run the command "pip install -r requirements.txt".
3. run the following command "python3 manage.py runserver". 

## Instructions to run the tests
1. Run the command: "python3 manage.py test".

## Clarifications
1. The default user is email: "valetobares11@gmail.com" and password: "123".
