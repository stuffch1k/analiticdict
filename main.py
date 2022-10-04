import csv
import re
import math
import heapq

file_name="C:\\vacanc.csv"
#file_name=input()
File=open(file_name, encoding='utf_8_sig')
reader=[row for row in csv.reader(File)]
titles=reader.pop(0)

filtered=[x for x in reader if len(x)==len(titles) and not '' in x]

dic_vacancy=[]

def clear(value):
    return ' '.join(re.sub(r"<[^>]+>", '', value).split())

for row in filtered:
    dic={}
    for i in range(0,len(row)):
        if row[i].find("\n")!=-1:
            ans=[clear(el) for el in row[i].split("\n")]
        else:
            ans=clear(row[i])
        dic[titles[i]]=ans
    dic_vacancy.append(dic)


#dic_vacancy['key_skills'] это либо массив строк, либо строка
#в некоторых строках есть траблы: тк сплитили изначально по \n, key_skills остался неотработан по другим знакам
#нужно сплитить еще раз или это одно значение key_skills?
#ок препдоложим это все один скилл, сплитить больше не будем
new_dic_vacancy = []
#новый словарь где не валютные вакансии
for i in range(len(dic_vacancy)):
    for key, value in dic_vacancy[i].items():
        if key=='salary_currency' and value=='RUR':
            new_dic_vacancy.append(dic_vacancy[i])
#добавим информацию о средней зп. тк размер менять нельзя, храним в ячейке currency
#rename key?
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        new_dic_vacancy[i]['salary_currency']=math.floor((int(new_dic_vacancy[i]['salary_from'])+int(new_dic_vacancy[i]['salary_to']))/2)

cities_list={}
cities_count=len(new_dic_vacancy)
skills={}
# считаем количесвто городов 
# парсим скилы и считаем их в словаре
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        if key=='area_name':
            if value in list(cities_list.keys()):
                cities_list[value]+=1
            else:
                cities_list[value]=1
        if key=='key_skills':
            if type(value).__name__ == 'list':
                for element in new_dic_vacancy[i][key]:
                    if element in list(skills.keys()):
                        skills[element]+=1
                    else:
                        skills[element]=1
            else:
                if new_dic_vacancy[i][key] in list(skills.keys()):
                        skills[new_dic_vacancy[i][key]]+=1
                else:
                    skills[new_dic_vacancy[i][key]]=1

# cheking
# for i in range(len(new_dic_vacancy)):
#     for key, value in new_dic_vacancy[i].items():
#         print(f'{key}: {value}')
#     #print()
# print(len(dic_vacancy))
# print(len(new_dic_vacancy))

