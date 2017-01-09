import argparse
import os

version = 'v1.1.0'

def main():

    print('[INFO] Courson Sorter ' + version)

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--source-directory", default='', help="the folder containing the John Courson Bible files")
    parser.add_argument("-d", "--destination", default='', help="the root folder to place the sorted files in")
    parser.add_argument("-r", "--reverse", default=False, action='store_true', help="revert the changes made")
    parser.add_argument("-n", "--dry-run", default=False, action='store_true', help="Show changes to be made, but do not apply them")
    parser.add_argument('--version', action='version', version='%(prog)s ' + version)

    args = parser.parse_args()

    if (args.source_directory == ''):
        print('Please provide the path to the Jon Coursen Bible files with -s')
        exit()

    if (args.destination == ''):
        args.destination = args.source_directory

    # Normalize paths
    args.source_directory = os.path.abspath(args.source_directory + '/')
    args.destination = os.path.abspath(args.destination + '/')

    sortFiles(args.source_directory, args.destination, args.dry_run, args.reverse)

def sortFiles(path, dst, dryRun = False, reverse = False):
    """
    Rename the source files to a descriptive name and place
    them in the dst folder

    path    : The source folder containing the files
    dst     : The destination folder to place the files
    dryRun  : If True, do not make any changes on disk
    reverse : If True, revert the renaming Operation
    """

    fileMap = getTeachingMap(path, dst)

    tmpKey = fileMap.keys()[0]
    tmpValue = fileMap[tmpKey]

    print(reverse)
    if (reverse):
        tmp = tmpKey

        tmpKey = tmpValue
        tmpValue = tmp

    print('Example output: \n' + tmpKey + ' -> ' + tmpValue)
    confirm = raw_input('Apply? [y/N] ')

    if (confirm.lower() == 'y'):
        renameFiles(fileMap, dryRun, reverse)
    else:
        print('Operation aborted. No changes has been made.')

def renameFiles(fileMap, dryRun = False, reverse = False):
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
        if (reverse):
            tmp = key

            key = value
            value = tmp

        print('Move: ' + key + ' -> ' + value)
        done = done + 1

        # Progress
        print(str(done) + '/' + str(count) + '(' + str(round(float(done) / count * 100, 2)) + '%)\n')

        if (not dryRun):
            os.renames(key, value)

def getFilesByExt(path, extension):
    """
    Returns a list of all files in the given directory that matches
    the given extension

    Arguments:
    path      : The folder to search in
    extension : The extension to search for

    Returns:
    List of all absolute file paths with a matching extension
    Example: /home/john/cats/bob.png
    """

    # Get all .htm files
    fileList = os.listdir(path)

    htmFiles = []

    for fileName in fileList:
        root, ext = os.path.splitext(fileName)

        if (ext == extension):
            htmFiles.append(path + '/' + fileName)

    return htmFiles

def filterString(text):
    """
    Replace/Remove invalid file characters

    text : The text to search in

    Returns:
    A filtered version of the given string
    """
    # Remove invalid chars
    text = text.strip()

    text = text.replace(':', ';')
    text = text.replace('?', '')
    text = text.replace('"', "'")

    return text;

def getTeachingMap(path, dst = ''):
    """
    Return a dictionary of original file path to descriptive file path
    """

    print('[INFO] Generating file rename map...')
    numberToBookDict = getNumberToBookDict(path)

    ''' Extract:
    <tr>
        <td width="17%" class=teachingtextbg height="21">10-01-97</td>
        <td width="15%" class=teachingtextbg height="21">W3001</td>
        <td width="60%" class=teachingtextbg>Genesis 1</td>
        <td width="8%" class=teachingtextbg align="center" height="21">
        <a href="W3001.mp3">
        <img border="0" src="play-dbg.gif" width="33" height="33"></a></td>
    </tr>
    '''

    # Open each .htm file and extract number and teaching name

    htmFilePaths = getFilesByExt(path, '.htm')

    teachingMap = {}

    for htmFile in htmFilePaths:
        f = open(htmFile, 'r')

        # Init page vars
        inPairSection = False
        teachingNumber = ''
        teachingName = ''
        book = ''
        category = ''

        for line in iter(f.readline, ''):
            line = line.strip()
            #print(line)

            # Section start and end
            if (line == "<tr>"):
                inPairSection = True
            elif (line == "</tr>"):

                if (inPairSection):
                    if (teachingName != '' and teachingNumber != ''):
                        book = numberToBookDict[teachingNumber]
                        teachingMap[path + '/' + teachingNumber] = dst + '/' + book + '/' + category + '/' + teachingName + '.mp3'

                        #print(path + '/' + teachingNumber + ' -> ' + dst + '/' + book + '/' + category + '/' + teachingName + '.mp3')
                        teachingName = ''
                        teachingNumber = ''
                        book = ''
                        category = ''

                    inPairSection = False


            if (inPairSection):

                tmp = line.split('>')

                tmp[0] = tmp[0].replace('teachingtextbg', 'teachingtext')

                # Teaching number
                # <td width="15%" class=teachingtextbg height="21">W3001</td>

                if (tmp[0] == '<td width="15%" class=teachingtext height="21"'):

                    teachingNumber = tmp[1].split('<')[0] + '.mp3'

                    if (teachingNumber[0] == 'W'):
                        category = 'Verse-By-Verse'
                    else:
                        category = 'Topical'


                if (category == "Verse-By-Verse"):
                    # Teaching name (Verse by Verse)
                    # <td width="60%" class=teachingtext>Genesis 3</td>
                    if (tmp[0] == '<td width="60%" class=teachingtext'):
                        teachingName = filterString(tmp[1].split('<')[0])
                else:
                    # Teaching name (Topical)
                    #                   0                            1                  2
                    # <td width="60%" class=teachingtextbg|He Didn't Say That!<br|Genesis 3:3</td|
                    if (tmp[0] == '<td width="60%" class=teachingtext'):
                        teachingName = filterString(tmp[2].split('<')[0]) + ' - ' + filterString(tmp[1].split('<')[0])

                    #print(teachingNumber)

        f.close()

    # Missing entry
    teachingNumber = 'S3067.mp3'

    book = numberToBookDict[teachingNumber]
    teachingName = 'Leviticus 17;11 - The Lamb Slain'
    category = 'Topical'

    teachingMap[path + '/' + teachingNumber] = dst + '/' + book + '/' + category + '/' + teachingName + '.mp3'

    return teachingMap

def getNumberToBookDict(path):
    """
    Return a dictionary of teaching file path to book Name
    """

    files = getFilesByExt(path, '.m3u')

    files.remove(path + '/97 - All Teachings.m3u')
    files.remove(path + '/98 - All In-Depth Teachings.m3u')
    files.remove(path + '/99 - All Verse By Verse Teachings.m3u')

    numberToBookDict = {}

    # Go through all playlists
    for playlist in files:
        f = open(playlist, 'r')

        fileName, ext = os.path.splitext(playlist)

        # Go through all lines in playlist
        for line in iter(f.readline, ''):
            numberToBookDict[line.strip()] = os.path.basename(fileName)

        f.close()

    return numberToBookDict

main()
