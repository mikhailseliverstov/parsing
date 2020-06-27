from pymongo import MongoClient
import json
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancies']

vacancies = db['vacancies']


def import_vac(vacancies, file_name):
    with open(file_name, "r") as f:
        data = json.load(f)

    for k, v in data.items():
        vacancies.insert_many(data)


def get_vacancies(vacancies, num: int) -> []:
    res = []
    vacs = vacancies.find({'vacancy_money.0': {'$gt': num}, 'vacancy_money.2': 'руб.'})
    for vac in vacs:
        res.append(vac)
    return res



import_vac(vacancies, "hhru.json")


vac1 = get_vacancies(vacancies, 150000)
for v in vac1:
    pprint(v)

client.close()
