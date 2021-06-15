from re import search
from generator_utils import query_dbpedia
from collections import defaultdict
import json
import requests
from difflib import SequenceMatcher
import spacy
nlp=spacy.load('en_core_web_md')

#This function is used to find similartity score using jaccard formula.
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

#This function is used to find similartity score using in built sequence matcher.
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#This functions returns the best entity
#By compairing vector similarity using SPACY model between extracted token from api and the question.
def api_vec_similarity(text,entlist):
    tokens = nlp(text)
    max = -1
    max_tok=''
    for ent in entlist:
        entv=nlp(ent.replace("_"," "))
        if max < tokens.similarity(entv):
            max= tokens.similarity(entv)
            max_tok=ent
    return max_tok

#This functions returns the best entity by compairing vector similarity using SPACY model, 
#Between extracted words for entity using extract_token_value function and the question.
def tok_vec_similarity(text,entlist):
    tokens = nlp(text)
    max = -1
    max_tok=''
    for ent in entlist:
        entv=nlp(ent)
        if max < tokens.similarity(entv):
            max= tokens.similarity(entv)
            max_tok=ent
    return max_tok

#This function takes the token name as input and apply entity linking method,
#To get the best token or entity by extracting maximum similarity score token of the resulted entities from the query.
def validate_ant(name):
    search_list=[]
    search_list.append(name)
    spl_list=name.split("_")
    for i in range(len(spl_list)):
        spl_list[i]="'"+spl_list[i]+"'"
    s = 'AND'.join(spl_list)
    search_list.append(s)
    search_list.extend(name.split('_'))
    score=0.0
    final_name=''
    for i in search_list:
        t='''SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 10'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        for i in l:
            nmatch=i['uri']['value'].split("/")[-1]
            sc=similar(name.lower(), nmatch.lower())
            if sc>score:
                score=sc
                final_name=nmatch
                if score>=1.0:
                    return final_name
    return final_name

#This function finds the entities in the sentence using DBpedia spotlight API
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

#This function finds the entities in the sentence using Falcon API and it's accurate than spotlight,
#But we are not using this beacause it takes large amount of time which is not suitable for dialogflow.
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

#This function compares the question and matched query from response 
#By eliminating similar words and filtering them on noun to get probable entity candidates.
def extract_token_value(inputq,matchedq,ne):
    S1=matchedq.lower().strip().replace(",","").replace("'s","").split(" ")
    S2=inputq.lower().strip().replace(",","").replace("'s","").split(" ")
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
                L.append(G.strip())
        i+=1
    if len(L)<=ne:
        return L
    else:
        final_list=[]
        for i in range(len(L)):
            doc=nlp(L[i])
            r=''
            for j in doc.noun_chunks:
                r+=str(j)+" "
            r=r.strip()
            if len(L[i].split()) % 2 == 0:
                if len(L[i].split())/2 <= len(r.split()):
                    final_list.append(r)
            else:
                if (len(L[i].split())+1)/2 <= len(r.split()):
                    final_list.append(r)
        return final_list

#This is the main function called from app.py when the question has one entity
#it first gets the entity from api and validates it if api response is empty
#then it uses probable candidates and validates it.
def one_entity(inputq,outputq,matchedq):
    try:
        name=get_entity(inputq)
        if len(name) >1:
            name=api_vec_similarity(inputq,name)
        else:
            name=name[0]
        print("api: ",name)   
    except:
        name=extract_token_value(inputq,matchedq,1)
        if len(name) >1:
            name=tok_vec_similarity(inputq,name)
        else:
            name=name[0]
        print("jac: ",name) 
        name=name.strip().title().replace(" ","_")
    name=validate_ant(name)
    print("Final: ",name)
    name='dbr:'+name
    outputq=outputq.replace("<A>",name)
    return outputq

#This is the main function called from app.py when the question has two entity
#it first gets the entity from api and validates it if api response is empty or only one entity is present
#then it uses probable candidates and validates it.
def two_entity(inputq,outputq,matchedq):
    L=[]
    try:
        L=get_entity(inputq)
        L=L[:2]
        print("Api: ",L)
    except:
        ext_l=extract_token_value(inputq,matchedq,2)
        if len(ext_l) >2:
            name=tok_vec_similarity(inputq,ext_l)
            L.append(name)
            name=tok_vec_similarity(inputq,ext_l.remove(name))
            L.append(name)
        else:
            L=ext_l
        L[0]=L[0].strip().title().replace(" ","_")
        L[1]=L[1].strip().title().replace(" ","_")
        print("jac: ",L)
    L[0]=validate_ant(L[0])
    L[1]=validate_ant(L[1])
    L[0]='dbr:'+L[0]
    L[1]='dbr:'+L[1]
    print("Final: ",L)
    if matchedq.find('<A>') < matchedq.find('<B>'):
        outputq=outputq.replace("<A>",L[0]).replace("<B>",L[1])
    else:
        outputq=outputq.replace("<A>",L[1]).replace("<B>",L[0])
    return outputq



