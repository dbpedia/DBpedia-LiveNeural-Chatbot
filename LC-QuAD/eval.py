import pandas as pd
df=pd.read_csv('Lookup_Final_spacy_Test5.csv',encoding= 'unicode_escape')
p=df['1.0']
r=df['1.0.1']
sump=0
sumr=0
for i in range(len(p)):
    sump+=p[i]
    sumr+=r[i]
Precision=sump/len(p)
Recall=sumr/len(r)
f=(2 * Precision * Recall) / (Precision + Recall)
print(" precision score: ",Precision)
print(" recall score: ",Recall)
print(" F-Measure score: ",f)