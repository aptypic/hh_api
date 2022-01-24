import requests


def main():
    hh_link = "https://api.hh.ru/vacancies/"
    params = {
        "text": "программист"
    }
    response = requests.get(hh_link, params)
    response.raise_for_status()
    for i in response.json().get("items"):
        print(i.get("name"))


if __name__ == "__main__":
    main()
