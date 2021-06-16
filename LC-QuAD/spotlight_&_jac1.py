import csv
import json
import requests
from evaluation import read_LCQUAD
from convert import validate_ant,template_convert


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
    return ext_ent

def one_entity(inputq,matchedq):
    outputq=[]
    try:
        L=get_entity(inputq)
        print("api: ",L)
    except:
        start=matchedq.find('<A>')
        end=matchedq.find('>')+1+(len(inputq)-len(matchedq))
        name =inputq[start:end]
        name=name.strip().title().replace(" ","_")
        name=validate_ant(name)
        print("jac: ",name)
        name='http://dbpedia.org/resource/'+name
        outputq.append(name)
        return outputq
    for i in range(len(L)):
        L[i]=validate_ant(L[i])
        L[i]='http://dbpedia.org/resource/'+L[i]
    return L

def two_entity(inputq,matchedq):
    try:
        L=get_entity(inputq)
        print("api: ",L)
    except:
        S1=matchedq.lower().split(" ")
        S2=inputq.lower().split(" ")
        L=[]
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
                    L.append(G)
            i+=1
        L[0]=L[0].strip().title().replace(" ","_")
        L[1]=L[1].strip().title().replace(" ","_")
        print(L)
        print("jac: ",L)

    for i in range(len(L)):
        L[i]=validate_ant(L[i])
        L[i]='http://dbpedia.org/resource/'+L[i]
    return L

questions=read_LCQUAD()
    #questions=evaluation.read_LCQUAD2()
    #questions=evaluation.read_QALD7()


    
coun=0
que=[]
sump=0
sumr=0
with open('Spotlight_&_jac1.csv',  mode='w' ) as results_file:
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
            else:
                entities = one_entity(question[0],temp)
            

            print(entities)
            coun+=1
            

            
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