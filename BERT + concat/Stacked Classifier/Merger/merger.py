import pandas as pd

df_a=pd.read_csv("alexa_output_all_premerge.csv", delimiter = ",")
df_d=pd.read_csv("daniela_output_all_premerge.csv", delimiter = ",")
df_et=pd.read_csv("data_full_clean_.csv", delimiter = ";", quoting=3)

print(df_et.columns)

df_et.drop(['Text'], axis=1, inplace=True)

print(df_et.columns)

df_both=df_a.join(df_d)
df_full=df_both.join(df_et)

print(df_full)

df_full.to_csv('merged_a_d_e_all.csv', index=False)