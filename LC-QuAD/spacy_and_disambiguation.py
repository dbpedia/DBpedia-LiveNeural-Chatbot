import csv
import json
import requests
import xmltodict
from evaluation import read_LCQUAD
from convert import query_dbpedia,similar
import unicodedata
import re
import spacy


nlp=spacy.load('en_core_web_lg')


def lookup_dbpedia(tex):
    search_list=[]
    flag=1
    search_list.append(tex)
    spl_list=tex.split(" ")
    #print(spl_list)
    lense=len(search_list)
    i=0
    final_list=[]
    while i < lense:
        text=search_list[i]
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post('https://lookup.dbpedia.org/api/search?MaxHits=100&QueryString='+text,headers=headers)
        j=response.content.decode("utf-8")
        data_dict = xmltodict.parse(j)
        json_data = json.dumps(data_dict,indent=4)
        data = json.loads(json_data)
        try:
            if isinstance(data["ArrayOfResults"]["Result"], list):
                final_list.extend(data["ArrayOfResults"]["Result"])
            else:
                return data["ArrayOfResults"]["Result"]
            i+=1
        except:
            if flag :
                flag=0
                #print('LOL')
                if len(spl_list)==2:
                    search_list.extend(spl_list)
                    lense+=2
                elif len(spl_list) >2 and len(spl_list) <=4:
                    for i in range(len(spl_list)):
                        templ=spl_list[:i]
                        templ.extend(spl_list[i+1:])
                        s = ' '.join(templ)
                        lense+=1
                        search_list.append(s)
                elif len(spl_list) >4 :
                    for i in range(len(spl_list)):
                        templ=spl_list[:i]
                        templ.extend(spl_list[i+2:])
                        s = ' '.join(templ)
                        lense+=1
                        search_list.append(s)
            else:
                i+=1
                continue
    return final_list

def sparqlEndpoint(name):
    search_list=[]
    sparqlResult=[]
    flag=1
    spl_list=name.split(" ")
    for i in range(len(spl_list)):
        spl_list[i]="'"+spl_list[i]+"'"
    s = 'AND'.join(spl_list)
    search_list.append(s)
    #print(search_list)
    lense=len(search_list)
    k=0
    while k < lense:
        text=search_list[k]
        #print(text)
        t='''SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+text+'''" } limit 10'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        for i in l:
            nmatch=i['uri']['value']
            sparqlResult.append(nmatch)
        if len(sparqlResult)==0 and flag:
            flag=0
            #print("LOL")
            if len(spl_list)==2 :
                search_list.extend(spl_list)
                lense+=2
            elif len(spl_list) >2 and len(spl_list) <=4:
                for i in range(len(spl_list)):
                    templ=spl_list[:i]
                    templ.extend(spl_list[i+1:])
                    s = 'AND'.join(templ)
                    lense+=1
                    search_list.append(s)
            elif len(spl_list) >4 :
                for i in range(len(spl_list)):
                    templ=spl_list[:i]
                    templ.extend(spl_list[i+2:])
                    s = 'AND'.join(templ)
                    lense+=1
                    search_list.append(s)
        k+=1
    return sparqlResult


def remove_special_characters(token):
    no_special_characters = re.sub(r'[^a-zA-Z0-9_\s]+', ' ', token)
    return no_special_characters

#print(remove_special_characters("Hi helloo how are (you) what's up yoo yoo 2019."))

def strip_accents(text):
    return ''.join(char for char in
                   unicodedata.normalize('NFKD', text)
                   if unicodedata.category(char) != 'Mn')


def matchDisambiguates(BElink):
    Disambglist=[]
    for Elink in BElink:
        Disambglist.append(Elink)
        t='''SELECT ?wikiPageDisambiguates WHERE { <'''+Elink+'''> <http://dbpedia.org/ontology/wikiPageDisambiguates> ?wikiPageDisambiguates. }'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        l=[i['wikiPageDisambiguates']['value'] for i in l]
        Disambglist.extend(l)
    return Disambglist

def matchRedirects(BElink):
    Redireclist=[]
    for Elink in BElink:
        Redireclist.append(Elink)
        t='''select ?sameAs where { { <'''+Elink+'''>   <http://dbpedia.org/ontology/wikiPageRedirects> ?sameAs } UNION { ?sameAs <http://dbpedia.org/ontology/wikiPageRedirects>  <'''+Elink+'''> }}'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        l=[i['sameAs']['value'] for i in l]
        Redireclist.extend(l)
    return Redireclist

def benExistsCheck(ques):
    for t in ques:
        t = '''ask { <'''+t+'''> ?p ?o.  }'''
        j=query_dbpedia(t)
        if j.get('boolean'):
            continue
        else:
            return False
    return True

def benLabelCheck(ques):
    for t in ques:
        t = '''ask { <'''+t+'''> rdfs:label ?label.  }'''
        j=query_dbpedia(t)
        if j.get('boolean'):
            continue
        else:
            return False
    return True

def validate_ant(name,ques):
    resultsLookup=lookup_dbpedia(name)
    resultsSparql=sparqlEndpoint(name)
    resultsCombined=[]
    score=0
    pr_intrsc=0
    final_name=''
    ques=remove_special_characters(ques)
    ques=strip_accents(ques)
    question_set=set(ques.lower().split(" "))
    nmatch=" "
    nmatchent=" "
    if isinstance(resultsLookup, list):
        for i in resultsLookup:
            try:
                resultsCombined.append(i['URI'])
            except:
                pass
    else:
        resultsCombined.append(resultsLookup['URI'])
    resultsCombined.extend(resultsSparql)
    for i in resultsCombined:
        nmatchent=i.split("/")[-1].replace("_"," ")
        nmatch=strip_accents(nmatchent)
        nmatch=remove_special_characters(nmatch)
        nmatch=nmatch.replace(' of '," ").replace(' the '," ")
        if nmatch is not None:
                #sc=similar(name.lower(), nmatch.lower())
                #sc=jaccard(ques.lower().split(" "), nmatch.lower().split(" "))
                nmatch=nmatch.lower().split(" ")
                nmatch=[x for x in nmatch if x!='' and x!=' ']
                nmatch=set(nmatch)
                #intersection = len(list(question_set.intersection(nmatch)))
                intersection=0
                for alpha in nmatch:
                    flagsm=1
                    for bravo in question_set:
                        sco=similar(alpha, bravo)
                        if sco > 0.85:
                            intersection+=1
                            flagsm=0
                            break
                    if flagsm:
                        for bravo in question_set:
                            sco=similar(alpha, bravo)
                            if sco > 0.7:
                                intersection+=sco
                                break
                union = len(nmatch)
                sc= float(intersection) / union
                #print(nmatch," : ",intersection," : ",sc)
                #sc=cosine_sc(vectors_ques[0],nmatch)
                if sc>score and ('Category:' not in nmatchent):
                    score=sc
                    pr_intrsc=intersection
                    final_name=i
                elif sc==score and intersection > pr_intrsc and ('Category:' not in nmatchent):
                    score=sc
                    pr_intrsc=intersection
                    final_name=i

    return final_name



def tokextractor(s):
    doc=nlp(s)
    ent1=[]
    ent2=[]
    for entity in doc.ents:
        ent1.append(str(entity.text))

    for i in doc.noun_chunks:
            pos=[t.pos_ for t in i]
            if (pos.count("NOUN")+pos.count("PROPN"))/len(i)>=0.4:
                ent2.append(str(i))
            
    print(ent1)
    print(ent2)

    finalent=[]

    for i in ent1:
        for j in ent2:
            if i in j:
                finalent.append(j)
            elif j in i:
                finalent.append(i)

    if len(ent1)<1:
        finalent=ent2
    elif len(finalent)!=len(ent1) :
        finalent.extend(ent1)

    finalent=list(set(finalent))

    return finalent


def expansion(inp):
    expan_dic={'us':'United states','sf':'San francisco','pm':'Prime minister','ny':'New York'}
    inp=inp.split()
    ret=[]
    for i in inp:
        if i.lower() in expan_dic:
            ret.append(expan_dic[i.lower().replace('.','')])
        else:
            ret.append(i)
    inp=' '.join(ret)
    return inp

def entitycall(inputq):
    L=[]
    inputq=inputq.replace('(',' ').replace(')',' ')
    inputq=expansion(inputq)
    L=tokextractor(inputq)
    inputq=inputq.replace(' the ',' ').replace(' of ',' ')
    print("extracted token: ",L)
    for i in range(len(L)):
        L[i]=L[i].strip().title()
        L[i]=validate_ant(L[i],inputq)
    L=list(set(L))
    L=[x for x in L if x!=' ' and x!='']
    return L

import csv
import json
import requests



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
errc=0
nolabel=0
with open('Lookup_Final_spacy_Test5.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        try:
            if benExistsCheck(question[3]) :
                if benLabelCheck(question[3]):
                    p_entity=0
                    r_entity=0
                    print(coun)
                    question[0]=question[0].replace("?","")
                    print(question[0])
                    entities = entitycall(question[0])
                    entities=list(set(entities))
                    print(question[3])
                    print(entities)
                    coun+=1
                    numberSystemEntities=len(question[3])
                    intersection= set(question[3]).intersection(entities)
                    if len(intersection)!=numberSystemEntities:
                        jj=matchRedirects(question[3])
                        je=matchRedirects(entities)
                        intersection= set(jj).intersection(je)
                        if len(intersection)>len(entities):
                            intersection=list(intersection)[0:len(entities)]
                        if len(intersection)!=numberSystemEntities:
                            jdis=matchDisambiguates(entities)
                            intersection= set(jj).intersection(jdis)
                            if len(intersection)==numberSystemEntities:
                                errc+=1
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
                    if (Precision + Recall)!=0:
                        f=(2 * Precision * Recall) / (Precision + Recall)
                    print(" precision score: ",Precision)
                    print(" recall score: ",Recall)
                    print(" F-Measure score: ",f)
                else:
                    nolabel+=1
        except:
            pass
                


print("FINAL: \n")
Precision=sump/coun
Recall=sumr/coun
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)
print("corrected sample: ",errc)
print("No label: ",nolabel)
print("Total Sample: ",coun)