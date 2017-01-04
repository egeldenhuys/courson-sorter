# Courson Sorter

Organise the Jon Courson Bible Teaching by Book

To be used on the set of files bought from [joncourson.com](http://www.joncourson.com/store/mp3s/mp3s.asp)

## Installation
```
git clone https://github.com/egeldenhuys/courson-sorter.git
cd courson-sorter
python courson-sorter.py -s <Source_Directory> -d <Destination_Directory>
```

## Usage
```
[INFO] Courson Sorter v1.0.0
usage: courson-sorter.py [-h] [-s SOURCE_DIRECTORY] [-d DESTINATION] [-r] [-n]
               [--version]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_DIRECTORY, --source-directory SOURCE_DIRECTORY
                        the folder containing the John Courson Bible files
  -d DESTINATION, --destination DESTINATION
                        the root folder to place the sorted files in
  -r, --reverse         revert the changes made
  -n, --dry-run         Show changes to be made, but do not apply them
  --version             show program's version number and exit


$ python courson-sorter.py -s /home/john/Courson -d /home/john/Courson_Sorted
```

## Sample Output
```
├── 32 - Jonah
│   ├── Topical
│   │   ├── Jonah 1;17 - A Whale Of A Sign.mp3
│   │   └── Jonah 4 - Preparing And Repairing.mp3
│   └── Verse-By-Verse
│       ├── Jonah 1-2.mp3
│       └── Jonah 3-4.mp3
├── 33 - Micah
│   ├── Topical
│   │   ├── Micah 4;1-2 - Our Vision; Reviewed And Renewed.mp3
│   │   ├── Micah 6;6-8 - What The Lord Requires.mp3
│   │   └── Micah 7 - None Like Him... None But Him.mp3
│   └── Verse-By-Verse
│       ├── Micah 1-3.mp3
│       └── Micah 4-6.mp3

```
