import csv
#gets the size of the hash table to create
#This assumes that the program will always load its packages from a file called 'Packages.csv'.
#This could be improved upon by creating a separate method that takes a filename as
#input and loads that file
'''
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
#    print(rows)
#print(IdArr)
#print(rowList[0][0])  # index inside of an index since rowList is a list of lists
#print(size)
'''

#Direct hash table class. The hash table
class HashTableDirect:

    def __init__(self, size): #size = rows, call with obj = HashTableDirect(size) or can replace size here with size=rows, either way works

        self.size = size  # size  # size determined by number of packages in csv file, ids are sequential
        self.table = [[] for i in range(size)]

    def __setitem__(self, key, value):
        self.table[key] = value

    def __getitem__(self, key):
        return self.table[key]
    #make table iteratable
    def __iter__(self):
        return iter(self.table)

    '''
    def findindex(self, key):
        index = 0
        #for row in rowList:
        for i in range(size):    
            index += 1
            #if row[0] == key:
            if self.table[0] == index:
                return index
            else:
                return -1
'''
    '''
    def hash(self, key): #get this to work later; probably an index issue. use safehash for now
        def findindex(key):
            index = -1
            for row in rowList:
                index += 1
                if row[0] == key:
                    return index
                else:
                    return -1
        
        #size = self.size
        '''
    '''The reason to hash this way instead of using the key directly is to be proactive. What if the ID format changes and we have random or many digit
        or even non integer characters as IDs in the future? Basically, this creates enough buckets for each item in the package list and packages
        are assigned to buckets based off of their index, not their key. For this project, the index+1 will always equal the key. Collision free
        direct hashing solution that is scalable to the size of the list taken from the csv file'''
    '''
        index = findindex(key)
        hashId = (index + 1) % size
        return hashId
'''

    #Hashing function that uses keyMODsize to create a unique hash ID. There is risk of collisions if the format of the package IDs changes to a nonsequential format (ie
    # if there is a package.csv of size 10 and the list contains packages with IDs 21 and 51, then both packages will collide at bucket 1). This risk is mitigated
    #elsewhere in the program in the loadPackages() method of the main file by creating an internal ID for each package associated with the position in the csv file
    #rather than the ID itself. Effectively, this will mean a suquential list of IDs which will be unique and each package will always be in its
    #own bucket.
    def safehash(self, key):
        hashID = key % self.size
        return hashID


    #inserts a package into the hash table
    def insert(self, key, item):
        index = self.safehash(key)
        self.table[index] = item


    #Removes an item from the hash table. This was unnecessary for this program.
    def remove_item(self, key):
        index = self.safehash(key)
        if self.table[index] is not None:
            self.table[index] = None
            print(f'Item {key} has been deleted')
        else:
            print(f'Item {key} not found')

    #Searches hashtable with internal ID as input, returns a packages
    def search(self, key):
        index = self.safehash(key)
        return self.table[index]


    def print(self):
        for i in range(len(self.table)):
            #print('Key {} and address {}'.format(i + 1, pkgHash.search(i + 1)))
            print('Key {} and address {}'.format(i + 1, self.search(i + 1)))

        '''for pkg in self.table:
            for key, value in pkg:
                print(f'Key: {key}, Value: {value}')
'''
    def print_bucket(self, index):
        if index < 0 or index >= self.size:
            print("invalid bucket")
            return
        print(f'Bucket {index}: {self.table[index]}')

    def print_bucket_singleval(self, index, pkgindex):
        if index < 0 or index >= self.size or pkgindex < 0 or pkgindex > 8:
            print("invalid")
            return

        print(f'Bucket {index}: {self.table[index]}')


#Package class
class Package:
    def __init__(self, Id, internalId, Address, City, State, Zip, deadline, weight, info, status):
        self.Id = Id
        self.internalId = internalId
        self.Address = Address
        self.City = City
        self.State = State
        self.Zip = Zip
        self.deadline = deadline
        self.weight = weight
        self.info = info
        self.status = status
        self.departtime = None
        self.deliverytime = None
        self.trkId = 0
        self.has_constraint = False

    #printable
    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.Id, self.internalId, self.Address, self.City, self.State, self.Zip, self.deadline, self.weight, self.info, self.status,
            self.departtime, self.deliverytime, self.trkId, self.has_constraint)



'''
pkgHash = HashTableDirect(size)
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
        pStatus = 'At the hub'
        # package object
        package = Package(pID, pInternalId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pInfo, pStatus)
        # insert into hashtable
        pkgHash.insert(pID, package)
'''
#pkgHash.print()
#pkgHash.print_bucket(3)
#print(pkgHash.search(2))


#for i in range(len(pkgHash.table)):
 #   print('Key {} and address {}'.format(i + 1, pkgHash.search(i + 1)))

#maybe we don't even need a hash table class? I can just use a list of lists from the csv file and access them
#as shown below
'''
print(rowList[5][2], rowList[5][4])
counter=0
while counter<size:
    print(rowList[counter][1], rowList[counter][2], rowList[counter][5])
    counter+=1
'''