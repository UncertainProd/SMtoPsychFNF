## As of latest version (0.6.2)

```jsonc
// SwagSong
{
    "song" : "song-name",
    "notes": [
        { // SwagSection
            "sectionNotes" : [
                [ "time-value(Float) aka when the note shows up", "column(0-7)",  "hold-duration(Float)" ]
            ], // Array<Dynamic>
            "sectionBeats" : 4.0, // usually 4 (dont see a reason for any value other than 4)
            "typeOfSection" : 0, // always 0 from what i see
            "mustHitSection" : true, // is player section?
            "gfSection" : false, // is usually false
            "bpm" : 0.0, // bpm of this section
            "changeBPM": true, // does this section change the bpm?
            "altAnim" : true, // animation stuff (cant generate this from this program)
            "lengthInSteps": 16 // unused
        }
    ],
    "events" : [
        {} // Dynamic
    ],
    "bpm" : 0.0, // bpm of the song (??)
    "needsVoices" : false, // shud be false when converting from sm i guess
    "speed" : 2.0, // song speed

    "player1" : "p1",
    "player2" : "p2",
    "gfVersion" : "gf", 
    "stage" : "",

    "arrowSkin" : "", // cant generate this from this program
    "splashSkin" : "", // cant generate this from this program
    "validScore" : false // pretty much always false
}
```