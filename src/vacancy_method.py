from abc import ABC, abstractmethod
import json

class AbstractVacancyMethod(ABC):
    """абстрактный класс, который обязывает реализовать методы
    для добавления вакансий в файл, получения данных из файла по
    указанным критериям и удаления информации о вакансиях"""

    @abstractmethod
    def add_vacancies_to_file(self):
        pass

    @abstractmethod
    def get_data_from_file(self):
        pass

    @abstractmethod
    def del_data(self):
        pass

class VacancyDataSaver(AbstractVacancyMethod):
    """
    класс для сохранения информации о вакансиях в JSON-файл"""


    def add_vacancies_to_file(self,b: list):
        list_of_dict_of_vacancies = self.get_data_from_file()
        list_of_dict_of_vacancies.extend(b) #добавляет список вакансий

        with open('Vacancies_JSON.json', 'w', encoding="UTF-8") as f:
            json.dump(list_of_dict_of_vacancies, f, indent=2, ensure_ascii=False)

    def get_data_from_file(self):
        with open('Vacancies_JSON.json', 'r', encoding="UTF-8") as f:
            return json.load(f)

    def del_data(self):
        with open('Vacancies_JSON.json', 'w', encoding="UTF-8") as f:
            f.write('[]')
