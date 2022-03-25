import os
import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def get_area_hh_id(city):
    area_link = "https://api.hh.ru/suggests/areas/"
    params = {
        "text": city
    }
    response = requests.get(area_link, params)
    response.raise_for_status()
    return response.json().get("items")[0].get("id")


def get_area_sj_id(city):
    area_link = "https://api.superjob.ru/2.0/towns/"
    params = {
        "keyword": city
    }
    response = requests.get(area_link, params)
    response.raise_for_status()
    return response.json().get("objects")[0].get("id")


def totalize_hh_results(city_id, popular_program_languages):
    program_languages_statistic = {}
    for program_language in popular_program_languages:
        average_salary = predict_hh_rub_salary(city_id, program_language)
        program_languages_statistic.update({
            f"{program_language}": {
                "vacancies_found": average_salary[2],
                "vacancies_processed": average_salary[1],
                "average_salary": average_salary[0]
            }})
    return program_languages_statistic


def totalize_sj_results(city_id, popular_program_languages):
    program_languages_statistic = {}
    for program_language in popular_program_languages:
        average_salary = predict_sj_rub_salary(city_id, program_language)
        program_languages_statistic.update({
            f"{program_language}": {
                "vacancies_found": average_salary[2],
                "vacancies_processed": average_salary[1],
                "average_salary": average_salary[0]
            }})
    return program_languages_statistic


def predict_hh_rub_salary(city_id, program_language):
    vacancies_page_number = 1
    vacancies_page = 0
    average_results = []
    vacancies_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": f"{program_language}",
        "area": city_id,
        "period": 30,
        "per_page": 100,
        "page": vacancies_page
    }
    while vacancies_page < vacancies_page_number:
        response = requests.get(vacancies_link, params)
        response.raise_for_status()
        headhunter_result = response.json()
        vacancies_page_number = headhunter_result.get("pages")
        vacancies_page += 1
        for vacancy in (headhunter_result.get("items")):
            if vacancy.get("salary") and vacancy.get("salary").get("currency") == "RUR":
                min_salary = vacancy.get("salary").get("from")
                max_salary = vacancy.get("salary").get("to")
                if min_salary and max_salary:
                    average_results.append(round((min_salary + max_salary) / 2))
                elif min_salary:
                    average_results.append(round(min_salary * 1.2))
                else:
                    average_results.append(round(max_salary * 0.8))
    return round(sum(average_results) / len(average_results)), len(average_results), headhunter_result.get("found")


def predict_sj_rub_salary(city_id, program_language):
    vacancies_page = 0
    average_results = []
    check_results = True
    vacancies_link = "https://api.superjob.ru/2.0/vacancies/"
    headers = {
        "X-Api-App-Id": os.getenv("X-API-APP-ID")
    }
    while check_results:
        params = {
            "keyword": program_language,
            "town": city_id,
            "page": vacancies_page,
            "count": "20"
        }
        response = requests.get(vacancies_link, params, headers=headers)
        response.raise_for_status()
        superjob_result = response.json()
        check_results = superjob_result.get("more")
        vacancies_page += 1
        for vacancy in superjob_result.get("objects"):
            min_salary = vacancy.get("payment_from")
            max_salary = vacancy.get("payment_to")
            if vacancy.get("currency") == "rub" and min_salary or max_salary:
                if min_salary and max_salary:
                    average_results.append(round((min_salary + max_salary) / 2))
                elif min_salary:
                    average_results.append(round(min_salary * 1.2))
                else:
                    average_results.append(round(max_salary * 0.8))
    return round(sum(average_results) / len(average_results)), len(average_results), superjob_result.get("total")


def create_job_table(table_values, vacancy_source):
    heading_row = [["Язык программирование", "Вакансий найдено", "Вакансий обработано", "Средняя зарплата"]]
    for key, value in table_values.items():
        iter_language = [key]
        iter_language.extend(value.values())
        heading_row.append(iter_language)
    table_date = AsciiTable(heading_row, vacancy_source)
    print(table_date.table)


def main():
    popular_program_languages = ["Python", "Java", "Javascript", "Golang", "C++", "php"]
    load_dotenv()
    city_hh_id = get_area_hh_id(os.getenv("CITY"))
    city_sj_id = get_area_sj_id(os.getenv("CITY"))
    create_job_table(totalize_sj_results(city_sj_id, popular_program_languages), f"SuperJob {os.getenv('CITY')}")
    create_job_table(totalize_hh_results(city_hh_id, popular_program_languages), f"HeadHunter {os.getenv('CITY')}")


if __name__ == "__main__":
    main()
