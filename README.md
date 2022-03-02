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
![image](https://user-images.githubusercontent.com/56154540/152491097-fc5caa77-84cc-4a8d-af0e-07b78b26d700.png)
