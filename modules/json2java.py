

def main(contents):
    allVariables = parseJSON(contents)
    file = openOutputFile()
    if file is not None and allVariables is not None:
        writeToFile(file,allVariables)


def parseJSON(contents):
    contents = contents.strip()
    contents = contents[1:len(contents) - 1]
    contents = contents.strip()
    data = contents.split(':', 1)
    if data[0].strip() != '"data"':
        return None
    else:
        arr = data[1].strip()
        arr = arr[1: len(arr) - 1]
        arr = arr.strip()
        arr = arr[1:len(arr)]
        rows = arr.split('{')
        row=rows[0]
        row = row.strip()
        keys = row.split(',')
        if len(keys) > 5:
            del keys[len(keys) - 1]
        allVariables = {}
        for key in keys:
            key = key.strip()
            if len(key) <1:
                continue
            if key[0] != '"':
                continue
            pair = key.split(':', 2)
            tag = pair[0].strip()
            tag = tag.split('"', 2)
            tag = tag[1]
            value = pair[1].strip()
            if value[0] == '"':
                allVariables[tag] = 'String'
            elif value[0] == '[':
                value= value[1:len(value)]
                value=value.strip()
                if value[0] == '"':
                    allVariables[tag] = 'String[]'
                else:
                    allVariables[tag]= 'int[]'
            else:
                allVariables[tag] = 'int'
        return allVariables


def writeToFile(file, allVariables):
    file.write('public class JSONmodel {\n\n')
    for variable in allVariables:
        file.write('\tprivate '+allVariables[variable]+' '+variable+';\n')
    file.write('\n\tpublic JSONmodel() { }\n\n}')
    file.close()
    print('Java model made successfully from JSON.\n')
    input=readFile()
    if input is not None:
        text = input.read()
        print(text)


def openOutputFile():
    try:
        file = open('data/JSONmodel.java', 'w')
        return file
    except IOError as e:
        print(e)
        return None

def readFile():
    try:
        file = open('data/JSONmodel.java', 'r')
        return file
    except IOError as e:
        print(e)
        return None