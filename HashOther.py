import HashTable
import csv
#gets the size of the hash table to create
with open('Packages.csv') as csvfile:
    rows = 0
    IdArr = []
    rowList = []
    size = 0
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:  # make sure csv encoded UTF-8
        rowList.append(row)
        rows += 1
        size += 1
        IdArr.append(row[0])

myHash = HashTable.HashTableDirect(size)
pkglist = []
with open("Packages.csv") as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    pInternalId = 0
    for pkg in readCSV:
        pID = int(pkg[0])
        pInternalId += 1
        pAddress = pkg[1]
        pCity = pkg[2]
        pState = pkg[3]
        pZip = pkg[4]
        pDeadline = pkg[5]
        pWeight = pkg[6]
        pInfo = pkg[7]
        pStatus = "At the hub"
        # package object
        package = HashTable.Package(pID, pInternalId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pInfo, pStatus)
        #print(package)
        # insert into hashtable
        myHash.insert(pInternalId, package) #uses internal Id, based on pkg position in csv file rather than provided Id
        pkglist.append(package)
#myHash.print()
myHash.print_bucket(6)
print(myHash.table[5])
myHash.print_bucket(0)


myPkg = myHash.search(8)
print(myPkg)
myAddress = myPkg.Address
print(myAddress)



#othHash = HashTable.HashTableDirect(size)
#othHash.insert(1, ['Dog', 'Shadow', 4])
#othHash.print()


