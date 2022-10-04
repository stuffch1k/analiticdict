import csv
import re
import math
import heapq

def count_pad(x,name):
    if 5 <= x <= 20 or 5 <= x % 10 <= 9 or x % 10 == 0:
        if name=='раз':
            return 'раз'
        elif name=='ваканси':
            return 'й'
        else:
            return 'рублей'
    elif x % 10 == 1:
        if name=='раз':
            return 'раз'
        elif name=='ваканси':
            return 'я'
        else:
            return 'рубль'
    else:
        if name=='раз':
            return 'раза'
        elif name=='ваканси':
            return 'и'
        else:
            return 'рубля'
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
salary_cities_list={}
cities_count=len(new_dic_vacancy)
skills={}

# считаем количесвто городов 
# парсим скилы и считаем их в словаре
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        if key=='area_name':
            salary_cities_list[value]=0
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
skills_count=len(skills)
#начинаем составлять рейтинг по зарплатам
hight_salary=[]
low_salary=[]
salary=[]
max=0
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        if new_dic_vacancy[i]['salary_currency']>=max and new_dic_vacancy[i]['area_name']:
            if cities_list[new_dic_vacancy[i]['area_name']]/cities_count>=0.01:
                salary.append(new_dic_vacancy[i]['salary_currency'])
# составляем список- топ макс и мин зп
salary=set(salary)
low_salary=list(salary)
low_salary.sort()
hight_salary=low_salary.copy()
hight_salary.reverse()
low_salary=low_salary[0:10]
hight_salary=hight_salary[0:20]

best_salary=[]
worst_salary=[]
#формируем рейтинг
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        if int(new_dic_vacancy[i]['salary_currency']) in low_salary:
            worst_salary.append(new_dic_vacancy[i])
        if int(new_dic_vacancy[i]['salary_currency']) in hight_salary:
            best_salary.append(new_dic_vacancy[i])

best_array=[]
temp=''
for dic in best_salary:
    if temp != dic['name']:
        best_array.append(dic)
    temp=dic['name']
worst_array=[]
temp=''
for dic in worst_salary:
    if temp != dic['name']:
        worst_array.append(dic)
    temp=dic['name']
# получаем два массива словарей: с лучшими зп и худшими зп
#сортируем скиллсы по возрастанию-вывод в обратном порядке
sorted_skills=dict(sorted(skills.items(), key=lambda item: item[1]))

sorted_best_array=sorted(best_array,key=lambda d: d['salary_currency'])
sorted_best_array.reverse()
sorted_worst_array=sorted(worst_array,key=lambda d: d['salary_currency']) 

# приступаем к формированию рейтинга  зп по городам тошько суммируем пока
cities_salary={}
for i in range(len(new_dic_vacancy)):
    for key, value in new_dic_vacancy[i].items():
        if key=='area_name' and cities_list[new_dic_vacancy[i]['area_name']]/cities_count>=0.01:
            if value in list(cities_salary.keys()):
                cities_salary[value]+=new_dic_vacancy[i]['salary_currency']
            else:
                cities_salary[value]=new_dic_vacancy[i]['salary_currency']
# вычисляем средню зп (тупо делим)
flag=0
for i in range(len(sorted_best_array)):
    for key,value in sorted_best_array[i].items():
        if key=='area_name' and salary_cities_list[value]==0:
            salary_cities_list[value]=sorted_best_array[i]['salary_currency']
            
sorted_salary=dict(sorted(salary_cities_list.items(), key=lambda item: item[1]))
items = list(sorted_salary.items())
new_salary_list = {k: v for k, v in reversed(items)}
            # print(cities_list[value])
# for key, value in cities_salary.items():
#     cities_salary[key]=math.floor(cities_salary[key]/cities_list[key])
# # sorting. dont forget print reversed
# sorted_cities_salary=dict(sorted(cities_salary.items(), key=lambda item: item[1]))

# create dictionary with number of average salary
average_salary_number={}
for i in range(len(new_dic_vacancy)):
    for key, value in new_salary_list.items():
        if new_dic_vacancy[i]['area_name']==key and new_dic_vacancy[i]['salary_currency']==value and cities_list[new_dic_vacancy[i]['area_name']]/cities_count>=0.01:
            if key in average_salary_number.keys():
                average_salary_number[key]+=1
            else:
                average_salary_number[key]=1

# вывод в формате:  
# for dic in sorted_best_array:
#     print(f"{dic['name']} в компании {dic['employer_name']} - {dic['salary_currency']} (г.{dic['area_name']})")
#     print()
# print('worst')
# for dic in sorted_worst_array:
#     print(f"{dic['name']} в компании {dic['employer_name']} - {dic['salary_currency']} (г.{dic['area_name']})")
#     print()
# cheking
# for i in range(len(new_dic_vacancy)):
#     for key, value in new_dic_vacancy[i].items():
#         print(f'{key}: {value}')
#     #print()
print('Самые высокие зарплаты:')
i=1
for dic in sorted_best_array:
    if i<=10:
        pad=count_pad(value,'rub')
        print(f'''    {i}) {dic['name']} в компании "{dic['employer_name']}" - {dic['salary_currency']} {pad} (г. {dic['area_name']})''')
    i+=1
print()
i=1
print('Самые низкие зарплаты:')
for dic in sorted_worst_array:
    if i<=10:
        pad=count_pad(value,'rub')
        print(f'''    {i}) {dic['name']} в компании "{dic['employer_name']}" - {dic['salary_currency']} {pad} (г. {dic['area_name']})''')
    i+=1
print()
print('Из 10 скиллов, самыми популярными являются:')
items = list(sorted_skills.items())
new_sorted_skills = {k: v for k, v in reversed(items)}
i=1
for key,value in new_sorted_skills.items():
    if i<=10:
        pad=count_pad(value,'раз')
        print(f'    {i}) {key} - упоминается {value} {pad}')
    i+=1
print()

print('Из 10 городов, самые высокие средние ЗП:')
# for key,value in cities_list.items():
#     print(f'{key}-{value}')
i=1
for key,value in new_salary_list.items():
    if i<=10 and value!=0:
        pad=count_pad(value,'rub')
        num=count_pad(average_salary_number[key],'ваканси')
        print(f'    {i}) {key} - средняя зарплата  {value} {pad} ({average_salary_number[key]} ваканси{num})')
        i+=1
print()
