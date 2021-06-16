import requests
import csv
import evaluation as read_LCQUAD


#this function uses spotlight annotate function to return the entities
def dbpeida_spotlight_call(text):
    headers = {
        'Accept': 'application/json',
    }
    response = requests.get('https://api.dbpedia-spotlight.org/en/annotate?text='+text, headers=headers)
    if response.status_code == 200:
        result=response.json()
        if 'Resources' in result:
            return result['Resources']
        else:
            return ""
    else:
        temp=dbpeida_spotlight_call(text)
        return temp


#from evaluation file
questions=read_LCQUAD()
    #questions=evaluation.read_LCQUAD2()
    #questions=evaluation.read_QALD7()


    
coun=0
que=[]
sump=0
sumr=0
with open('/content/gdrive/MyDrive/only_Spotlight3_LCQUAD.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:    
            p_entity=0
            r_entity=0
            print(coun)
            print(question[0])
            results=dbpeida_spotlight_call(question[0])
            results=[result['@URI'] for result in results]
            entities=results
            

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
            que.append(question)
            writer.writerow([question[0],question[3],question[4],question[5],question[6]])
            Precision=sump/coun
            Recall=sumr/coun
            f=(2 * Precision * Recall) / (Precision + Recall)
            print(" precision score: ",Precision)
            print(" recall score: ",Recall)
            print(" F-Measure score: ",f)


print("FINAL: \n")
Precision=sump/coun
Recall=sumr/coun
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)