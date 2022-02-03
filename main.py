import os
import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_area_id_hh(city):
    area_link = "https://api.hh.ru/suggests/areas/"
    params = {
        "text": city
    }
    response = requests.get(area_link, params)
    response.raise_for_status()
    return response.json().get("items")[0].get("id")


def get_area_id_sj(city):
    area_link = "https://api.superjob.ru/2.0/towns/"
    params = {
        "keyword": city
    }
    response = requests.get(area_link, params)
    response.raise_for_status()
    return response.json().get("objects")[0].get("id")


def compare_demand_hh_pl(city_id, popular_pl):
    pl_statistic = {}
    for pl in popular_pl:
        info_results = predict_rub_salary_hh(city_id, pl)
        pl_statistic.update({
            f"{pl}": {
                "vacancies_found": info_results[2],
                "vacancies_processed": info_results[1],
                "average_salary": info_results[0]
            }})
    return pl_statistic


def compare_demand_sj_pl(city_id, popular_pl):
    pl_statistic = {}
    for pl in popular_pl:
        info_results = predict_rub_salary_sj(city_id, pl)
        pl_statistic.update({
            f"{pl}": {
                "vacancies_found": info_results[2],
                "vacancies_processed": info_results[1],
                "average_salary": info_results[0]
                    }})
    return pl_statistic


def predict_rub_salary_hh(city_id, pl):
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
        for vacancy in (response.json().get("items")):
            if vacancy.get("salary") is not None and vacancy.get("salary").get("currency") == "RUR":
                min_salary = vacancy.get("salary").get("from")
                max_salary = vacancy.get("salary").get("to")
                if min_salary is not None and max_salary is not None:
                    average_results.append(round((min_salary + max_salary) / 2))
                elif min_salary is not None:
                    average_results.append(round(min_salary * 1.2))
                else:
                    average_results.append(round(max_salary * 0.8))
    return round(sum(average_results) / len(average_results)), len(average_results), response.json().get("found")


def predict_rub_salary_sj(city_id, pl):
    vacancies_page = 0
    average_results = []
    check_results = True
    vacancies_link = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": os.getenv("X-API-APP-ID")
    }
    while check_results:
        params = {
            "keyword": pl,
            "town": city_id,
            "page": vacancies_page,
            "count": "20"
        }
        response = requests.get(vacancies_link, params, headers=headers)
        response.raise_for_status()
        check_results = response.json().get("more")
        vacancies_page += 1
        for vacancy in response.json().get("objects"):
            min_salary = vacancy.get("payment_from")
            max_salary = vacancy.get("payment_to")
            if vacancy.get("currency") == "rub" and min_salary != 0 or max_salary != 0:
                if min_salary != 0 and max_salary != 0:
                    average_results.append(round((min_salary + max_salary) / 2))
                elif min_salary != 0:
                    average_results.append(round(min_salary * 1.2))
                else:
                    average_results.append(round(max_salary * 0.8))
    return round(sum(average_results) / len(average_results)), len(average_results), response.json().get("total")


def create_table_job(table_values, vacancy_source):
    heading_row = [["Язык программирование", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for key, value in table_values.items():
        iter_language = [key]
        iter_language.extend(value.values())
        heading_row.append(iter_language)
    table_date = AsciiTable(heading_row, vacancy_source)
    print(table_date.table)


def main():
    popular_pl = ["Python", "Java", "Javascript", "Golang", "C++", "php"]
    load_dotenv()
    city_id_hh = get_area_id_hh(os.getenv("CITY"))
    city_id_sj = get_area_id_sj(os.getenv("CITY"))
    create_table_job(compare_demand_sj_pl(city_id_sj, popular_pl), f"SuperJob {os.getenv('CITY')}")
    create_table_job(compare_demand_hh_pl(city_id_hh, popular_pl), f"HeadHunter {os.getenv('CITY')}")



if __name__ == "__main__":
    main()
