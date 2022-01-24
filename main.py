import os
import requests
from dotenv import load_dotenv


def get_area_id(city):
    area_link = "https://api.hh.ru/suggests/areas/"
    params = {
        "text": city
    }
    response = requests.get(area_link, params)
    response.raise_for_status()
    return response.json().get("items")[0].get("id")


def find_job(city_id):
    vacancies_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": "программист",
        "area": city_id,
        "period": 30,
        "per_page": 100
    }
    response = requests.get(vacancies_link, params)
    response.raise_for_status()
    for i in response.json().get("items"):
        print(i.get("name"))
    print(response.json().get("found"))


def main():
    load_dotenv()
    city = os.getenv("CITY")
    city_id = get_area_id(city)
    find_job(city_id)


if __name__ == "__main__":
    main()
