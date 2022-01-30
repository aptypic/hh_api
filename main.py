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


def compare_demand_pl(city_id, popular_pl):
    pl_statistic = []
    for pl in popular_pl:
        info_results = predict_rub_salary(city_id, pl)
        pl_statistic.append({
            f"{pl}": {
                "vacancies_found": info_results[2],
                "vacancies_processed": info_results[1],
                "average_salary": info_results[0]
                    }})
    return pl_statistic


def predict_rub_salary(city_id, pl):
    vacancies_page_number = 1
    vacancies_page = 0
    average_results = []
    vacancies_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": f"{pl}",
        "area": city_id,
        "period": 30,
        "per_page": 100,
        "page": vacancies_page
    }
    while vacancies_page < vacancies_page_number:
        response = requests.get(vacancies_link, params)
        response.raise_for_status()
        vacancies_page_number = response.json().get("pages")
        vacancies_page += 1
        for i in (response.json().get("items")):
            if i.get("salary") is not None and i.get("salary").get("currency") == "RUR":
                min_salary = i.get("salary").get("from")
                max_salary = i.get("salary").get("to")
                if min_salary is not None and max_salary is not None:
                    average_results.append(round((min_salary + max_salary) / 2))
                elif min_salary is not None:
                    average_results.append(round(min_salary * 1.2))
                else:
                    average_results.append(round(max_salary * 0.8))
    return round(sum(average_results) / len(average_results)), len(average_results), response.json().get("found")


def main():
    popular_pl = ["Python", "Java", "Javascript", "Golang", "C++", "Rust", "php"]
    load_dotenv()
    city_id = get_area_id(os.getenv("CITY"))
    print(compare_demand_pl(city_id, popular_pl))
    # print(predict_rub_salary(city_id, popular_pl[0]))


if __name__ == "__main__":
    main()
