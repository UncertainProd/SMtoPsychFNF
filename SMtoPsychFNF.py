import json
import sys

from SMFile import SMFile

def get_chart_index_to_convert(smfile:SMFile):
    chart_index = 0
    if len(smfile.charts) == 1:
        print(f'Chart detected: {smfile.charts[0]}')
    else:
        print('Multiple charts detected. Which one would you like to convert?')
        for ind, chart in enumerate(smfile.charts):
            print(f'[{ind+1}] {chart}')
        
        chart_index = int(input('Enter the [number] of the chart to convert: ')) - 1
    return chart_index

def input_or_default(prompt:str, default, typefn=None):
    if typefn is None:
        typefn = str
    val = input(prompt)
    if val == '':
        return default
    return typefn(val)

def replace_bad_chars(string:str, chars_toreplace:list[str], replacewith=''):
    s = string
    for ch in chars_toreplace:
        s = s.replace(ch, replacewith)
    return s

def parse_config_file(filename):
    '''Config files have this structure:
    {
        "sm_path": "path/to/simfile.sm",
        "chart_index": chart-number-you-want-to-convert-starting-at-1,
        "songname": "Name of the song",
        "songspeed": song-speed,
        "p1": "player 1 name",
        "p2": "player 2 name",
        "gfVersion": "gf-version-you-want"
    }'''
    with open(filename) as f:
        jsondata:dict = json.load(f)
    # TODO : Validate the json structure here
    return jsondata

def main():
    # Use this command below if you don't wanna type things over and over again:
    # python SMtoPsychFNF.py --useconfig <config-file>.json

    if len(sys.argv) == 1+2 and sys.argv[1] == '--useconfig':
        configfilename = sys.argv[2]
        print(f'Using configuration file: {configfilename}')
        cfg = parse_config_file(configfilename)
        sm_path = cfg.get('sm_path', '')
        simfile = SMFile(sm_path)
        
        chart_index = int(cfg.get('chart_index', 0)) - 1
        
        nkeys = simfile.charts[chart_index].n_keys

        songname = cfg.get('songname', simfile.header_tags.get('TITLE', 'Simfile-song'))
        songspeed = float(cfg.get('songspeed', 1))
        p1 = cfg.get('p1', 'bf')
        p2 = cfg.get('p2', 'dad')
        gfversion = cfg.get('gfVersion', 'gf')
        flip_chart = cfg.get('flipsides', 'n')
        flip_chart = flip_chart.lower() == 'y'
    else:
        sm_path = input('Enter the path to the .sm file: ')
        simfile = SMFile(sm_path)
        chart_index = get_chart_index_to_convert(simfile)
    
        nkeys = simfile.charts[chart_index].n_keys
    
        songname = input_or_default('Enter the name of the song (leave empty to use the SM file song title): ', simfile.header_tags.get('TITLE', 'Simfile-song'))
        songspeed = input_or_default('Enter the song speed (leave empty for songspeed = 1): ', 1, float)
        p1 = input_or_default('Enter the name of player1 (leave empty for bf): ', 'bf')
        p2 = input_or_default('Enter the name of player2 (leave empty for dad): ', 'dad')
        gfversion = input_or_default('Enter gfVersion (leave empty for \'gf\'): ', 'gf')
        flip_chart = input_or_default('Flip the chart (dance-single + flip -> bf sings the whole chart) [y/n]? (leave empty for no-flip): ', 'n')
        flip_chart = flip_chart.lower() == 'y'
    
    print(f'Found SM file:')
    print(simfile)
    
    print(f'Converting: {simfile.charts[chart_index]}')
    
    if nkeys not in (4, 8):
        print(f'WARNING: This chart has {nkeys} keys which isn\'t supported by psych engine (vanilla) and can generate incorrect charts')

    
    print('Selected values: ')
    print(f'{songname = }')
    print(f'{songspeed = }')
    print(f'{p1 = }')
    print(f'{p2 = }')
    print(f'{gfversion = }')
    print(f'{flip_chart = }')

    final_filename = replace_bad_chars(songname, ['\\', '/', ':', '*', '?', '\"', '<', '>', '|']).replace(' ', '-').lower()

    config = {
        'song': songname,
        'speed': songspeed,
        'player1': p1,
        'player2': p2,
        'gfVersion': gfversion
    }
    chart = simfile.make_fnf_chart(chart_index, config, flip_chart)

    with open(f'{final_filename}.json', 'w') as f:
        json.dump(chart, f)

    print('Done!')


if __name__ == '__main__':
    main()