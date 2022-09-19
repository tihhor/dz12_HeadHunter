import requests
import pprint
import time
import json

# request_text = input('Введите запрос для поиска вакансий:')
request_text = ''

def  hh_search(request_text):
    url = 'https://api.hh.ru/vacancies'

    if request_text == '':
        request_text = 'Python AND Django'

    key_skills = {}
    vacancies_total = 0     #число найденных вакансий
    salary_total = 0        #суммарная зарплата вакансий - для расчета средней
    NUM_PAGES = 2           #MAX 20    #ограничение числа страниц поиска

    for page_number in range(NUM_PAGES):

        parameters = {
             'text': 'NAME:'+request_text,
             'per_page': 10,
             'page': page_number,
             'only_with_salary': True,
             'currency': 'RUR'
        }

        result = requests.get(url, params=parameters).json()

        # print('Страница:', page_number)
        # pprint.pprint(result)

        vacancies = result['items']     #получили список вакансий

        for vacancy in vacancies:
            url_vacancy = vacancy['url']
            result = requests.get(url_vacancy).json()   #запрашиваем данные по каждой вакансии
            salary = result['salary']

            if salary['currency'] == 'RUR' and not (salary['from'] is None and salary['to'] is None) :    #учитываем только вакансии с указанной зарплатой в рублях
                # print(result['key_skills'])
                # print(result['salary'])
                vacancies_total  += 1
                # вычисляем зарплату как среднее между верхним и нижним значением
                salary_start = 0 if salary['from'] is None else salary['from']
                salary_finish = salary_start if salary['to'] is None else salary['to']
                salary_total  += (salary_start+salary_finish)/2

                skills = result['key_skills']   #разбираем ключевые навыки
                for skill in skills:
                    item = skill['name']
                    if item in key_skills:
                        key_skills[item] += 1
                    else:
                        key_skills[item] = 1

                time.sleep(1)

    #print(key_skills)

    key_skills_sorted = sorted(key_skills.items(), key=lambda x: x[1], reverse=True)

    request_result = {}      #записвываем результаты в словарь

    request_result['request_text'] = request_text
    request_result['vacancies_total'] = vacancies_total
    request_result['average_salary'] = 0 if salary_total == 0 else round(salary_total/vacancies_total,-3)
    request_result['key_skills'] = key_skills_sorted[:3]

    #сохраняем словарь результатов в файл .json
    with open('request_result.json', "w", encoding="utf-8") as file:
        json.dump(request_result, file)

    # print('Результат сохранен в файле request_result.json')

    return (request_result)