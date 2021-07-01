import csv
import json
import requests
import xmltodict
from evaluation import read_LCQUAD
from convert import template_convert,extract_token_value,tok_vec_similarity

def lookup_dbpedia(text):
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post('https://lookup.dbpedia.org/api/search?MaxHits=50&QueryString='+text,headers=headers)
    j=response.content.decode("utf-8")
    data_dict = xmltodict.parse(j)
    json_data = json.dumps(data_dict,indent=4)
    data = json.loads(json_data)
    try:
        return data["ArrayOfResults"]["Result"]
    except:
        return []


def validate_ant(name,ques):
    results=lookup_dbpedia(name)
    score=0
    pr_intrsc=0
    final_name=''
    question_set=set(ques.lower().split(" "))
    nmatch=" "
    if isinstance(results, list):
        for i in results:
            nmatch=i['Label']
            if nmatch is not None:
                #sc=similar(name.lower(), nmatch.lower())
                nmatch=nmatch.lower().split(" ")
                intersection = len(list(question_set.intersection(nmatch)))
                union = len(nmatch)
                sc= float(intersection) / union
                print(nmatch," : ",intersection," : ",sc)
                #sc=cosine_sc(vectors_ques[0],nmatch)
                if sc>score and ('Category:' not in nmatch):
                    score=sc
                    pr_intrsc=intersection
                    final_name=i['URI']
                elif sc==score and intersection > pr_intrsc:
                    score=sc
                    pr_intrsc=intersection
                    final_name=i['URI']
    else:
        final_name=results['URI']

    return final_name

def one_entity(inputq,matchedq):
    outputq=[]
    name=extract_token_value(inputq,matchedq)
    print("extracted tok: ",name)
    if len(name) >1:
        name=tok_vec_similarity(inputq,name)
    else:
        name=name[0]
    name=name.strip().title()
    name=validate_ant(name,inputq)
    print("jac: ",name)
    outputq.append(name)
    return outputq

def two_entity(inputq,matchedq):
    L=[]
    ext_l=extract_token_value(inputq,matchedq)
    print("extracted token",ext_l)
    if len(ext_l) >2:
        name=tok_vec_similarity(inputq,ext_l)
        L.append(name)
        ext_l.remove(name)
        name=tok_vec_similarity(inputq,ext_l)
        L.append(name)
    else:
        L=ext_l
    for i in range(len(L)):
        L[i]=L[i].strip().title()
        L[i]=validate_ant(L[i],inputq)
    print("jac: ",L)
    return L

questions=read_LCQUAD()
    #questions=evaluation.read_LCQUAD2()
    #questions=evaluation.read_QALD7()


    
coun=0
que=[]
sump=0
sumr=0
Precision=0
Recall=0
f=0
with open('/content/gdrive/MyDrive/entityextract_lookup_Test1.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        #try:    
            p_entity=0
            r_entity=0
            print(coun)
            question[0]=question[0].replace("?","")
            print(question[0])
            temp=template_convert(question[0],question[3])
            if ("<A>" in temp and "<B>" in temp and len(question[3])==2) or (len(question[3])==1 and ("<A>" in temp or "<B>" in temp)):
                if "<A>" in temp and "<B>" in temp:
                    entities = two_entity(question[0],temp)
                elif "<A>" in temp or "<B>" in temp:
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
                if (Precision + Recall)!=0:
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
