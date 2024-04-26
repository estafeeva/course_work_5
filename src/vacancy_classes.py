import re
from datetime import datetime

DT_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
class Vacancy:
    """класс для работы с вакансиями"""

    def __init__(self, name, link, salary_from, salary_to, city, requirements, published_at):
        self.name = name
        self.link = link
        #self.salary = salary
        self.city = city
        self.requirements = requirements
        if salary_from:
            self.salary_from = salary_from
        else:
            self.salary_from = 0

        if salary_to:
            self.salary_to = salary_to
        else:
            self.salary_to = 0
        self.__published_at = datetime.strptime(published_at, DT_FORMAT)


    def valid_salary(self):
        """Метод валидации данных: проверка, указана или
        нет зарплата, и вывод информации по вакансии"""

        if self.salary_from == 0 and self.salary_to == 0:
            return (f"\n{'-' * 50}\n\n"
                f"Название вакансии: {self.name}\n"
                f"Город: {self.city}\n"
                f"Заработная плата: Зарплата не указана...\n"
                    f"Требования: {re.sub(r'<.*?>', '', self.requirements)}\n"
                f"Ссылка на вакансию: {self.link}")
        else:
            return (f"\n{'-' * 50}\n\n"
                f"Название вакансии: {self.name}\n"
                f"Город: {self.city}\n"
                f"Заработная плата: {self.salary_from}-{self.salary_to}.\n"
                f"Требования: {re.sub(r'<.*?>', '', self.requirements) if self.requirements else 'Нету'}\n"
                f"Ссылка на вакансию: {self.link}")

    def compare_salary(self, other):
        """метод сравнения вакансий между собой по зарплате"""
        if self.salary_from == 0 and other.salary_from == 0:
            return f"Минимальные зарплата не указаны."
        elif self.salary_from < other.salary_from:
            return f"Минимальная зарплата по вакансии {other.name} больше чем по вакансии {self.name}."
        elif self.salary_from > other.salary_from:
            return f"Минимальная зарплата по вакансии {self.name} больше чем по вакансии {other.name}."
        else:
            return f"Минимальные зарплаты по вакансиям {self.name} и {other.name} одинаковы."

    def __repr__(self):
        return f"Вакансия {self.name}, опубликована {self.__published_at.strftime("%d.%m.%Y %H:%M")}"

testdatetime = "2024-02-26T18:42:12+0300"

manager = Vacancy('Менеджер', "", 40000, False, "Москва", "Работать", testdatetime)
developer = Vacancy('Программист', "", 60000, 110000, "Москва", "Писать код", testdatetime)
driver = Vacancy('Водитель', "", 0, 0, "Москва", "Писать код", testdatetime)

#print(driver.valid_salary())
#print(manager.compare_salary(developer))