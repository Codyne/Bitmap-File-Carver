# Bitmap-File-Carver
This script reads in file paths to bitmap files from the command line and searches for bitmap headers within the file. Any bitmap files discovered will be stored and saved to an output directory and a filename corresponding to the offset number of bytes the bitmap was found at.

Any blocks of contiguous suspicious bytes found outside the size of the bitmap will be also output with its offset and use a `.unknown` file extension.

Using the test file contained in this repo, it will identify 3 bitmaps (2 hidden) and suspicious bytes.
This is the example input and output.
```
python3 bmp_carver.py steg.bmp
Offset: 0, FileSize: 8294538 bytes, MD5: 2857b4fae33f177e98d6b99164b571c8, Path: steg.bmp_Output/0.bmp
Offset: 8294542, FileSize: 1000138 bytes, MD5: 796960a097dcecddee4246b545ecf9c1, Path: steg.bmp_Output/8294542.bmp
Offset: 9294684, FileSize: 40138 bytes, MD5: d0fa257ce629ad05d739223363aac6bf, Path: steg.bmp_Output/9294684.bmp
Offset: 8294538, FileSize: 4 bytes, MD5: f1d3ff8443297732862df21dc4e57262, Path: steg.bmp_Output/8294538.unknown
Offset: 9294680, FileSize: 4 bytes, MD5: f1d3ff8443297732862df21dc4e57262, Path: steg.bmp_Output/9294680.unknown
Offset: 9334822, FileSize: 4 bytes, MD5: f1d3ff8443297732862df21dc4e57262, Path: steg.bmp_Output/9334822.unknown
```


Another example output from possible file inputs.

Assume `simple.bmp` is a valid bitmap file. The file will be read in and output to `simple.bmp_Output/0.bmp`.

Assume `steg.bmp` is a bitmap file, but there is a second hidden bitmap file hidden inside at offset 130448 bytes, as well as a hidden file contained at the end of the file that is of unknown type.
The bitmap will be identified and written to with it's corresponding offset of `0.bmp`, and the subsequent hidden bitmap will be stored in the same directory with its filename as its offset as `130448.bmp`. Lastly the contiguous block of suspicious bytes contained at the of the file are stored with its file extension as `.unknown`.

```
python3 bmp_carver.py simple.bmp steg.bmp
Offset: 0, FileSize: 1216166 bytes, MD5: 7b9912e657196dc89cbffd65b4bacadb, Path: simple.bmp_Output/0.bmp
Offset: 0, FileSize: 1216166 bytes, MD5: c6c4dc5bce95f296188005c28a92c86c, Path: steg.bmp_Output/0.bmp
Offset: 130448, FileSize: 3038 bytes, MD5: 0791b89fb49f891e8e6b3c1da65f0728, Path: steg.bmp_Output/130448.bmp
Offset: 1216166, FileSize: 1865 bytes, MD5: be6a4e925f8be6a5b12028b490c934dd, Path: steg.bmp_Output/1216166.unknown
```