import json
import requests
import csv
import evaluation as evaluation
import re


def get_entity_falcon(text):
    headers = {
        'Content-Type': 'application/json',
    }

    params = (
        ('mode', 'long'),
    )

    data = '{"text":"<t>"}'
    data=data.replace("<t>",text)

    response = requests.post('https://labs.tib.eu/falcon/api', headers=headers, params=params, data=data)

    j=response.content.decode("utf-8")
    data = json.loads(j)
    data=data['entities']
    data=[i[0] for i in data]
    return data

if __name__ == "__main__":
    questions=evaluation.read_LCQUAD()
    #questions=evaluation.read_LCQUAD2()
    #questions=evaluation.read_QALD7()


    
count=0
notemp=0
que=[]
sump=0
sumr=0
with open('only_Falcon1.csv',  mode='w', encoding= 'unicode_escape') as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        #try:    
            p_relation=0
            r_relation=0
            p_entity=0
            r_entity=0
            print(count)
            print(question[0])
            #try:
            entities=[]
            try:
                entities = get_entity_falcon(question[0])
            except:
                try:
                    entities = get_entity_falcon(question[0])
                except:
                    pass
            
            

            print(entities)
            count+=1

            
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
            que.append(question)
            writer.writerow([question[0],question[3],question[4],question[5],question[6]])
            Precision=sump/count
            Recall=sumr/count
            f=(2 * Precision * Recall) / (Precision + Recall)
            print(" precision score: ",Precision)
            print(" recall score: ",Recall)
            print(" F-Measure score: ",f)


Precision=sump/count
Recall=sumr/count
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)