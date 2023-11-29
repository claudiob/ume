#! /usr/bin/python3 -W ignore

import sys
import azapi
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, USLT
import os, contextlib

total = len(sys.argv[1:])
for index, file in enumerate(sys.argv[1:]): # "~/Music/Albums/**/**/*.mp3"
  print("{:05d}/".format(index+1) + "{:05d} ".format(total) + "/".join(file.rsplit("/", 3)[1:]), end=' ? ')
  id3 = EasyID3(file)

  if "grouping" in id3 and "★" in id3["grouping"][0]:
    print(" \033[34mHas lyrics\033[0m")

  elif "artist" in id3 and "title" in id3:
    artist = id3["artist"][0]
    title = id3["title"][0]

    API = azapi.AZlyrics('google', accuracy=0.5)
    API.artist = artist
    API.title = title
    # with open(os.devnull, 'w') as devnull:
    #   with contextlib.redirect_stdout(devnull):
    #     API.getLyrics(save=False)
    if API.getLyrics(save=False, sleep=5):
      audio = ID3(file)
      audio.add(USLT(encoding=3, text=API.lyrics))
      audio.save()

      id3["grouping"] = id3["title"][0] + " ★"
      id3.save()
      print("\033[32mLyrics added\033[0m")

  else:
    id3["grouping"] = "No lyrics ☆"
    id3.save()
    print("\033[31mLyrics not found\033[0m")
