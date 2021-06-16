# **BENCHMARKING-using-[LCQuad-v1-dataset](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/lcquad_qaldformat.json)**

## **[LC-QuAD](http://lc-quad.sda.tech/lcquad1.0.html)**
LC-QuAD is a Question Answering dataset with 5000 pairs of question and its corresponding SPARQL query. The target knowledge base is DBpedia, specifically, the April, 2016 version. Please see our paper for details about the dataset creation process and framework.



## **Only using [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api)**
1. **Case 1 [OnlySpotlight.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/onlySpotlight.csv)**
    ```
    precision score:  0.5462900000000006
    recall score:  0.5711
    F-Measure score:  0.5584195652368469
    ```
    **Code - [OnlySpotlight.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/onlyspotlight.py)**

    **Process**- Here we simply use [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api) *annotate* function to get the results and then compare with the available entity names.

    **Conclusion**- 
    * There are  2029/5000 samples correctly annotated
    * There are 335 samples which has *2 entities* and *2 are anotated* by spotlight but only *1 is correct*. 
    * There are 96 samples which has *2 entities* and *3 are anotated* by spotlight and *2 is correct*.
    * There are 147 samples which has *2 entities* and *3 are annotated* by spotlight but only *1 is correct*.
    * There are 247 samples which has *2 entities* and *1 is annotated* by spotlight and *1 is correct*.
    * There are 341 samples which has *1 entity* and *2 are annotated* by spotlight but only *1 is correct*.
    * Lastly there are 1222 samples which have no correct annotations.

2. **Case 2 [OnlySpotlight1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/onlySpotlight1.csv)**
    ```
    precision score:  0.5463973871892291
    recall score:  0.52749450109978
    F-Measure score:  0.5367795777223314
    ```

    **Process**- Everything is same as Case 1 but Here we simply use [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api) *Candidate* function to get the results.

    **Conclusion**- 
    * Conclusion is almost same as **Case 1**


## **Using [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api) and entity extraction using templates (spotlight+jaccard)**
1. **Case 1 [spotlight_&_jac1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac1.csv)**
    ```
    precision score:  0.604106666666667
    recall score:  0.5939
    F-Measure score:  0.5989598544248503
    ```
    **Code - [spotlight_&_jac1.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac1.py)** validation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api) *candidate* function to get the results as tokens then we breakdown the token and validate it using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100.
    
    If the template has two token holders and after validation we get 2 entities we return them directly, if API+validation do not give same entity as the no. of holders in temmplate then we go for extraction by finding the suitable word comparing template and the question

    Then we validate those probable entities, extracted by comparing using same query given above. 
    
    Basically, we only use extraction and validation if api fails to give correct response or complete reponse. Also the template is not accurate there are 4760/5000 templates which has correct no. of Token holders as per entity in dataset. Rest may have no token holders or one in if there are two entities.

    **Conclusion**- 
    * There are  2504/5000 samples correctly annotated
    * There are 370 samples which has *2 entities* and *2 are anotated* by code but only *1 is correct*. 
    * There are 83 samples which has *2 entities* and *3 are anotated* by code and *2 is correct*.
    * There are 123 samples which has *2 entities* and *3 are annotated* by code but only *1 is correct*.
    * There are 223 samples which has *2 entities* and *1 is annotated* by code and *1 is correct*.
    * There are 16 samples which has *1 entity* and *2 are annotated* by code but only *1 is correct*.
    * Lastly there are 1664 samples which have no correct annotations.


2. **Case 2 [spotlight_&_jac2.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac2.csv)**
    ```
    precision score:  0.5071223850468004
    recall score:  0.624875024995001
    F-Measure score:  0.5598742721857325
    ```
    **Code - [spotlight_&_jac2.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac2.py)** validation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use [DBpedai-Spotlight](https://www.dbpedia-spotlight.org/api) *candidate* function to get the results as tokens then we breakdown the token and validate it using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100.

    But here we don't return the value directly instead we then extract the probable entities using template. Then we validate those probable entities, and then we use match function which returns the unioun  of both predicted entities.  
    
    Basically, it contains unioun of entities from both *api+validation* and *extraction+validation* avoiding copies. That's why we have high recall score but low precision score in this case.

    **Conclusion**- 
    * There are  2220/5000 samples correctly annotated
    * There are 334 samples which has *2 entities* and *2 are anotated* by code but only *1 is correct*. 
    * There are 101 samples which has *2 entities* and *3 are anotated* by code and *2 is correct*.
    * There are 109 samples which has *2 entities* and *3 are annotated* by code but only *1 is correct*.
    * There are 14 samples which has *2 entities* and *4 are annotated* by code but only *1 is correct*.
    * There are 246 samples which has *2 entities* and *1 is annotated* by code and *1 is correct*.
    * There are 18 samples which has *1 entity* and *2 are annotated* by code but only *1 is correct*.
    * Lastly there are 1957 samples which have no correct annotations.

## **Observation from above implementations**
1. I noticed that in case 1 in which api+validation failed and extraction+validation worked the results of extraction was more accurate than api, this was visible in case 2 as well while we created unioun we saw extraction had a liltle better results

2. Also after going through dataset I saw that our code annotates extra entities which is not required, like if the template is accurate than we can know how many token holders are there which will tell how many entities we require. which will improve our precision score.

3. In benchmarking if the template is correct  for questions, then extraction + validation will have good score because while comparing question and template the order and words will not change.

4. Problem in template creation is because of mismatch of entity spelling or words or use of latin characters in given entity in dataset and the entity in question. template creation function is documented properly in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

5. Now thinking of all the above points I tried an approach with only entity extraction + validation in cases, in which we have correct templates which has 4768/5000 samples. Here correct templates doesn't mean that the words are same for entities, it means that in these 4768 samples the no. of token holders is same as no. of entities given in dataset, because in template creation it replaces any matching word in question with the matching word in entities provided by dataset by a token holder <> for a particular entity.

6. Results of this approach is given below.

## **Using only entity extraction + validation using templates**
1. **Case 1 [only_jac_correct_temp1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_jac_correct_temp1.csv)**
    ```
    precision score:  0.6398153975246487
    recall score:  0.6396056219844766
    F-Measure score:  0.6397104925570269
    ```
    **Code - [only_jac_correct_temp1.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_jac_correct_temp1.py)** validation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use 4768 samples only with proper templates. In this we extract probable entities by comparing question with templates and then validate it using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100 by breaking down the probable entities in words.
    
    Also here If the template has 2 token holders and then we only extract 2 most probable entities from question by using spacy for comparing question and extracted entities. same goes for 1 token holder. This is done to avoid extra wrong annotations and improve precision score.

    **Conclusion**- 
    * There are  2758/4768 samples correctly annotated
    * There are 580 samples which has *2 entities* and *2 are anotated* by code but only *1 is correct*. 
    * There are 2 samples which has *2 entities* and *1 is annotated* by code and *1 is correct*.
    * Lastly there are 1427 samples which have no correct annotations.
    * Here we see we have no extra annotations which improves the result even if the template is not perfect.


## **Only using [Falcon](https://labs.tib.eu/falcon/)**
1. **Case 1 [only_Falcon.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_Falcon.csv)**
    ```
    precision score:  0.7962325298764421
    recall score:  0.8615556005671461
    F-Measure score:  0.8276070782160055
    ```
    **Code - [only_Falcon.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_Falcon.py)**

    **Process**- Here we simply use [Falcon](https://labs.tib.eu/falcon/) *Relation and Entity* function API of falcon to get the results and then compare with the available entity names.

    **Conclusion**- 
    * There are  3379/4938 samples correctly annotated
    * There are 188 samples which has *2 entities* and *2 are anotated* by spotlight but only *1 is correct*. 
    * There are 145 samples which has *2 entities* and *3 are anotated* by spotlight and *2 is correct*.
    * There are 111 samples which has *2 entities* and *3 are annotated* by spotlight but only *1 is correct*.
    * There are 30 samples which has *2 entities* and *4 are annotated* by code but only *1 is correct*.
    * There are 67 samples which has *2 entities* and *1 is annotated* by spotlight and *1 is correct*.
    * There are 493 samples which has *1 entity* and *2 are annotated* by spotlight but only *1 is correct*.
    * Lastly there are 436 samples which have no correct annotations.

    **Observations**-
    * Falcon takes a good amount of time to annotate, it took 7-8 hours for this dataset, so not exactly time efficient.
    * It over annotates very much which can be seen in Conclusion.
    * If we match extracted word and falcon response to find most similar or probable entity as per proper template, so this will avoid over annotation like above approach and may improve scores for falcon.
    * Also in cases were falcon fails, we use extracted entity + validation. 
    * This approach is yet to bet tested.


## **Papers**
 
This paper explains how the Falcon works.
 
```
@inproceedings{conf/naacl/SakorMSSV0A19,
  added-at = {2019-06-07T00:00:00.000+0200},
  author = {Sakor, Ahmad and Mulang, Isaiah Onando and Singh, Kuldeep and Shekarpour, Saeedeh and Vidal, Maria-Esther and Lehmann, Jens and Auer, Sören},
  biburl = {https://www.bibsonomy.org/bibtex/2b71b43be4bf953384eec726d0067f109/dblp},
  booktitle = {NAACL-HLT (1)},
  crossref = {conf/naacl/2019-1},
  editor = {Burstein, Jill and Doran, Christy and Solorio, Thamar},
  ee = {https://aclweb.org/anthology/papers/N/N19/N19-1243/},
  interhash = {2289c18c59f008d36727a0664c2ea1c3},
  intrahash = {b71b43be4bf953384eec726d0067f109},
  isbn = {978-1-950737-13-0},
  keywords = {dblp},
  pages = {2336-2346},
  publisher = {Association for Computational Linguistics},
  timestamp = {2019-06-08T11:38:37.000+0200},
  title = {Old is Gold: Linguistic Driven Approach for Entity and Relation Linking of Short Text.},
  url = {http://dblp.uni-trier.de/db/conf/naacl/naacl2019-1.html#SakorMSSV0A19},
  year = 2019
}
```
