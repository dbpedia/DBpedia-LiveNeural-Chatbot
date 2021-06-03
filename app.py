import json
import os
from flask import Flask
from flask import request
from flask import make_response
import re
from generator_utils import normalize_predicates,query_dbpedia

app=Flask(__name__)

@app.route('/webhook',methods={'POST'})
def webhook():
    req = request.get_json(silent=True,force=True)
    print(json.dumps(req,indent=4))
    res=makeWebhookResult(req)
    res=json.dumps(res,indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r

def one_entity(inputq,outputq,matchedq):
    start=matchedq.find('<A>')
    end=matchedq.find('>')+1+(len(inputq)-len(matchedq))
    name =inputq[start:end]
    name=name.strip().title().replace(" ","_")
    print(name)
    name='dbr:'+name
    outputq=outputq.replace("<A>",name)
    return outputq

def two_entity(inputq,outputq,matchedq):
    S1=matchedq.split(" ")
    S2=inputq.split(" ")
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
    L[0]='dbr:'+(L[0].strip().title().replace(" ","_"))
    L[1]='dbr:'+(L[1].strip().title().replace(" ","_"))
    print(L)
    if matchedq.find('<A>') < matchedq.find('<B>'):
        outputq=outputq.replace("<A>",L[0]).replace("<B>",L[1])
    else:
        outputq=outputq.replace("<A>",L[1]).replace("<B>",L[0])
    return outputq


def makeWebhookResult(req):
    result=req.get("queryResult")
    inputq=result.get("queryText").strip().replace("?","")
    outputq=result.get("fulfillmentText").strip()
    matchedq=result.get("knowledgeAnswers").get("answers")[0].get("faqQuestion").strip().replace("?","")
    inputq = re.sub(' +', ' ', inputq)
    matchedq = re.sub(' +', ' ', matchedq)
    if "<A>" in matchedq and "<B>" in matchedq:
        outputq = two_entity(inputq,outputq,matchedq)
    else:
        outputq = one_entity(inputq,outputq,matchedq)
    outputq = outputq.replace("comma",",")
    outputq=normalize_predicates(outputq)
    j=query_dbpedia(outputq)
    try:
        ans=j.get('results').get('bindings')[0]['callret-0']['value']
    except:
        ans=j.get('results')
    speech='Output Query: '+outputq+"\n Ans: "+str(ans)
    return{
        "fulfillmentMessages": [
            {
            "text": {
                "text": [speech]
            }
            }
        ]
    }


if __name__=='__main__':
    app.run(debug=True,port=80,host='0.0.0.0')
