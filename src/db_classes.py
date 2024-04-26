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
            cur.execute("CREATE TABLE if NOT EXISTS vacancies (vacancy_id int PRIMARY KEY, name text, salary_from int, salary_to int, employer_id int REFERENCES employers(employer_id))")

            cur.execute("TRUNCATE employers, vacancies")

            for item in employers:
                cur.execute("INSERT INTO employers (employer_id, name) VALUES (%s, %s)", item)

            for item in vacancies:

                row = [int(item['id']),
                        item['name'],
                        item['salary']['from'] if item['salary'] else None,
                        item['salary']['to'] if item['salary'] else None,
                        item['employer']['id']]

                cur.execute("INSERT INTO vacancies (vacancy_id, name, salary_from, salary_to, employer_id) VALUES (%s, %s, %s, %s, %s)", row)