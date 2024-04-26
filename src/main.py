import json
from src.vacancy_method import VacancyDataSaver
from src.API_classes import VacancyFromHH
from src.vacancy_classes import Vacancy
from db_classes import fill_database

i = VacancyFromHH.get_vacancy_from_hh()
list_of_employers_all = [item['employer']["id"] for item in i]
list_of_employers = list_of_employers_all[0:10]
print(list_of_employers)

print("Введите количество желаемых вакансий: ")
data_input_N = int(input())
data_dict = VacancyFromHH.get_vacancy_from_hh(data_input_N, list_of_employers)

"""
c = VacancyDataSaver()
data_dict_2 = c.get_data_from_file()"""

data_classes = [Vacancy(item['name'],
                        item['url'],
                        item['salary']['from'] if item['salary'] else None,
                        item['salary']['to'] if item['salary'] else None,
                        item['area']['name'],
                        item['snippet']['requirement'],
                        item["published_at"]
                        ) for item in data_dict]

data_employers = set([(int(item["employer"]["id"]),
                   item["employer"]["name"]
                   ) for item in data_dict])

[print(item) for item in data_classes]


b = VacancyDataSaver()
new_vacancy = {'name': "{Художник}",
                'url': "нет ссылки",
                "salary": {
                    "from": 0,
                    "to": 0
                },
                "area": {"name": "Москва"},
                "snippet": {"requirements": "Рисовать картины."},
                "published_at": "2024-02-26T18:42:12+0300"
                }
b.add_vacancies_to_file(data_dict)

fill_database(data_dict, data_employers)

"""b.add_vacancies_to_file([new_vacancy])
print("Хотите ли вы удалить данные? y/n")
answer = input()
if answer == "y":
    b.del_data()
else:
    pass"""