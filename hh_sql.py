import sqlite3
from datetime import datetime
from hh_requests import hh_search

#копия БД выложена в репозиторий GitHub
def save_data(data):
    # Подключение к базе данных
    conn = sqlite3.connect('dz17sqlite.db')
    # Создаем курсор
    cursor = conn.cursor()

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    #сохраняем в БД данные и результат запроса
    cursor.execute("insert into requests (date, search_str, vacans, aver_sal) \
    VALUES (?, ?, ?, ?)", \
    (now, data['request_text'], data['vacancies_total'], data['average_salary']))

    #находим значение ключа последней записи
    conn.commit()
    cursor.execute("select max(id) from requests")
    next_id = cursor.fetchone()[0]

    #добавляем записи в таблицу вакансий с ключом последнего запроса
    for item in data['key_skills']:
        cursor.execute("insert into req_skills (req_id, skills_name, skills_qnt) \
        VALUES (?, ?, ?)", \
        (next_id, item[0], item[1]))

    conn.commit()

    # печатаем журнал всех запросов из базы данных
    query = 'select r.id, r.date, s.skills_name from requests r, req_skills s where r.id = s.req_id'
    cursor.execute(query)
    while True:
        str = cursor.fetchone()
        if str != None:
            print(str)
        else:
            break

    cursor.close()
