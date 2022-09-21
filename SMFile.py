import SMUtils
from SMUtils import BEATS_PER_MEASURE, TAG_END, TAG_START, NOTE_STEP, NOTE_HOLD_HEAD, NOTE_MINE, NOTE_NONE, NOTE_ROLL_HEAD, NOTE_TAIL


class SMFile:
    def __init__(self, filename:str):
        self.filename = filename
        self.header_tags = {}
        self.bpms:list[tuple[float]] = []
        self.charts:list[SMChart] = []
        self._parse_file()
    
    def _parse_file(self):
        curr_header_entry = ''
        parsing_tag = False
        with open(self.filename) as f:
            while ch := f.read(1):
                if ch == TAG_START:
                    parsing_tag = True
                elif ch == TAG_END:
                    parsing_tag = False
                    should_parse, tag, value = SMUtils.parse_entry(curr_header_entry)
                    if not should_parse:
                        curr_header_entry = ''
                        continue

                    if tag == 'BPMS':
                        self.bpms = SMUtils.parse_bpm_str(value)
                    elif tag == 'NOTES':
                        self.charts.append(SMChart(value))
                    elif tag == 'OFFSET':
                        self.header_tags['OFFSET'] = float(value)
                    else:
                        self.header_tags[tag] = value
                    curr_header_entry = ''
                else:
                    if parsing_tag:
                        curr_header_entry += ch
    
    def __str__(self):
        selfstr = f'Stepmania Chart File\nFile Name: {self.filename}\nFile Headers:'
        for tag in self.header_tags:
            selfstr += f'\n{tag} : {self.header_tags.get(tag)}'
        
        bpmstr = ','.join([ f'{x}={y}' for x,y in self.bpms ])
        if len(bpmstr) > 80:
            bpmstr = bpmstr[:80] + '...'
        selfstr += f'\nBPMS: {bpmstr}'

        return selfstr
    
    def make_fnf_chart(self, chart_index=0, song_config:dict=None):
        # shoutout to: https://gamebanana.com/tuts/14079 plus a little extra digging around i did
        fnfjson = {
            "song": song_config.get('song', self.header_tags['TITLE']), # take from simfile or ask the user
            "sectionLengths": [], # unused but gets generated for every file
            "sections": 0, # also unused but i found it in the generated files
            "notes": [], # list[swagsection]
            "events": [], # unused by this program
            "bpm": self.bpms[0][1],
            "needsVoices": False,
            "speed": song_config.get('speed', 1),
            "player1": song_config.get('player1', 'bf'),
            "player2": song_config.get('player2', 'dad'),
            "gfVersion": song_config.get('gfVersion', 'gf'),
            "stage": "",
            "validScore": True
        }

        fnf_chart = self.charts[chart_index].to_fnf(self.bpms, self.header_tags.get('OFFSET', 0.0))
        fnfjson["notes"].extend(fnf_chart)
        return { "song": fnfjson }


class SMChart:
    def __init__(self, chartstr:str):
        # TODO : More robust parsing maybe
        chartstr = chartstr.strip()
        newchartstr = ''
        valid = True
        for ch in chartstr:
            if ch == '/':
                valid = False
            elif ch == '\n':
                newchartstr += ch
                valid = True
            else:
                if valid:
                    newchartstr += ch
        chartstr = newchartstr
        self.chart_type, self.author, self.difficulty, self.numerical_meter, self.groove_radar_val, note_data = [ x.strip() for x in chartstr.split(':')]
        
        self.measures = [ x.strip() for x in note_data.split(',')]
        self.n_keys = len(self.measures[0].strip().split()[0]) # 4 -> one player, 8 -> 2 player
    
    def to_fnf(self, bpmmap:list[tuple[float]], offset:float=0.0):
        sections:list[dict] = []
        holdtracker = {}
        strumtime = 0
        beatnum = 0
        curbpm = SMUtils.bpm_from_map(bpmmap, beatnum) # initial bpm
        change_bpm = False
        sections.append(SMUtils.make_swagsection(curbpm, change_bpm))
        for measure in self.measures:
            measure_rows = measure.strip().split()

            for row in measure_rows:
                latest_section = sections[-1]
                latest_section['bpm'] = curbpm
                for column_index, notevalue in enumerate(row):
                    if notevalue == NOTE_STEP:
                        latest_section['sectionNotes'].append([ (strumtime - offset)*1000, column_index, 0.0 ])
                    elif notevalue in (NOTE_HOLD_HEAD, NOTE_ROLL_HEAD):
                        # holds and rolls are treated the same
                        latest_section['sectionNotes'].append([ (strumtime - offset)*1000, column_index ])
                        holdtracker[column_index] = latest_section['sectionNotes'][-1]
                    elif notevalue == NOTE_TAIL:
                        holdhead:list[float] = holdtracker.get(column_index, None) # [ time, col ]
                        if holdhead is not None:
                            holdhead.append((strumtime - offset)*1000 - holdhead[0])
                            del holdtracker[column_index]
                        else:
                            print(f"\t\t\t[ERROR] Encountered tail {notevalue!r} with no head!")
                    else:
                        pass
                
                beatsperrow = SMUtils.get_beats_per_row(measure)
                beatnum += beatsperrow
                nextbpm = SMUtils.bpm_from_map(bpmmap, beatnum)
                if nextbpm != curbpm:
                    change_bpm = True
                    sections.append(SMUtils.make_swagsection(nextbpm, change_bpm))
                else:
                    change_bpm = False
                    if len(latest_section['sectionNotes']) >= 16:
                        sections.append(SMUtils.make_swagsection(nextbpm, change_bpm))

                strumtime += (60/curbpm) * beatsperrow
                curbpm = nextbpm
        
        return sections
    
    def __str__(self):
        return f'{self.chart_type} - {self.difficulty} - {self.numerical_meter} by {self.author} ({self.n_keys}k chart)'

