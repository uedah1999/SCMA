import json
import sys
import os
import subprocess as sp
import pandas as pd

def select_summary(start_scene, candidate_path, accepted_path, episode_info):
    samples = json.load(open(candidate_path, 'r'))
    currdate = str(input('Date (yyyy-mm-dd): '))

    df_epi = pd.read_csv('office_episodes.csv')
    for idx, row in df_epi.iterrows():
        if (row['min_scene'] <= start_scene) and (row['max_scene'] >= start_scene):
            epi_idx = idx
            curr_epi = row
            break
    
    for i in range(start_scene-1, samples['data'][-1]['id']):
        sp.call('clear', shell=True)
        scene = samples['data'][i]
        if scene['id'] > curr_epi['max_scene']:
            epi_idx += 1
            curr_epi = df_epi.iloc[epi_idx, :]
        print('{}: Scene {} (same episode until {})'.format(curr_epi['episode_info'], scene['id'], curr_epi['max_scene']))
        print(scene['dialogue'])
        # decision has been settled for all five summaries
        reviewed = False
        good_idx = []
        while not reviewed:
            good_idx = []
            candidates = scene['summary_candidates']
            for j in range(len(candidates)):
                valid_response = False
                print('\n' + candidates[j])
                while not valid_response:
                    response = str(input('Accept summary (y/n): '))
                    if response == 'y':
                        good_idx.append(j)
                        valid_response = True
                    elif response == 'n':
                        valid_response = True
                    else:
                        print('Answer in y or n')
            valid_response = False
            while not valid_response:
                review = str(input('Your choice is good to go (t/f): '))
                if review == 't':
                    reviewed = True
                    valid_response = True
                elif review == 'f':
                    valid_response = True
                else:
                    print('Answer in t or f')
        if len(good_idx) > 0: # some summary was accepted
            accepted_summaries = {
                'id': scene['id'], 
                'num_speaker': scene['num_speaker'], 
                'dialogue': scene['dialogue'], 
                'accepted_summaries': [candidates[k] for k in good_idx]
                }
            if os.path.exists(accepted_path):
                with open(accepted_path) as outfile:
                    accepted = json.load(outfile)
                    accepted['version'] = currdate
                    accepted['data'].append(accepted_summaries)
            else:
                accepted = {}
                accepted['version'] = currdate
                accepted['data'] = [accepted_summaries]
            with open(accepted_path, 'w') as outfile:
                json.dump(accepted, outfile, indent=2)        

def main(
    candidate_path='office_summary_candidates.json', 
    accepted_path='office_summary_accepted.json',
    episode_info='office_episodes.csv'):
    if os.path.exists(accepted_path):
        with open(accepted_path) as outfile:
            accepted = json.load(outfile)
            first = accepted['data'][0]['id']
            last = accepted['data'][-1]['id']
        start_scene = last + 1
    else:
        start_scene = int(input('Which scene number to start? (≥1): '))
    print('starting at scene {}'.format(start_scene))
    select_summary(start_scene, candidate_path, accepted_path, episode_info)

main()
