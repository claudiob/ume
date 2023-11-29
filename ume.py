#! /usr/bin/python3 -W ignore

import sys
import azapi
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT

for file in sys.argv[1:]: # "~/Music/Albums/**/**/*.mp3"
    print(file + "…")
    artist = EasyID3(file)["artist"][0]
    title = EasyID3(file)["title"][0]

    API = azapi.AZlyrics('google', accuracy=0.5)
    API.artist = artist
    API.title = title
    API.getLyrics(save=True, ext='lrc')

    audio = ID3(file)
    audio.add(USLT(encoding=3, text=API.lyrics))
    audio.save()
    print(file + " updated")