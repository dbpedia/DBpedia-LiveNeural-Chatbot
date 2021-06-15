# **DBpedia-LiveNeural-Chatbot**
DBpedia Live Neural Chatbot.
 
 This is a live chatbot version of the DBpedia Neural Question Answering dataset [DBNQA](https://github.com/AKSW/DBNQA) built using [Google Dialogflow](https://cloud.google.com/dialogflow/es/docs) and connected to a webhook [flask server](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/app.py).
 
## **[DBQNA dataset](https://github.com/AKSW/DBNQA)**
"DBpedia Neural Question Answering (DBNQA) [Hartmann et al.] is the largest DBpedia-targeting dataset we have found so far and a superset of the Monument dataset. It is also based on English and SPARQL pairs and contains 894,499 instances in total. In terms of vocabulary, it has about 131,000 words for English and 244,900 tokens for SPARQL without any reduction. A large number of generic templates are extracted from the concrete examples of two existing datasets LC-QUAD and QALD-7-Train [18] by replacing the entities with placeholders.
 
## **Abstract**
The chatbot is based on DBQNA templates which are broken down in Factual question Answers, where if the user asks a question it returns a respective Sparql query for the question and the answer fetched from [Dbpedia endpoint](https://dbpedia.org/sparql/) using the translated SPARQL query(if it's in the dataset). The format of the question can be seen in [data.en](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/data/LC-QuAD_v6_personal/data.en) file.
 
## **Process**
For using DBQNA in Dialogflow we have to break down the templates in CSV format which should strictly contain two columns one for the question and the other for an answer, we use [breakdown.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/breakdown.py) file to do this.
 
After breaking down we upload the converted CSV file to the knowledge base of Dialogflow (The max pair per document is 2000), [Tutorial to use Dialogflow knowledge base](https://youtu.be/kF33Ime0a2k), then we have our Knowledge base which contains FAQ's like this
<img src="https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/FAQsample.png" alt="Example 1" width="300">
 
Then when we hit a question on Dialogflow *"Give me the total number of architects of the buildings whose one of the architects was Stanford white?"*
 
it trigers the knowldege-base intent and responds with query *"SELECT DISTINCT COUNT(?uri) where { ?x dbp:architect **"tok A"** . ?x dbp:architect ?uri }"*. 
 
Then a post API call is made to [flask server](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/app.py) connected with Webhook in Dialogflow using Dialogflow response as a body. 
Now in the server the extraction of the **"tok A"** from the question takes place, which is **"Stanford_White"**. 
 
Entity extraction takes place using [DBpedia spotlight](https://www.dbpedia-spotlight.org/api) or by extracting words from the question and then by validating it using the query *"SELECT ?Uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "**' Extracted words or response of API '**"} limit 10"* in [Dbpedia endpoint](https://dbpedia.org/sparql/) which returns a list of the entity and from there we return the entity with the highest probability using similarity checking like Jaccard and sequence matcher.
 
After extraction we replace the token holder **"tok A"** with the entity and it's tag **"dbr:Stanford_White"** and final query is formed *"SELECT DISTINCT COUNT(?uri) where { ?x dbp:architect dbr:Stanford_White . ?x dbp:architect ?uri }"*.
 
Then it gets the response from [Dbpedia endpoint](https://dbpedia.org/sparql/) which is then returned to  dialogflow in form of *"Output Query: SELECT DISTINCT COUNT(?uri) where { ?x dbp:architect dbr:Stanford_White . ?x dbp:architect ?uri }\n Ans: 33"* 
 
The final answer is then displayed in Dialogflow, check the example below.
 
 
 
## **Example**
<img src="https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/Example2.png" alt="Example 1" width="300">
 
<img src="https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/Example1.png" alt="Example 2" width="300">
 
 

### **Note**
* [Data folder](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/tree/main/data) contains the processed dataset in there respective template folder where  Doc.csv is for Dialogflow and (data.en & data.sparql) is for [NSPM](https://github.com/LiberAI/NSpM)
* [Dialogflow Limitations](https://cloud.google.com/dialogflow/quotas#es-agent_1)
 
## **Steps for Local setup**
 
1. Clone the repository and install requirements.
    ```bash
    pip install -r requirements.txt
    ```
 
2. Break the templates from the DBQNA dataset into [Dialogflow knowledge base format](https://cloud.google.com/dialogflow/es/docs/how/knowledge-bases) 
    1. create a folder named as the template you want to convert and run the given command-
    2. ```bash
        mkdir -p data/LC-QuAD_v6_personal
        ```
    3. Break down the template file [LC-QuAD_v6_personal](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/LC-QuAD_v6_personal.csv) using the given commands, where the parameters are template file and output directory.
    4. ```bash
        python breakdown.py --templates LC-QuAD_v6_personal.csv --output data/LC-QuAD_v6_personal
        ```
 
3. Now Follow the given steps to get started with the Dialogflow chatbot.
 
    1. Create a Dialogflow Agent [Tutorial to create a Dialogflow agent](https://youtu.be/b7w1W9c-luU).
 
    2. create a Knowledge base [Tutorial to use Dialogflow knowledge base](https://youtu.be/kF33Ime0a2k) and upload the file like [Doc.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/data/LC-QuAD_v6_personal/doc.csv) as documents in the Knowledge base. 
 
    3. check the response is enabled and make sure to save the changes.
 
4. Integrating the webhook with the Flask server for processing the tokens.
    1. Now start the [flask server](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/app.py) exposing port 80 by running the following command.
    2. ```bash
        python app.py
        ```
    2. Install [ngrok](https://ngrok.com/download) and see its [documentation](https://ngrok.com/docs) to expose your port 80 to internet.
 
    3. Enable webhook in fulfillment section of Dialogflow and update the exposed link there with a webhook route like *"https://fff08dc6385a.ngrok.io/webhook"* and save the changes [Tutorial to connect webhook with flask server](https://youtu.be/Oh62SfC-3KY) 
 
    4. All done ask any question from [data.en](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/data/LC-QuAD_v6_personal/data.en) file you will get the converted query and its fetched answer from DBpedia.
 
## **For local testing you can use postman, without using Webhook and Ngrok**
 
1. Now start the [flask server](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/app.py) exposing port 80 by running the following command.
2. ```bash
    python app.py
    ```
3. Ask any question from [data.en](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/main/data/LC-QuAD_v6_personal/data.en) in Dialogflow and copy the raw response from diagnostic info.
 
4. Hit a post request using postman on *"localhost:80/webhook"* using the Dialogflow response as a body.
 
5. you have the same answer which will be returned to Dialogflow in case of webhook integration. Just make sure the time taken by the server is less else the webhook call will fail after integration.
 
## **Papers**
 
### Hartman, Marx, and Soru et al., 2018
 
This paper explains how the DBQNA dataset was made.
 
```
@article{hartmann-marx-soru-2018,
  author = {Hartmann, Ann-Kathrin and Marx, Edgard and Soru, Tommaso},
  abstract = {The role of Question Answering is central to the fulfillment of the Semantic Web. Recently, several approaches relying on artificial neural networks have been proposed to tackle the problem of question answering over knowledge graphs. Such techniques are however known to be data-hungry and the creation of training sets requires a substantial manual effort. We thus introduce DBNQA, a comprehensive dataset of 894,499 pairs of questions and SPARQL queries based on templates that are specifically designed on the DBpedia knowledge base. We show how the method used to generate our dataset can be easily reused for other purposes. We report the successful adoption of DBNQA in an experimental phase and present how it compares with existing question-answering corpora.},
  booktitle = {Workshop on Linked Data Management, co-located with the W3C WEBBR 2018},
  title = {Generating a Large Dataset for Neural Question Answering over the {DB}pedia Knowledge Base},
  url = {https://www.researchgate.net/publication/324482598_Generating_a_Large_Dataset_for_Neural_Question_Answering_over_the_DBpedia_Knowledge_Base},
  year = 2018
}
```
