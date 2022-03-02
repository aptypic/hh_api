# Compare of IT vacancies
This project takes info from HeadHunter and Superjob, collects data and compare results (e.g. keyword, vacancies found, vacancies processed and average sallary)
## Requirements
Before launch must be installed:  
 - python-dotenv==0.19.2
 - requests==2.26.0
 - terminaltables==3.1.10
 
## How to install
Python3 should be already installed. Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
## How to start
For specify city should to create .env file in the same directory. SuperJob require token unlike Headhunter, so you need to register your app and get the token. Then to add all in .env file:
```
CITY="Москва"
X-API-APP-ID="token"
```
After fill .env to should launch main.py

<img width="699" alt="image" src="https://user-images.githubusercontent.com/56154540/156317437-4dd69c8c-ebda-4acc-9fed-e571ae3990d1.png">
