import csv
import HashTable
from HashTable import HashTableDirect


class Package:
    def __init__(self, Id, Address, City, State, Zip, deadline, weight, info):
        self.Id = Id
        self.Address = Address
        self.City = City
        self.State = State
        self.Zip = Zip
        self.deadline = deadline
        self.weight = weight
        self.info = info

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (
            self.Id, self.Address, self.City, self.State, self.Zip, self.deadline, self.weight, self.info)


def loadPackageData(csvFileName):
    with open(csvFileName) as csvfile:
        rows = 0
        rowList = []
        size = 0
        readCSV = csv.reader(csvfile, delimiter=',')
        next(readCSV)
        for pkg in readCSV:
            pID = int(pkg[0])
            pAddress = pkg[1]
            pCity = pkg[2]
            pState = pkg[3]
            pZip = pkg[4]
            pDeadline = pkg[5]
            pWeight = pkg[6]
            pInfo = pkg[7]
            # package object
            pkg = Package(pID, pAddress, pCity, pState, pZip, pDeadline, pWeight, pInfo)
            # insert into hashtable
            pkgHash.insert(pID, pkg)
            size += 1


pkgHash = HashTableDirect(HashTable.size) #pulls size from HashTable.py
loadPackageData('Packages.csv')
#pkgHash.print_bucket(5) #note bucket 0 is pkg 40
# pkgHash.print()

# for i in range(len(pkgHash.table)):
#   print('Key {} and address {}'.format(i+1, pkgHash.search(i+1)))

# pkgHash.print()
# print("ID {}")
# print("ID: {} , Address: {}".format(i+1, pkgHash.search(i+1)))
