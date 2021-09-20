# reads a threaddat file and returns the data in a dict
import os
import csv

def getThreadDataFiles():
    # open and return a combined array of all available threads
    thread_files = []
    for file in os.listdir('./resources'):
        if file.endswith('.threaddat'):
            # print(os.path.join('./resources', file))
            thread_files.append(os.path.join('./resources', file))
    return thread_files

def readThreaddat(file):
    # open the file
    in_file = open(file, 'r')
    # expects the following elements:
    # standard
    # type
    # hint
    # external data
    # internal data
    data = {}
    line = in_file.readline()
    while line:
        # check for type
        if 'standard' in line:
            data['standard'] = threaddatReadValue(line)
        elif 'type' in line:
            data['type'] = threaddatReadValue(line)
        elif 'hint' in line:
            data['hint'] = threaddatReadValue(line)
        elif 'external_data' in line:
            # read all the following lines
            external_lines = threaddataReadGroupedData(in_file)
            data['external_data'] = threaddatLinesToArr(external_lines)
        elif 'internal_data' in line:
            # read
            internal_lines = threaddataReadGroupedData(in_file)
            data['internal_data'] = threaddatLinesToArr(internal_lines)
        line = in_file.readline()

    return data

def threaddatLinesToArr(lines):
    # convert to array
    # this is dirty
    # save as a temp file
    arr = []
    with open('screw_temp.tmp','w') as temp_file:
        temp_file.writelines(lines)
        temp_file.close()
    with open('screw_temp.tmp','r') as temp_file:
        dict = csv.DictReader(temp_file)
        for d in dict:
            entry = {}
            # print(d)
            for key in d:
                # print(key)
                if key != 'thread_class' and key != 'screw_size':
                    entry[key] = float(d[key])
                else:
                    entry[key] = d[key]
                # print(entry[key])
            arr.append(entry)
        temp_file.close()
        os.remove('screw_temp.tmp')
        return arr


def threaddataReadGroupedData(file):
    # read until a '}'
    line = file.readline()
    grouped = []
    while line:
        if '}' in line:
            return grouped
        else:
            grouped.append(line)
        line = file.readline()
    return grouped


def threaddatReadValue(line):
    colon_index = line.index(':')
    start = line.index('"',colon_index) + 1
    end = line.index('"',start)
    value = line[start:end]
    return value

if __name__ == '__main__':
    file = './resources/unified.threaddat'
    print(readThreaddat(file))
