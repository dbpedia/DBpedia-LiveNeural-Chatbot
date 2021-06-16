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


    
count=1
notemp=0
que=[]
sump=0
sumr=0
with open('only_Falcon_LCQUAD.csv',  mode='a+' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        if count>2671:
            try:    
                p_relation=0
                r_relation=0
                p_entity=0
                r_entity=0
                print(count)
                question[0]=question[0].replace("?","")
                print(question[0])
                temp=template_convert(question[0],question[3])
                try:
                    if "<A>" in temp and "<B>" in temp:
                        entities = get_entity_falcon(question[0])
                    else:
                        entities = get_entity_falcon(question[0])
                        if "<A>" not in temp and "<B>" not in temp:
                            notemp+=1
                except:
                    entities=[]  
                    pass
                
                

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
                count=count+1
                que.append(question)
                writer.writerow([question[0],question[-1],question[3],question[4],question[5],question[6]])
            except Exception as e:
                print("ERROR at ",count)
                print(e)
                pass
        else:
            count+=1

'''with open('Spotlight1_LCQUAD.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in que:
        writer.writerow([question[0],question[-1],question[3],question[4],question[5],question[6]])'''

Precision=sump/count
Recall=sumr/count
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)
print("no template formed: ",notemp)