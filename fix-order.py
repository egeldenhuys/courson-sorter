"""
Applies natural sorting using alphabetical prefix

Input:
A1
A10
A156
A2
A23

Output:
01_A1
02_A2
03_A10
04_A23
05_A156
...
99_XXX
"""

import argparse
import os
import re

version = 'v1.1.0'

def main():

    print('[INFO] Fix Order ' + version)

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source-directory", default='', help="the folder containing the John Courson Bible files")
    parser.add_argument("-n", "--dry-run", default=False, action='store_true', help="Show changes to be made, but do not apply them")
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)

    args = parser.parse_args()

    sortFiles(args.source_directory, args.dry_run)

def getFileMap(src):

    print('[INFO] Generating file map from ' + src)
    ''' Look for:
    Verse-By-Verse
    Topical
    '''

    fileMap = {}

    # Traverse through all dirs in src
    for root, dirs, files in os.walk(src):

        # Only sort files in relevant folders

        # NOTE: Hardcoded values!
        if (os.path.basename(root) == 'Verse-By-Verse' or os.path.basename(root) == 'Topical'):
            # sort the files
            counter = 1

            for x in sorted_nicely(files):
                if (counter < 10):
                    output = '0' + str(counter)
                else:
                    output = str(counter)

                fileMap[os.path.join(root, x)] = os.path.join(root, output + '_' + x)
                # print(os.path.join(root, x) + ' -> ' + os.path.join(root, output + '_' + x))
                counter = counter + 1

    return fileMap

def sortFiles(path, dryRun = False):
    """
    Rename the source files to a descriptive name and place
    them in the dst folder

    path    : The source folder containing the files
    dst     : The destination folder to place the files
    dryRun  : If True, do not make any changes on disk
    reverse : If True, revert the renaming Operation
    """

    fileMap = getFileMap(path)

    tmpKey = fileMap.keys()[0]
    tmpValue = fileMap[tmpKey]

    print('Example output: \n' + tmpKey + ' -> ' + tmpValue)
    confirm = raw_input('Apply? [y/N] ')

    if (confirm.lower() == 'y'):
        renameFiles(fileMap, dryRun)
    else:
        print('Operation aborted. No changes has been made.')

def renameFiles(fileMap, dryRun = False):
    """
    Rename the source files to a descriptive name and place
    them in the dst folder

    fileMap : Dictionary of (Source File Path : Destination File Path)
    dryRun  : If True, do not make any changes on disk
    reverse : If True, revert the renaming Operation
    """
    #print(fileMap)

    count = len(fileMap)
    done = 0

    for key, value in fileMap.items():

        print('Move: ' + key + ' -> ' + value)
        done = done + 1

        # Progress
        print(str(done) + '/' + str(count) + '(' + str(round(float(done) / count * 100, 2)) + '%)\n')

        if (not dryRun):
            os.renames(key, value)

# http://www.codinghorror.com/blog/2007/12/sorting-for-humans-natural-sort-order.html
# http://stackoverflow.com/questions/2669059/how-to-sort-alpha-numeric-set-in-python

def sorted_nicely( l ):
    """ Sort the given iterable in the way that humans expect."""
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(l, key = alphanum_key)

main()
