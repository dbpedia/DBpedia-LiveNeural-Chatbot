# DBpedia-LiveNeural-Chatbot
The DBpedia Live Neural Chatbot repository contains DBQNA dataset which is also broken down in Dialogflow and NSPM format. It also contains webhook integration function.

# Data folder contains the processed dataset in there respective template folder where  Doc.csv is for Dialogflow and (data.en & data.sparql) is for NSPM

### Local setup

Clone the repository.

```bash
pip install -r requirements.txt
```

# To create the dialogflow dataset 

create a folder named as template you want to convert and run the given command-

```bash
mkdir -p data/LC-QuAD_v6_personal
python breakdown.py --templates LC-QuAD_v6_personal.csv --output data/LC-QuAD_v6_personal
```

# Now Follow the given steps to get stated with Dialogflow chatbot.

1. Create a dialogflow Agent.

2. Name a Knowldege base and upload the Doc.csv file as documents. 

3. check the response is enabled and make sure to save the changes.

# Integrating the webhook
1. Now start the server exposing port 80.
```bash
python app.py
```
2. install ngrok and see its documentation to expose your port 80 to internet.

3. Enable webhook and update the exposed server link in fulfilment section of Dialogflow.

4. All done ask any question from data.en file you will get the converted query and its fetched answer from DBpedia.

# for local testing without integrating webhook you can use postman

1. activate the ```app.py``` server in local.

2. ask any question from data.en in dialogflow and copy the raw reponse from diagnostic info.

3. hit a post request using postman in your active localhost server using the dialogflow response as body.
