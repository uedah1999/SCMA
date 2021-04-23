import pandas as pd
from tqdm import tqdm

# create a csv with information on which scenes each episode begins and ends
def summarize_dataset(input='./corpora/The-Office-Lines-V4.csv', output='./office_summary/office_episodes.csv'):
    df = pd.read_csv(input)
    df['episode_info'] = pd.NA
    for idx, row in tqdm(df.iterrows(), total=df.shape[0]):
        df.loc[idx, 'episode_info'] = "Season {}, Eposide {} ({})".format(row['season'], row['episode'], row['title'])
    df = df.loc[:, ['scene', 'episode_info']]
    df_scene = df.groupby(['scene'])
    df_epi = df.groupby(['episode_info']).min()
    df_epi.columns = ['min_scene']
    df_epi = df_epi.join(df.groupby(['episode_info']).max())
    df_epi.reset_index(inplace=True)
    df_epi.columns = ['episode_info', 'min_scene', 'max_scene']
    df_epi.sort_values(by='min_scene', inplace=True, ignore_index=True)
    df_epi.to_csv(output, index=False)

summarize_dataset()