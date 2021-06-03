import pandas as pd
df=pd.read_csv('doc.csv')
print(df.shape)
rows_with_nan = []
for index, row in df.iterrows():
    is_nan_series = row.isnull()
    if is_nan_series.any():
        rows_with_nan.append(index)

print(rows_with_nan)
