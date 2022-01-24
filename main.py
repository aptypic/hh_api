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


def predict_rub_salary(city_id, pl):
    vacancies_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": f"{pl}",
        "area": city_id,
        "period": 30,
        "per_page": 100
    }
    response = requests.get(vacancies_link, params)
    response.raise_for_status()
    for i in (response.json().get("items")):
        if i.get("salary") is not None and i.get("salary").get("currency") == "RUR":
            min_salary = i.get("salary").get("from")
            max_salary = i.get("salary").get("to")
            if min_salary is not None and max_salary is not None:
                print(round((min_salary+max_salary)/2), i.get("salary").get("currency"))
            elif min_salary is not None:
                print(round(min_salary*1.2), i.get("salary").get("currency"))
            else:
                print(round(max_salary*0.8), i.get("salary").get("currency"))


def main():
    popular_pl = ["Python", "Java", "Javascript", "Golang", "C++", "Rust", "php"]
    pl_statistic = {}
    load_dotenv()
    city_id = get_area_id(os.getenv("CITY"))
    # compare_demand_pl(city_id, popular_pl, pl_statistic)
    predict_rub_salary(city_id, popular_pl[0])


if __name__ == "__main__":
    main()
