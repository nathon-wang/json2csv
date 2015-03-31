from __future__ import print_function

import six
import sys
import os
import json
import csv
import codecs
import getopt

class NotValidJsonException(Exception):pass

def to_readable(s):
    if s is None:return ''

    if six.PY2:
        if isinstance(s, unicode):
            return s.encode('utf-8')
        else:
            return s
    else:
        return s

def json_dumps(jdatas, headers):
    for data in jdatas:
        yield [data.get(header, '') for header in headers]

def csv_dumps(ldatas, headers):
    for data in ldatas:
        yield {header:data[idx] for idx, header in enumerate(headers) if header != ''}

def jsonFile2csvFile(jsonFile, csvFile, headers=None, bom=False):
    jData = json.loads(open(jsonFile, 'r').read())
    if isinstance(jData, dict):
        jsonData = [jData, ]
    elif isinstance(jData, (tuple, list)):
        jsonData = jData
    else:
        raise NotValidJsonException()

    if not headers:
        headers = jsonData[0].keys()

    csv_data = list(map(lambda x:list(map(to_readable, x)), json_dumps(jsonData, headers)))
    if bom:
        with open(csvFile, 'wb') as f:
            f.write(codecs.BOM_UTF8)

    with open(csvFile, 'w+') as f:
        cw = csv.writer(f)
        cw.writerows(csv_data)

    return

def csvFile2jsonFile(csvFile, jsonFile, headers=None, indent=None):
    cData = csv.reader(open(csvFile, 'r'))
    jsonData = list(csv_dumps(cData, headers))
    with open(jsonFile, 'w') as f:
        f.write(json.dumps(jsonData, indent=indent))

    return

HELP_TEMPLATE = '''This program convert a json file to csv file
(-s|--source) source file
(-t|--target) target file
(-r|--reverse) csv file to json file
(-a|--header) include header. Example: -a "h1,h2"
(-i|--indent) target json file indent
(-b|--bom) add BOM_UTF8 to file
'''

def usage():
    print(HELP_TEMPLATE)

if __name__ == '__main__':
    opts, _ = getopt.getopt(sys.argv[1:], "hs:t:ra:bi:", ["help", "source=", "target=", "reverse=", "header=", "bom", "indent="])
    reverse, headers, bom, indent = False, None, False, None
    srcFile, dstFile = None, None
    for opt, arg in opts:
        if opt in ("-s", "--source"):
            srcFile = arg
        elif opt in ("-t", "--target"):
            dstFile = arg
        elif opt in ("-r", "--reverse"):
            reverse = True
        elif opt in ("-a", "--header"):
            headers = arg.split(',')
        elif opt in ("-i", "--indent"):
            indent = int(arg)
        elif opt in ("-b", "--bom"):
            bom = True
        else:
            usage()
            sys.exit(-1)

    if not srcFile or not os.path.isfile(srcFile):
        print('A source file must be needed')
        usage()
        sys.exit(-1)

    if not dstFile:
        print('A target file must be needed')
        usage()
        sys.exit(-1)

    if reverse:
        csvFile2jsonFile(srcFile, dstFile, headers=headers, indent=indent)
    else:
        jsonFile2csvFile(srcFile, dstFile, headers=headers, bom=bom)

