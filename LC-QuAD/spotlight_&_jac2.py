import csv
import json
import requests
from evaluation import read_LCQUAD
from convert import validate_ant,template_convert

def match(list_1,list_2):
    combined_list=[]
    set_1 = set(list_1)
    set_2 = set(list_2)
    
    combined_list= list(set_1 | set_2)
    if 'http://dbpedia.org/resource/' in combined_list:
      combined_list.remove('http://dbpedia.org/resource/')
    return combined_list


def get_entity(text):
    headers = {
        'accept': 'application/json',
    }

    params = (
        ('text', text),
    )

    response = requests.get('https://api.dbpedia-spotlight.org/en/candidates', headers=headers, params=params)
    j=response.content.decode("utf-8")
    data = json.loads(j)
    data=data.get('annotation').get('surfaceForm')
    ext_ent=[]
    if isinstance(data, dict):
        ext_ent.append(data['resource']['@uri'])
    else:
        for i in data:
            if i['resource']['@uri'] not in ext_ent:
                ext_ent.append(i['resource']['@uri'])
    for i in range(len(ext_ent)):
        ext_ent[i]=validate_ant(ext_ent[i])
        ext_ent[i]='http://dbpedia.org/resource/'+ext_ent[i]
    return ext_ent


def one_entity(inputq,matchedq):
    outputq=[]
    L=[]
    try:
        L=get_entity(inputq)
        print("api: "+L)
    except:
        pass
    start=matchedq.find('<')
    end=matchedq.find('>')+1+(len(inputq)-len(matchedq))
    name=inputq[start:end]
    name=name.strip().title().replace(" ","_")
    name=validate_ant(name)
    print("jac: "+name)
    name='http://dbpedia.org/resource/'+name
    outputq=match(L,[name])
    return outputq

def two_entity(inputq,matchedq):
    outputq=[]
    L=[]
    try:
        L=get_entity(inputq)
        print("api: ",L)
    except:
        pass
    S1=matchedq.lower().split(" ")
    S2=inputq.lower().split(" ")
    L1=[]
    i=0
    while i<len(S2):
        word=S2[i]
        if word not in S1:
            G=""
            while i<len(S2) and S2[i] not in S1:
                G+=S2[i]
                G+=" "
                i+=1
            i-=1
            if len(G):
                L1.append(G)
        i+=1
    for i in range(len(L1)):
        L1[i]=L1[i].strip().title().replace(" ","_")
        L1[i]=validate_ant(L1[i])
        L1[i]='http://dbpedia.org/resource/'+L1[i]
        print("jac: ",L1)
    outputq=match(L,L1)
    return outputq

questions=read_LCQUAD()
    #questions=evaluation.read_LCQUAD2()
    #questions=evaluation.read_QALD7()


    
coun=1
que=[]
sump=0
sumr=0
with open('Spotlight_&_jac2.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        try:    
            p_relation=0
            r_relation=0
            p_entity=0
            r_entity=0
            print(coun)
            question[0]=question[0].replace("?","")
            print(question[0])
            temp=template_convert(question[0],question[3])
            if "<A>" in temp and "<B>" in temp:
                entities = two_entity(question[0],temp)
            elif "<A>" in temp or "<B>" in temp:
                entities = one_entity(question[0],temp)
            else:
                try:
                    entities = get_entity(question[0])
                except:
                    entities=[]

            print(entities)
            

            
            numberSystemEntities=len(question[3])
            intersection= set(question[3]).intersection(entities)
            if numberSystemEntities!=0 and len(entities)!=0 :
                p_entity=len(intersection)/len(entities)
                r_entity=len(intersection)/numberSystemEntities
            sump+=p_entity
            sumr+=r_entity
            question.append(entities)
            question.append(p_entity)   
            question.append(r_entity)
            question.append(temp)   
            coun=coun+1
            que.append(question)
            writer.writerow([question[0],question[-1],question[3],question[4],question[5],question[6]])
            Precision=sump/coun
            Recall=sumr/coun
            f=(2 * Precision * Recall) / (Precision + Recall)
            print(" precision score: ",Precision)
            print(" recall score: ",Recall)
            print(" F-Measure score: ",f)
        except Exception as e:
            print("ERROR at ",coun)
            print(e)
            break


print("FINAL: \n")
Precision=sump/coun
Recall=sumr/coun
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)