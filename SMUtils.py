TAG_START = '#'
TAG_END = ';'
TAG_SEP = ':'
TAGS_TO_INCLUDE = {
    'TITLE', # str
    'OFFSET', # float
    'BPMS', # str (which must be parsed)
    'STOPS', # it's important for SM but cant work with FNF
    'NOTES', # list[str for each chart]
    'ARTIST',
    'CREDIT'
}

NOTE_NONE = '0'
NOTE_STEP = '1'
NOTE_HOLD_HEAD = '2'
NOTE_TAIL = '3'
NOTE_ROLL_HEAD = '4'
NOTE_MINE = 'M'

BEATS_PER_MEASURE = 4

def parse_bpm_str(bpmstr:str):
    bpm_map = []
    pairs = bpmstr.strip().split(',')
    for pair in pairs:
        beatnum, bpm = pair.split('=')
        bpm_map.append((float(beatnum), float(bpm)))
    
    return sorted(bpm_map, key=lambda x: x[0])

def parse_entry(entry:str):
    pair = entry.strip().split(TAG_SEP)
    tag = pair[0]
    if tag not in TAGS_TO_INCLUDE:
        # dont bother parsing these, so return False
        return False, None, None
    if len(pair) > 2:
        value = TAG_SEP.join(pair[1:])
    else:
        value = pair[1]
    
    value = value.removesuffix(';')
    return True, tag, value

def get_beats_per_row(measure:str):
    return BEATS_PER_MEASURE/len(measure.strip().split()) # beats/measure / rows/measure

def bpm_from_map(bpmmap:list[tuple[float]], beatn:float):
    for i in range(len(bpmmap)):
        beat, _ = bpmmap[i]
        if beat > beatn:
            return bpmmap[i-1][1]
    return bpmmap[-1][1]

def make_swagsection(bpm:float, changebpm:bool, bfsection:bool=False):
    return {
        "sectionNotes": [], # list[list[float(strumtime), int(note), float(hold duration)]]
        "sectionBeats": 4,
        "typeOfSection": 0,
        "mustHitSection": bfsection,
        "gfSection": False,
        "bpm": bpm,
        "changeBPM": changebpm,
        "lengthInSteps": 16
    }

def clean_chart(chartstr):
    # removing comments (anything between a '//' and a newline)
    newchartstr = ''
    valid = True
    for i, ch in enumerate(chartstr):
        if ch == '/' and (i+1 < len(chartstr) and chartstr[i+1] == '/'):
            valid = False
        elif ch == '\n':
            newchartstr += ch
            valid = True
        else:
            if valid:
                newchartstr += ch
    return newchartstr