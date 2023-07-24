# ffmpeg-metadata-chapter-generator
A Python script that generates an FFmpeg metadata file to add chapters to MP4 files.

Usage:

```bash
$ python3 ffmpeg-chapter-generator.py setlist.txt chapters.ffmeta
```

Then add the chapters to your MP4 file:

```bash
$ ffmpeg -i input.mp4 -i chapters.ffmeta -map_metadata 1 -codec copy output.mp4
```

Imagine you have a setlist file named setlist.txt containing a set of data that looks like this:

```
00:00:00	1. First Chapter Name
00:02:08	2. Second Chapter Name
00:05:06	3. Third Chapter Name
00:13:51	4. Fourth Chapter Name
00:18:27	5. Fifth Chapter Name
```

Using this script, you can create an `FFMETADATA` file containing a list of chapters as follows and use it with `ffmpeg` to add these chapters to your MP4 file:

```
;FFMETADATA1

[CHAPTER]
TIMEBASE=1/1000
START=0
END=128000
title=1. First Chapter Name

[CHAPTER]
TIMEBASE=1/1000
START=128000
END=306000
title=2. Second Chapter Name

[CHAPTER]
TIMEBASE=1/1000
START=306000
END=831000
title=3. Third Chapter Name

[CHAPTER]
TIMEBASE=1/1000
START=831000
END=1107000
title=4. Fourth Chapter Name

[CHAPTER]
TIMEBASE=1/1000
START=1107000
END=
title=5. Fifth Chapter Name
```
