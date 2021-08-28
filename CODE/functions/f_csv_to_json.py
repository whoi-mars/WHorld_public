'''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DESCRIPTION:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Script contains function that converts CVS file into JSON

'''
import csv
import json


# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'Case #' to be the primary key
            key = rows['Case #']
            data[key] = rows

    # Open a json writer, and use the json.dumps()
    # function to dump data

    # CREATE JSON FILE for each case
    i = 1
    for cases in data:
        case_name = 'case' + str(i)
        j = json.dumps(data[case_name])

        with open(jsonFilePath + case_name, 'w') as f:
            f.write(j)
            f.close()
            print('JSON # (%d) FILE CREATED!' % i)
        i = i + 1

