Refer <a href="https://github.com/stepmania/stepmania/wiki/sm">this</a> for a comprehensive guide on how the .sm format works. The following is just paraphrasing the entire article.

## SM Header contains:
"#TITLE"
"#SUBTITLE"
"#ARTIST"
"#SUBTITLETRANSLIT"
"#ARTISTTRANSLIT"
"#GENRE"
"#CREDIT"
"#BANNER"
"#BACKGROUND"
"#LYRICSPATH"
"#CDTITLE"
"#MUSIC"
"#OFFSET"
"#BPMS"
"#STOPS"
"#SAMPLESTART"
"#SAMPLELENGTH"
"#DISPLAYBPM"
"#SELECTABLE"
"#BGCHANGES"
"#FGCHANGES"

## Chart Tags
#NOTES
The Notes tag contains the following information:
    Chart type (e.g. dance-single)
    Description/author
    Difficulty (one of Beginner, Easy, Medium, Hard, Challenge, Edit)
    Numerical meter
    Groove radar values, generated by the program
    and finally, the note data itself.
The first five values are postfixed with a colon. Groove radar values are separated with commas.

Note data is defined in terms of "measures" where a measure is several lines of text, terminated by a comma. The final measure in a chart is terminated by a semicolon instead. Each line consists of a set of characters representing each playable column in the chart type.
Valid note types are 4th, 8th, 12th, 16th, 24th, 32nd, 48th, 64th, and 192nd. Each measure consists of a number of lines that corresponds to one of these numbers. The total number of beats covered by any given measure is 4, and each line represents a portion of that. If a measure has 64 lines, for example, each line represents 1/64th of those 4 beats, or 1/16th of a beat, with the first line representing beat 0 within the measure. The note type of a given line can be determined by taking said beat value, dividing by 4, and then simplifying the fraction as much as possible and looking at the denominator. If the denominator is 96, 192 is used as the note type instead.
Note Values
These are the standard note values:
    0 – No note
    1 – Normal note
    2 – Hold head
    3 – Hold/Roll tail
    4 – Roll head
    M – Mine (or other negative note)

Later versions of StepMania accept other note values which may not work in older versions:
    K – Automatic keysound
    L – Lift note
    F – Fake note

## Non-Standard Tags
You might run into some .sm files with some non-standard tags. Though these aren't supported by StepMania, they're (maybe) good to know.
#MENUCOLOR
Defines the color of the song on ScreenSelectMusic. Origin is StepMania 3.9 Plus? Not supported in SM5.