import json
import os
from flask import Flask
from flask import request
from flask import make_response
import re
from generator_utils import normalize_predicates,query_dbpedia
from func_call import two_entity,one_entity

app=Flask(__name__)

#This function get hits when the person hits the post request in webhook route

@app.route('/webhook',methods={'POST'})
def webhook():
    req = request.get_json(silent=True,force=True)
    print(json.dumps(req,indent=4))
    res=makeWebhookResult(req)
    res=json.dumps(res,indent=4)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r


#This function is called from webhook route to replace the tokens with entity, 
#This function preprocess the questions and calls function one entity or two entity from Func_call file,
#Depending on the no. of token in the question, i.e matched query.

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
