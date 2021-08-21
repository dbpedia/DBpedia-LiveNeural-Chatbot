# **BENCHMARKING-using-[LCQuad-v1-dataset](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/lcquad_qaldformat.json)**

## **[LC-QuAD](http://lc-quad.sda.tech/lcquad1.0.html)**
LC-QuAD is a Question Answering dataset with 5000 pairs of question and its corresponding SPARQL query. The target knowledge base is DBpedia, specifically, the April, 2016 version. Please see our paper for details about the dataset creation process and framework.


## Check this Google [Doc](https://docs.google.com/document/d/19ZblsgnzQ8AKhv738hIwBurzbpXm5h5wqM6eekutUsM/edit?usp=sharing) for problems of approches mentioned below and ongoing discussions.


## **Only using [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api)**
1. **Case 1 [OnlySpotlight.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/onlySpotlight.csv)**
    ```
    precision score:  0.5462900000000006
    recall score:  0.5711
    F-Measure score:  0.5584195652368469
    ```
    **Code - [OnlySpotlight.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/onlyspotlight.py)**

    **Process**- Here we simply use [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api) *annotate* function to get the results and then compare with the LCQuAD benchmark answers.

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

    **Process**- Everything is same as Case 1 but Here we simply use [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api) *Candidate* function to get the results.

    **Conclusion**- 
    * Conclusion is almost same as **Case 1**


## **Using [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api) and entity extraction using templates (spotlight+jaccard)**
1. **Case 1 [spotlight_&_jac1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac1.csv)**
    ```
    precision score:  0.604106666666667
    recall score:  0.5939
    F-Measure score:  0.5989598544248503
    ```
    **Code - [spotlight_&_jac1.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac1.py)** validation using Entity Disambiguation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api) *candidate* function to get the results as tokens then we breakdown the token and do entity disambiguation using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100.
    
    If the template has two token holders and after validation we get 2 entities we return them directly, if API+Disambiguation do not give same entity as the no. of holders in temmplate then we go for extraction by finding the suitable word comparing template and the question

    Then we again do entity disambiguation for extracted tokens by comparing using same query given above. 
    
    Basically, we only use *extraction by comparing* and *disambiguation* if *API+Disambiguation fails* to give correct response or complete reponse. Also the template is not accurate there are 4760/5000 templates which has correct no. of Token holders as per Benchmark answers in dataset. Rest may have no token holders or one in if there are two entities.

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
    **Code - [spotlight_&_jac2.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spotlight_%26_jac2.py)** validation using Entity Disambiguation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use [DBpedia-Spotlight](https://www.dbpedia-spotlight.org/api) *candidate* function to get the results as tokens then we breakdown the token and do entity disambiguation using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100.

    But here we don't return the value directly instead we then extract the probable entities using template. Then we validate those probable entities using entity disambiguation, and then we use match function which returns the unioun  of both predicted entities.  
    
    Basically, it contains unioun of entities from both *API + Entity Disambiguation* and *extraction + Entity Disambiguation* avoiding copies. That's why we have high recall score but low precision score in this case.

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
1. I noticed that in case 1 in which *API + Entity Disambiguation* failed and *extraction + Entity Disambiguation* worked, The results of extraction was more accurate than api, This was visible in case 2 as well while we created unioun we saw extraction had a liltle better results

2. Also after going through dataset I saw that our code annotates extra entities which is not required, like if the template is accurate than we can know how many token holders are there which will tell how many entities we require. which will improve our precision score.

3. In benchmarking if the template is correct  for questions, then *extraction + Entity Disambiguation* will have good score because while comparing question and template the order and words will not change.

4. Problem in template creation is because of mismatch of *entity spelling or words or use of latin characters* in question with *Benchmark answers* in dataset. Template creation function is here in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

5. Now thinking of all the above points I tried an approach with only entity *extraction + Entity Disambiguation* and only in those cases, in which we have correct templates which is 4768/5000 samples. Here correct templates doesn't mean benchmark answers and question have same entities spelling or words, it means that in these 4768 samples the no. of token holders is same as no. of entities in Benchmark answers of dataset, because in template creation it replaces any matching word in question with the matching word in entities in Benchmark answers by a token holder <> for a particular entity.

6. Results of this approach is given below.

## **Using only Extraction + Entity Disambiguation using templates**
1. **Case 1 [only_jac_correct_temp1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_jac_correct_temp1.csv)**
    ```
    precision score:  0.6398153975246487
    recall score:  0.6396056219844766
    F-Measure score:  0.6397104925570269
    ```
    **Code - [only_jac_correct_temp1.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_jac_correct_temp1.py)** validation using Entity Disambiguation and comparison function imported can be found in **[convert.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/convert.py)**

    **Process**- 
    Here we use 4768 samples only with proper templates. In this we extract probable entities by comparing question with templates and then validate it by doing entity disambiguation using *"SELECT ?uri ?label WHERE { ?uri rdfs:label ?label . ?label bif:contains "'''+i+'''" } limit 100"* this query with limit 100, by breaking down the probable entities in words.
    
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
    precision score:  0.7976466666666657
    recall score:  0.8628
    F-Measure score:  0.8289450758229708
    ```
    **Code - [only_Falcon.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/only_Falcon.py)**

    **Process**- Here we simply use [Falcon](https://labs.tib.eu/falcon/) *Relation and Entity* function API of falcon to get the results and then compared them with the LCQuAD benchmark answers.

    **Conclusion**- 
    * There are  3421/5000 samples correctly annotated
    * There are 195 samples which has *2 entities* and *2 are anotated* by spotlight but only *1 is correct*. 
    * There are 148 samples which has *2 entities* and *3 are anotated* by spotlight and *2 is correct*.
    * There are 118 samples which has *2 entities* and *3 are annotated* by spotlight but only *1 is correct*.
    * There are 30 samples which has *2 entities* and *4 are annotated* by code but only *1 is correct*.
    * There are 71 samples which has *2 entities* and *1 is annotated* by spotlight and *1 is correct*.
    * There are 497 samples which has *1 entity* and *2 are annotated* by spotlight but only *1 is correct*.
    * Lastly there are 451 samples which have no correct annotations.

    **Observations**-
    * Falcon takes a good amount of time to annotate, it took 13 hours for this dataset, so not exactly time efficient.
    * It over annotates very much which can be seen in Conclusion.
    * If we match extracted word and falcon response to find most similar or probable entity as per proper template, so this will avoid over annotation like above approach and may improve scores for falcon.
    * Also in cases were falcon fails, we can use extracted entity + Entity disambiguation. 
    * This approach is yet to bet tested.

## **Using (Extraction by comparing with templates) + [Dbpedia lookup](https://lookup.dbpedia.org/) + Entity Disambiguation(different)**
1. **Case 1 [Lookup_Test1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/entityextract_lookup_Test1.csv)**
    ```
    precision score:  0.7232011747430249
    recall score:  0.7230962869729389
    F-Measure score:  0.7231487270546688
    ```
    **Code - [entityextract_lookup.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/2bdade389e2d3e56d843ff19b352d8701bcb048e/LC-QuAD/entityextract_lookup.py)** validation using Entity Disambiguation and comparison function imported can be found in the same file.

    **Process**- 
    I tried disambiguation using DBpedia lookup which takes candidate entity directly like “bill finger” and returns an [XML file](https://lookup.dbpedia.org/api/search?query=bill%20finger) which we then convert into JSON and from the list of the candidates related to bill finger we match and select and one entity.
    Now for matching/disambiguation, we match the question and entity in the returned list and find out the intersection of words between the question and entity and divide it by the number of words in the entity **I.e. (intersection of words / length of entity)** and if the score is the same for more than one entity then we select the one with **Max no. of intersection** with the question. Now, this disambiguation approach is one of the main reasons for the increase in scores this is taken from Jaccard where **(intersection / (questionlength+ entitylength - intersection))**
    But our’s is a bit different, here the intersection of words is divided by entity length. We have tried with Jaccard,  Levenshtein but this gives a better score. 

    **We have tried this with jaccard as well, here's the dataset we have [jac_Lookup_Test1.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/jac_Lookup_Test1.csv)**
    ```
    precision score:  0.5629326620516047
    recall score:  0.5628277742815188
    F-Measure score:  0.5628802132803338
    ```
    why did the score fall? 
    
    see this example-
    question is - "Was winston churchill the prime minister of Selwyn Lloyd"
    
    our token - "winston churchill"  
    
    now what jaccard selects is -"Timeline of the first premiership of Winston Churchill" instead of just winston churchil why?  because question length is 9 + entity length is 8 intersection is 4 (the ,of ,winston,churchill) so the score is  4/(9+8-4)= 0.30769
    why it didn't pick "winston churchill" because it had score of 0.2222   intersection=2 , question =9 , entity=2  so 2/(9+2-2) = 0.222
    
    
    In the first approach case mentioned just above, score for "winston churchill" was 1 as it is intersection/entity length  so 2/2 =1 
    for the "Timeline of the first premiership of Winston Churchill" it had score of 0.5 because intersection/entity length i.e.  4/8 =0.5

2. **Case 2 [Lookup_Test2.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/Lookup_Test2.csv)**
    ```
    precision score:  0.7879169288860919
    recall score:  0.7878120411160059
    F-Measure score:  0.7878644815101427
    corrected sample:  241
    ```
    **Code - [entityextract_lookup.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/30cc2985e5b1975d654140bc5486ce61329721b6/LC-QuAD/entityextract_lookup.py)** validation using Entity Disambiguation and comparison function imported can be found in the same file.

    **Process**- 
    The process remains same as the case 1 with score of 0.72 but here we added two functions which solved two of the problems check **[Docs](https://docs.google.com/document/d/19ZblsgnzQ8AKhv738hIwBurzbpXm5h5wqM6eekutUsM/edit?usp=sharing)**.
    What we did in this approach is we checked if the entities mentioned in benchmark had any redirect links and if the entity we selected is one of them. This was solved using a query- 

    ```select ?sameAs where { { <'''+Elink+'''>   <http://dbpedia.org/ontology/wikiPageRedirects> ?sameAs } UNION { ?sameAs <http://dbpedia.org/ontology/wikiPageRedirects>  <'''+Elink+'''> }}```


    Where Elink will be entities given in the benchmark.

    second thing we did is, if the entity we selected form candidates have the benchmarked entity in their disambiguation section like the example mentioned in mentioned docs. Then we use another query to retrieve the all the links in disambiguation section of the selected entity from candidates. Query -

    ```SELECT ?wikiPageDisambiguates WHERE { <'''+Elink+'''> <http://dbpedia.org/ontology/wikiPageDisambiguates> ?wikiPageDisambiguates. }```

    Where Elink will be entities we selected from initial retrieved candidates from lookup.

    So after this two improvement we had a score of **0.78** here is the **[Docs](https://docs.google.com/document/d/19ZblsgnzQ8AKhv738hIwBurzbpXm5h5wqM6eekutUsM/edit?usp=sharing)** which has solved problem and problem examples.

2. **Case 3 [Lookup_Test3.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/Lookup_Test3.csv)**
    ```
    precision score:  0.8646761377317602
    recall score:  0.8646761377317602
    F-Measure score:  0.8646761377317602
    ```
    **Code - [entityextract_lookup.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/entityextract_lookup.py)** validation using Entity Disambiguation and comparison function imported can be found in the same file.

    **Process**- 
    The process remains same as the case 1 and 2 but with further problems solved check **[Docs](https://docs.google.com/document/d/19ZblsgnzQ8AKhv738hIwBurzbpXm5h5wqM6eekutUsM/edit?usp=sharing)** for explaination of problems and solution with example.
    
    The 1st problem we solved was the minute spelling errors because of which while selecting entities from retrieved candidates we were choosing the wrong one.
    Like 
    ```
    How many rivers are crossed by different Box Girder bridges
    Benchmaked- ['http://dbpedia.org/resource/Box_girder_bridge']
    We choosed- ['http://dbpedia.org/resource/Girder']
    ```
    With this when we were comparing the retrieved entity with the question instead of counting an exact word-match as intersection, we matched words of question and candidate entities to find a score using difflib similar function like if Bridge in a candidate was compared Bridges in question it would not be an exact match so it will not be counted as an intersection but it should be. So with difflib similar score we count any score >0.85 as an intersection. So the bridge and brides will be considered as intersection and then we can choose our correct entity from candidate even if there are minute spelling differences.

    The 2nd problem we solved was the entities which can’t be fetched up lookup because it doesn’t have labels in it. so for that, we checked using query if the entity in the benchmark is retrieval or not or it has label or not. If it doesn’t have any label then we don’t count it in the evaluation.
    Query -

    ```ask { <'''+Elink+'''> rdfs:label ?label.  }```
    Where Elink is the Benchmarked entity.

    The 3rd problem we solved was that entities which are no more present. so for that, we checked using query if the entity in the benchmark is present or not. If it is not present then we don’t count it in the evaluation.
    Query -

    ```ask { <'''+Elink+'''> ?p ?o.  }```
    Where Elink is the Benchmarked entity.    

    The 4th problem we solved was like a spelling error because of the Latin character in the retrieved candidate and English character in question we were not able to match them so I converted Latin character in candidates to English alphabet so that we can match and it worked.

    The 5th problem we solved was that some entities could not be retrived by lookup so we solved this by Taking candidates  from both SPARQL ENDPOINT and LOOKUP.

    So after this two improvement we had a score of **0.86** here is the **[Docs](https://docs.google.com/document/d/19ZblsgnzQ8AKhv738hIwBurzbpXm5h5wqM6eekutUsM/edit?usp=sharing)** which has solved problem and problem examples.

    **There are still few problems which can be solved with the correct spotting of the entity in question so that we don’t need to compare the complete question. And also we can get correct candidates with that. 
    So currently we’re exploring Token spotting using Standford’s parser**


## **Using [Spacy_large_model](https://spacy.io/models) for (token Extraction ) + [Dbpedia lookup](https://lookup.dbpedia.org/)+[Dbpedia Sparql endpoint](https://dbpedia.org/sparql/) for candidate selection + Entity Disambiguation**
1. **Case 1 [Lookup_spacy_ner.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/Lookup_Final_spacy_Test5.csv)**
    ```
    precision score:  0.7907653910149761
    recall score:  0.8238352745424293   
    F-Measure score:  0.8069616678630216
    ```
    **Code - [spacy_and_disambiguation.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/spacy_and_disambiguation.py)** 

    **Process**- 
    All the above process were not independent as we were extracting token using templates created from already known benchmark entities. But this approach is completely independent. Here we first spot token which are probable entities, like if the question is **"Which are the major hubs of airline which operates the Menora Tunnel"** then spotted entity is  **Menora Tunnel** using a combination of spacy ner and spacy noun chunks. 
    Then we use the token to get a candidate list form Dbpedia Lookup and Dbpedia sparql endpoint, next using entity disambiguation we select one entity from the candidate list for respective token.
    **In this case we compare candidate entity with complete question for disambigutaion**

2. **Case 2**
    ```
    F-Measure score:  0.76
    ```
    In this case everthing remains same as case 1, but while disambiguation we were only comparing extracted token with cadidate entities not the complete question.
    we did this to test if comparing only with tokens instead of question can improve results, but that wasn't the case.

## **Using [Stanford-corenlp-parser](https://stanfordnlp.github.io/CoreNLP/) + [Stanford-Stanza-Ner](https://stanfordnlp.github.io/stanza/) for (token Extraction ) + [Dbpedia lookup](https://lookup.dbpedia.org/)+[Dbpedia Sparql endpoint](https://dbpedia.org/sparql/) for candidate selection + Entity Disambiguation**
1. **Case 1 [Lookup_Stanford_ner.csv](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/Lookup_Final_parser_Test5.csv)**
    ```
    precision score:  0.8037643207855966
    recall score:  0.8514729950900164
    F-Measure score:  0.8269311077049624
    ```
    **Code - [Stanford_and_disambiguation.py](https://github.com/dbpedia/DBpedia-LiveNeural-Chatbot/blob/benchmarks/LC-QuAD/Stanford_and_disambiguation.py)** 

    **Process**- 
    This approach is also completely independent like spacy one. Here we first spot enitity using stanfordcore nlp parser and stanford stanza ner.
    For spotting we extract noun phrases from core nlp parser tree, we also use stanford stanza NER and then we choose a superset. Then we use the spotted token to get a candidate list form Dbpedia Lookup and Dbpedia sparql endpoint, next using entity disambiguation we select one entity from the candidate list for respective token.




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
This paper explains how the spotlight works.

```@inproceedings{isem2011mendesetal,
title = {DBpedia Spotlight: Shedding Light on the Web of Documents},
author = {Pablo N. Mendes and Max Jakob and Andres Garcia-Silva and Christian Bizer},
year = {2011},
booktitle = {Proceedings of the 7th International Conference on Semantic Systems (I-Semantics)},
abstract = {Interlinking text documents with Linked Open Data enables the Web of Data to be used as background knowledge within document-oriented applications such as search and faceted browsing. As a step towards interconnecting the Web of Documents with the Web of Data, we developed DBpedia Spotlight, a system for automatically annotating text documents with DBpedia URIs. DBpedia Spotlight allows users to configure the annotations to their specific needs through the DBpedia Ontology and quality measures such as prominence, topical pertinence, contextual ambiguity and disambiguation confidence. We compare our approach with the state of the art in disambiguation, and evaluate our results in light of three baselines and six publicly available annotation systems, demonstrating the competitiveness of our system. DBpedia Spotlight is shared as open source and deployed as a Web Service freely available for public use.}
}
```
