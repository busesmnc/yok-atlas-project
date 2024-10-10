import pandas as pd
from yokatlas_zeynep import fakulteler as data

df = pd.DataFrame(data)
#DENEME 
df.to_csv('yok_atlas_veri.csv', index=False)  # 'index=False', satır numaralarını CSV'ye dahil etmez
print(data)
print(df)
