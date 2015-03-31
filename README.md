Example:
===========

#convert json to csv

    python json2csv.py -s test.json -t test.csv -b -a "h1,h2,h3"

#convert csv to json

    python json2csv.py -s test.csv -t test.json -i -a "h1,h2,h3" -r

#used for program
import json2csv

json2csv.json_dumps(data, header)
json2csv.csv_dumps(data, header)
