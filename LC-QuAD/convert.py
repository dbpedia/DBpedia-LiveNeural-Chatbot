from re import search
from collections import defaultdict
import http.client
import logging
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import sys
import json
import requests
import re
from difflib import SequenceMatcher
import spacy
nlp=spacy.load("en_core_web_md")

#This function is a simple function which uses two lists to find relation using jaccard formula
def jaccard(list1, list2):
    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    return float(intersection) / union

#This queries DBpedia enpoint
def query_dbpedia( query ):
    ENDPOINT = "http://dbpedia.org/sparql"
    GRAPH = "http://dbpedia.org"
    param = dict()
    param["default-graph-uri"] = GRAPH
    param["query"] = query
    param["format"] = "JSON"
    param["CXML_redir_for_subjs"] = "121"
    param["CXML_redir_for_hrefs"] = ""
    param["timeout"] = "600" 
    param["debug"] = "on"
    try:
        resp = urllib.request.urlopen(ENDPOINT + "?" + urllib.parse.urlencode(param))
        j = resp.read()
        resp.close()
    except (urllib.error.HTTPError, http.client.BadStatusLine):
        logging.debug("*** Query error. Empty result set. ***")
        j = '{ "results": { "bindings": [] } }'
    sys.stdout.flush()
    return json.loads(j)


#This function extracts probable entities by comparing question which is inputq and templates which is matchedq
#We remove same words and filter out phrases which is between similar words between question and template 
def extract_token_value(inputq,matchedq):
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
    return L


def api_vec_similarity(text,entlist):
    tokens = nlp(text)
    max = -1
    max_tok=''
    for ent in entlist:
        entv=nlp(ent.split("/")[-1].replace("_"," "))
        if max < tokens.similarity(entv):
            max= tokens.similarity(entv)
            max_tok=ent.split("/")[-1]
    return max_tok


#This function uses spacy vector to find similarity score between to sentences or words
def tok_vec_similarity(text,entlist):
    tokens = nlp(text)
    print("incoming tok",entlist)
    max = -1
    max_tok=''
    for ent in entlist:
        entv=nlp(ent)
        if max < tokens.similarity(entv):
            max= tokens.similarity(entv)
            max_tok=ent
    return max_tok

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def match(list_1,list_2):
    combined_list=[]
    set_1 = set(list_1)
    set_2 = set(list_2)
    
    combined_list= list(set_1 | set_2)
    if 'http://dbpedia.org/resource/' in combined_list:
        combined_list.remove('http://dbpedia.org/resource/')
    return combined_list



#This function takes entity as input like Ralph_Bunche 
#Then it breaks down this in Ralph_Bunche,'Ralph'AND'Bunche',Ralph,Bunche
#then it uses them as value in given query and returns entity with highest score with Ralph_Bunche or given name
#if it finds any score 1.0 in between it returns the entity then and there.
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
        t='''SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        for i in l:
            nmatch=i['uri']['value'].split("/")[-1]
            sc=similar(name.lower(), nmatch.lower())
            #sc=jaccard(name.lower().split("_"), nmatch.lower().split("_"))
            if sc>score:
                score=sc
                final_name=nmatch
                if score>=1.0:
                    return final_name
    return final_name


#This function takes input a question and given entity list from dataset
#Then for each entity like this http://dbpedia.org/resource/Stanford_Cardinal we take out Stanford_Cardinal
#we break this and match directly if its present in question it replaces the entity with place holder and moves to next entity
#if not present then we check for each word in "Stanford Cardinal" 
# and replace all of the same words with empty space and last word with place holder
def template_convert(text,ent):
    text=text.lower().replace("'s","")
    for i in range(len(ent)):
        print(ent[i])
        tok=ent[i].split('/')[-1]
        tok=tok.replace("_"," ").lower()
        print(tok)
        reptok ='<'+ chr(ord('A') + i) +'>'
        if tok in text:
            text=text.replace(tok,reptok)
        else:
            slist=[x for x in text.split() if x in tok and len(x)>2]
            print(slist)
            s = ' '.join(slist)
            s=s.strip()
            print("set: "+s)
            if s in text and s!='':
              text=text.replace(s,reptok)
            elif s!='':
              for i in slist[:-1]:
                text=text.replace(i,'')
              text=text.replace(slist[-1],reptok)
    text = re.sub(' +', ' ', text)
    print(text)
    return text

#not used
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

