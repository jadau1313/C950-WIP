import csv
#make sure csv files encoded UTF-8
with open('Addresses.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    addresses = []

    for row in readCSV:
        print(row[0], row[1])
        address = row[1]
        addresses.append(address)

print(addresses)

with open('Distances.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    distances = []

    for row in readCSV:
        print(row)
        distances.append(row)
    print(distances)
with open('Packages.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    packageData = [[]]
    for row in readCSV:
        print(row[0])