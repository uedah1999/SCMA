import pandas as pd
import json
import os

# load file and create dialogues
df = pd.read_csv('./corpora/The-Office-Lines-V4.csv').iloc[:,:-1]
df['dialogue'] = df['speaker'] + ': ' + df['line']
df_dialogue = df.groupby(['season','episode','scene'])['dialogue'].apply(lambda x: '\r\n'.join(x)).reset_index()

# add the number of speakers
df = df_dialogue.join(df.groupby('scene')['speaker'].nunique(), on='scene')
df.drop(columns=['season','episode'], inplace=True)
df.columns = ['id', 'dialogue', 'num_speaker']
df = df[['id', 'num_speaker', 'dialogue']]
df['summary'] = ""

result = df.to_json(orient='records')
parsed = json.loads(result)
output_dict = {}
output_dict['version'] = '2021-03-25'
output_dict['data'] = parsed
with open('corpora/office_dialogue.json', 'w') as outfile:
    json.dump(output_dict, outfile, indent=2)