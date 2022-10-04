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
for i in range(len(dic_vacancy)):
    for key, value in dic_vacancy[i].items():
        dic_vacancy[i]['salary_currency']=math.floor((int(dic_vacancy[i]['salary_from'])+int(dic_vacancy[i]['salary_to']))/2)

#cheking
# for i in range(len(dic_vacancy)):
#     for key, value in dic_vacancy[i].items():
#         if type(dic_vacancy[i]['key_skills']).__name__ != 'list':
#             print(f'{key}: {value}')
    #print()
print('OK')