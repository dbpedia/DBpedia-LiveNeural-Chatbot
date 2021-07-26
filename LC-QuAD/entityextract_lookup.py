import csv
import json
import requests
import xmltodict
from evaluation import read_LCQUAD
from convert import template_convert,extract_token_value,tok_vec_similarity,query_dbpedia,similar
import unicodedata
import re

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

def sparqlEndpoint(name):
    search_list=[]
    sparqlResult=[]
    search_list.append(name)
    spl_list=name.split(" ")
    for i in range(len(spl_list)):
        spl_list[i]="'"+spl_list[i]+"'"
    s = 'AND'.join(spl_list)
    search_list.append(s)
    for i in search_list:
        t='''SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100'''
        j=query_dbpedia(t)
        l=j.get('results').get('bindings')
        for i in l:
            nmatch=i['uri']['value']
            sparqlResult.append(nmatch)
    return sparqlResult


def remove_special_characters(token):
    no_special_characters = re.sub(r'[^a-zA-Z0-9_\s]+', '', token)
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
            resultsCombined.append(i['URI'])
    else:
        resultsCombined.append(resultsLookup['URI'])
    resultsCombined.extend(resultsSparql)
    for i in resultsCombined:
        nmatchent=i.split("/")[-1].replace("_"," ")
        nmatch=remove_special_characters(nmatchent)
        nmatch=strip_accents(nmatch)
        if nmatch is not None:
                #sc=similar(name.lower(), nmatch.lower())
                #sc=jaccard(ques.lower().split(" "), nmatch.lower().split(" "))
                nmatch=nmatch.lower().split(" ")
                nmatch=set(nmatch)
                #intersection = len(list(question_set.intersection(nmatch)))
                intersection=0
                for alpha in nmatch:
                    for bravo in question_set:
                        sco=similar(alpha, bravo)
                        if sco > 0.85:
                            intersection+=1
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
errc=0
nolabel=0
with open('Lookup_Test3.csv',  mode='w' ) as results_file:
    writer=csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for question in questions:
        #try:
        if benExistsCheck(question[3]) :
            if benLabelCheck(question[3]):
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
            else:
                nolabel+=1
                


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
