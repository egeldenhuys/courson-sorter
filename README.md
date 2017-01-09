# Courson Sorter

Organise the Jon Courson Bible Teaching by Book

To be used on the set of files bought from [joncourson.com](http://www.joncourson.com/store/mp3s/mp3s.asp)

## Installation
```
git clone https://github.com/egeldenhuys/courson-sorter.git
```

## Usage
#### 1. Organise files
`$ python courson-sorter.py -s /home/john/Courson -d /home/john/Courson_Sorted`

```
[INFO] Courson Sorter v1.1.0
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
```

#### 2. Fix order of files
`$ python fix-order.py -s /home/john/Courson_Sorted`

```
[INFO] Fix Order v1.1.0
usage: fix-order.py [-h] [-s SOURCE_DIRECTORY] [-n] [--version]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE_DIRECTORY, --source-directory SOURCE_DIRECTORY
                        the folder containing the John Courson Bible files
  -n, --dry-run         Show changes to be made, but do not apply them
  --version             show program's version number and exit
```
## Sample Output
```
├── 55 - 2 Timothy
│   ├── Topical
│   │   └── 01_2 Timothy 2;15 - Rightly Dividing The Word.mp3
│   └── Verse-By-Verse
│       ├── 01_2 Timothy 1.mp3
│       ├── 02_2 Timothy 2.mp3
│       └── 03_2 Timothy 3-4.mp3
├── 56 - Titus
│   ├── Topical
│   │   └── 01_Titus 2;11-13 - Looking For Our Lord.mp3
│   └── Verse-By-Verse
│       ├── 01_Titus 1.mp3
│       └── 02_Titus 2-3.mp3
```
