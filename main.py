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
#в некоторых строках есть траблы: тк сплитили изначально по \n, key_skills остался неотработан по точкам/двоеточиям
#нужно сплитить еще раз или это одно значение key_skills?
new_dic_vacancy = []
for i in range(len(dic_vacancy)):
    for key, value in dic_vacancy[i].items():
        if type(dic_vacancy[i]['key_skills']).__name__ != 'list':
            print(f'{key}: {value}')
    #print()
print('OK')