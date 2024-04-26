"""Скрипт для заполнения данными таблиц в БД Postgres."""
import psycopg2


def fill_database(vacancies, employers):
    """
    функция получает список вакансий и список выбранных работодателей,
    создает таблицы с заданными полями, если они ранее не были созданы,
    заполняет данные в таблицы с вакансиями и таблицы с работодателями
    """
    conn_params = {
      "host": "localhost",
      "database": "hh_vacancies",
      "user": "postgres",
      "password": "12345678"
    }
    with psycopg2.connect(**conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE TABLE if NOT EXISTS employers (employer_id int PRIMARY KEY, name text)")
            cur.execute("CREATE TABLE if NOT EXISTS vacancies (vacancy_id int PRIMARY KEY, name text, salary_from int, salary_to int, employer_id int REFERENCES employers(employer_id), vacancy_url text)")

            cur.execute("TRUNCATE employers, vacancies")

            for item in employers:
                cur.execute("INSERT INTO employers (employer_id, name) VALUES (%s, %s)", item)

            for item in vacancies:

                row = [int(item['id']),
                        item['name'],
                        item['salary']['from'] if item['salary'] else None,
                        item['salary']['to'] if item['salary'] else None,
                        item['employer']['id'],
                        item['url']]

                cur.execute("INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, employer_id, vacancy_url) VALUES (%s, %s, %s, %s, %s, %s)", row)

class DBManager():
    """
    класс для работы с данными в БД
    """

    def __init__(self):
        self.params = {
      "host": "localhost",
      "database": "hh_vacancies",
      "user": "postgres",
      "password": "12345678"
    }


    def get_function(self, query):
        with psycopg2.connect(**self.params) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании"""
        self.get_function("""
                SELECT employers.name, COUNT(*) FROM vacancies
                INNER JOIN employers USING(employer_id)
                GROUP BY employers.name
                """)

    def get_all_vacancies(self):
        """
        получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        self.get_function("""
                SELECT employers.name, vacancies.name, vacancies.salary_from,
                vacancies.vacancy_url FROM vacancies
                INNER JOIN employers USING(employer_id)
                ORDER BY employers.name
                """)

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        self.get_function("""
                SELECT AVG(salary_from) FROM vacancies
                """)

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        self.get_function("""
                SELECT name, salary_from FROM vacancies
                WHERE salary_from>(SELECT AVG(salary_from) FROM vacancies)
                ORDER BY salary_from
                """)

    def get_vacancies_with_keyword(self, your_text):
        """получает список всех вакансий, в названии которых содержатся
        переданные в метод слова, например python"""
        self.get_function(f"""
                SELECT name FROM vacancies
                WHERE name LIKE('%{your_text}%')
                """)
