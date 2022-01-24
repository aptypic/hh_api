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


def find_job(city_id, pl):
    vacancies_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": f"{pl}",
        "area": city_id,
        "period": 30,
        "per_page": 100
    }
    response = requests.get(vacancies_link, params)
    response.raise_for_status()
    return response.json().get("found")


def compare_demand_pl(city_id, popular_pl, pl_statistic):
    for pl in popular_pl:
        pl_statistic[pl] = find_job(city_id, pl)
    print(pl_statistic)


def main():
    popular_pl = ["Python", "Java", "Javascript", "Golang", "C++", "Rust", "php"]
    pl_statistic = {}
    load_dotenv()
    city_id = get_area_id(os.getenv("CITY"))
    compare_demand_pl(city_id, popular_pl, pl_statistic)


if __name__ == "__main__":
    main()
