#Jacob Sutherland WGU ID 007416153 04JUN2024
import os
import re
from datetime import datetime, timedelta
import csv
# import animationtest
import Truck
from Truck import Truck
import HashTable
import subprocess
import time
import runpy

#loads packages from csv into hashtable
#complexity: space O(N) , time O(N)
def loadPackages():
    print('Loading packages into hash table...')
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
            package = HashTable.Package(pID, pInternalId, pAddress, pCity, pState, pZip, pDeadline, pWeight, pInfo,
                                        pStatus)
            # print(package)
            # insert into hashtable
            myHash.insert(pInternalId,
                          package)  # uses internal Id, based on pkg position in csv file rather than provided Id
            pkglist.append(package)
    '''myHash.print_bucket(6)
    print(myHash.table[5])
    myHash.print_bucket(0)

    myPkg = myHash.search(8)
    print(myPkg)
    myAddress = myPkg.Address
    print(myAddress)'''
    return myHash


#load addresses from hashtable
#complexity: space O(N) / time O(N)
def loadAddresses():
    # print('Loading addresses...')
    with open('Addresses.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        addresses = []

        for row in readCSV:
            # print(row[0], row[1])
            address = row[1]
            address = address[1:]
            addresses.append(address)
    return addresses

#another version that does the same, keeping for now but may remove later O(N)/O(N)
def loadAddresses2():
    with open('Addresses.csv') as csv_file:
        address_list = []

        # Create a reader object which will iterate over lines in the packages.csv file
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Iterate through the reader and parse the information from each row
        for row_text in csv_reader:
            # Each row contains the full address for a location. Only parse the street address for the address list
            full_address = row_text[0].split("\n")
            street_address = full_address[1].strip()
            address_list.append(street_address)
    return address_list


#gets a count of addresses O(N) for both time and space
def addressCount():
    num_addresses = 0
    with open('Addresses.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            num_addresses = num_addresses + 1

    return num_addresses

#pulls distances from csv, complexity of O(N) for both space and time
#method is obselete, use loadDistances2()
def loadDistances():
    print('Loading distances...')
    with open('Distances.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        distances = []

        for row in readCSV:
            # print(row)
            distances.append(row)
        # print(distances)

#loads distances from csv file, this version is necessary for finding the distance between two points
#O(N^2) for both space and time complexities
def loadDistances2():
    with open('distances.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        num_addresses = addressCount()
        distance_data = [[0 for x in range(num_addresses)] for y in range(num_addresses)]
        address1index = 0
        for address1 in csv_reader:
            for address2index in range(num_addresses):
                if address1[address2index] != '':
                    distance_data[address1index][address2index] = float(address1[address2index])
                    distance_data[address2index][address1index] = float(address1[address2index])
            address1index += 1

        return distance_data

#not used, not necessary, O(1)
'''def initializeTrucks():
    print('Building trucks...')
    truck1 = Truck(1)
    truck1.pkgs = []

    truck2 = Truck(2)
    truck3 = Truck(3)
    return truck1, truck2, truck3
    # print(truck1.speed)'''

#used in early testing, O(1), obsolete, may be useful during further testing
def lookuppkginfo(pkgId, hashtbl): # make this obsolete, use get_user_package instead
    id = pkgId
    pkglistsize = hashtbl.size
    if id == pkglistsize: id = 0
    if id < 0 or id > pkglistsize:
        print('Error! No package with that ID.')
        userinterface(hashtbl)
    # hashy = loadPackages()
    # return hashy.print_bucket(id)
    return hashtbl.print_bucket(id)


'''
def display_all_truck_packages(trucklist, hashtbl): #testing 6/5

    for truck in trucklist:
        lookup_truck_pkgs_at_time(truck, hashtbl)

    pass'''

#takes a package, time, and ht as input and finds the status at the given time by comparing the user entered time
#to the delivery and departure times and updating accordingly
#space-time complexity of O(1) / O(1)
def lookup_pkg_status_by_time(hashtbl, package, usertime): # 5/31 this seems to be working as expected
    #had issues with timedelta vs datetime comparisons so had to do some conversions
    converted_user_time = timedelta(hours=usertime.hour, minutes=usertime.minute)
    #uses a duplicate package in case changes occur in the HT due to repeated status searches
    #might not be necessary now, but was during early testing. Don't feel like updating dependencies; it is working as is
    OGPackageinfo = package
    #printabledeliverytime = package.deliverytime
    OGprintableconversion = datetime.strptime(str(OGPackageinfo.deliverytime), "%H:%M:%S")
    OGprintabletime = OGprintableconversion.time()
    printabledeliverytimeConversion = datetime.strptime(str(package.deliverytime), "%H:%M:%S")
    printabledeliverytime = printabledeliverytimeConversion.time()
    convertdepartime = datetime.strptime(str(package.departtime), "%H:%M:%S")
    converteddeparttime = convertdepartime.time()
    paknineupdatetime = '10:20'
    DTobject = datetime.strptime(paknineupdatetime, "%H:%M")
    paknineupdatetimeobj = DTobject.time()
    convertedpakninedelta = timedelta(hours=paknineupdatetimeobj.hour, minutes=paknineupdatetimeobj.minute)
    if package.departtime is timedelta:
        dtobj = datetime.strptime(package.departtime, '%H:%M')
        package.departtime = dtobj.time()
    #convertedusertime = timedelta(hours=usertime.hour, minutes=usertime.minute)

    #handle the package 9 problem. Alternatively, I could create a method that finds packages with a status that contains
    #the substring 'Wrong address' to identify this package elsewhere in the program and then have it return that
    #package here instead of calling 9 directly. In a real world scenario it would be ideal since any package
    #could theoretically have the wrong address listed but this way works and meets project requirements.
    if package.internalId == 9:
        id = package.internalId
        if usertime < paknineupdatetimeobj:
            package.Address = '300 State St'
            package.Zip = '84103'
            package.info = 'Wrong address listed'


        else:
            package.Address = '410 S State St'
            package.Zip = '84111'
            package.info = 'Address corrected'

    if usertime < package.departtime:
        package.status = 'at the hub'
        printabledeliverytime = None

    elif converted_user_time < package.deliverytime:
        package.status = 'en route'
        printabledeliverytime = None

    else:
        package.status = 'Delivered'
        printabledeliverytime = OGprintabletime

    id = package.internalId

    #further handle package 9 outputs
    if package.internalId == 9 and usertime < paknineupdatetimeobj and usertime >= package.departtime: package.status = 'en route, awaiting instructions for new address'
    if package.internalId == 9 and usertime >= paknineupdatetimeobj and converted_user_time < package.deliverytime:  package.status = 'en route to updated address'

    print(f'Package {id}: \n Address: {package.Address}, Zip: {package.Zip}, City: {package.City},\n Deadline : {package.deadline}, Weight: {package.weight}, '
          f'Delivery status: {package.status}, Delivery time: {printabledeliverytime}, Truck number: {package.trkId}, Departure time: {package.departtime}')



#prompts the user for a package ID
# O(1) / O(1)
#handles errors recursively; user cannot proceed until proper format is entered
def get_user_package(hashtbl):
    pkgId = input('Enter a package ID')
    pkgId = int(pkgId)
    pkglistsize = hashtbl.size
    if pkgId < 0 or pkgId > pkglistsize:
        print('Error! No package with that ID.')
        return get_user_package(hashtbl)
    return hashtbl.search(pkgId) #learned the hard way that I need to remember to return the function, not just call it
    #hashtbl.search


#O(1) checks if the user input a valid time
def validate_time_format(time_string):
    #Define the regex pattern for HH:MM format
    pattern = r'^\d{2}:\d{2}$'

    #Check if the input matches the pattern
    if re.match(pattern, time_string):
        # Extract hours and minutes
        hours, minutes = map(int, time_string.split(':'))

        #Validate the range of hours and minutes
        if 0 <= hours < 24 and 0 <= minutes < 60:
            return True
    return False

#O(1) for both, prompts user for a time, checks the validity of input
def get_user_time():
    usertime = input('Choose a time:   (use xx:xx format)')
    if validate_time_format(usertime) == True:
        DTobject = datetime.strptime(usertime, "%H:%M")
        timeobj = DTobject.time()
        return timeobj
    else:
        print('Please enter a valid time')
        return get_user_time() #learned the hard way that I need to remember to return the function, not just call it hashtbl.search


#shows all package status by time, prompts user for time internally
#complexity: time O(N) / space O(1)
def lookup_all_by_time(hashtbl):
    usertimeobj = get_user_time()
    pkglist = hashtbl.table
    for pkg in pkglist:
        if pkg is not None:
            lookup_pkg_status_by_time(hashtbl, pkg, usertimeobj)
            print(f'On truck: {pkg.trkId}')
    #pass

#looks up packages on a specific truck at a specific time
#O(N) for time, O(1) space
def lookup_truck_pkgs_at_time(truck, time,  hashtbl): #testing 6/5 -- print packages on each truck
    #time = get_user_time()
    pkglist = hashtbl.table
    print(f'Packages on truck {truck.truckId} at {time}')
    for pkg in pkglist:
        if pkg.trkId == truck.truckId:
            lookup_pkg_status_by_time(hashtbl, pkg, time)
            #pak = hashtbl.search(pkg)
            #lookup_pkg_status_by_time(hashtbl, pak, time)
        #print('package')



#loads the UI for the program
def userinterface(hashtbl):
    cleanconsole()
    print('Select from the following options or enter Q to quit')
    print('1. Lookup Package')  # address deadline city zip weight status
    print('2. View all package statuses by time')
    print('3. View mileage daily total')
    print('4. View packages on trucks')
    userinput = input()
    userinput.lower()
    if userinput == 'q':
        quit()
    if userinput == '1':
        cleanconsole()
        userinputtime = get_user_time()
        newHash = hashtbl
        userinputpkg = get_user_package(newHash)
        lookup_pkg_status_by_time(newHash, userinputpkg, userinputtime)

        inp = input("Press enter to proceed or q to quit")
        if inp.lower() == 'q': quit()
        userinterface(hashtbl)


    if userinput == '2':
        cleanconsole()
        #usertime = input('Choose a time between 08:00 and 17:00 (user xx:xx format)')
        #DTobject = datetime.strptime(usertime, "%H:%M")
       #timeobj = DTobject.time()
        #print(timeobj)
        # show all package statuses on all trucks
        # pass
        newHash = hashtbl
        lookup_all_by_time(newHash)
        #lookup_all_by_time_and_truck(hashtbl, truck1)
        inp = input("Press enter to proceed or q to quit")
        if inp.lower() == 'q': quit()
        userinterface(hashtbl)
    if userinput == '3':
        cleanconsole()
        totalmileage(trucklist)
        #miles_traveled = 100  # replace with function call to find total miles traveled
        #print(f'Total miles traveled: {miles_traveled}')
        inp = input("Press enter to proceed or q to quit")
        if inp.lower() == 'q': quit()
        userinterface(hashtbl)

    if userinput == '4':
        cleanconsole()
        usertime = get_user_time()
        lookup_truck_pkgs_at_time(truck1, usertime, hashtbl)
        lookup_truck_pkgs_at_time(truck2, usertime, hashtbl)
        lookup_truck_pkgs_at_time(truck3, usertime, hashtbl)
        inp = input("Press enter to proceed or q to quit")
        if inp.lower() == 'q': quit()
        userinterface(hashtbl)


#clears the console. This program should be run via command line for best interface results
def cleanconsole():
    os.system('cls' if os.name == 'nt' else 'clear')


'''
def add_pkg_to_trk2(truck, packageid, hashtbl):
    if len(truck.pkgs) < truck.pkg_max:
        pkg = hashtbl.search(packageid)
        truck.pkgs.append(pkg)
        pkg.trkId = truck.truckId
        pkg.status = 'en route'
'''

#space and time complexity of O(N), O(N)
#finds all packages with a known constraint. Package 19 does not meet the criteria, but has a constraint due to others
#future update might include a method that finds associated packages and marks them as a constraint
#for example, finding a package where the info contains "must be delivered with ..." and then returning
#any package numbers listed after this
#The below method meets project requirements, but there is definitely area to optimize this for any type of package list
def identifyconstraintpkgs(hashtbl):
    constraintlist = []
    for key in hashtbl:
        item = key
        if item.deadline != 'EOD' or item.info: #if there is a deadline or extra info, item has a constraint
            item.has_constraint = True
            constraintlist.append(item.internalId)
    constraintlist.append(19)  # other packages must be delivered with 19, so 19 is a constraint too
    # print(constraintlist)
    return constraintlist


#find packages that don't have constraints. As discussed above, there are better ways
#to identify pkg 19 as a constraint pkg, but this works and meets requirements
#O(N) for both time and space complexities
def idnoncontraintpkgs(hashtbl):
    full_list = []
    for pkg in hashtbl:
        full_list.append(pkg.internalId)

    constraintlist = identifyconstraintpkgs(hashtbl)
    # print(constraintlist)
    set1 = set(full_list)
    set2 = set(constraintlist)
    nonconstraintlist = set1.symmetric_difference(set2)

    return list(nonconstraintlist)

#load packages into truck that have been identified as having constraints
#and manually loaded on trucks
#handles package 9, discussed elsewhere how this could be done better
#O(N) for space and time
def loadmanualpkgs(truck, pkgidlist, hashtbl):
    listofassignedpkgs = []
    for pkg in pkgidlist:
        pak = hashtbl.search(pkg)
        if pak.internalId == 9:
            pak.Address = '410 S State St'
            pak.Zip = '84111'
            pak.info = 'Address corrected'
        truck.add_pkg_to_trk2(pkg, hashtbl)
        # truck.add_pkg_to_trk(pak)
        pak.status = 'on truck'
        listofassignedpkgs.append(pkg)
        truck.pkg_ids.append(pkg)
        assignedpkg = hashtbl.search(pkg)
        assignedpkg.trkId = truck.truckId

    # print(truck.pkgs)
    # print(listofassignedpkgs)


#load remaining packages automatically
#O(N) for both space and time
def autoloadremaining(truck, nonconstraintlist,
                      hashtbl):
    for key in nonconstraintlist:
        pkg = hashtbl.search(key)
        if len(truck.pkg_ids) < truck.pkg_max:
            # pak = hashtbl.search(pkg)
            if pkg.status == 'At the hub':
                truck.add_pkg_to_trk2(pkg, myHash)
                # assignedpkg = myHash.search(pkg)
                pkg.status = 'on truck'
                pkg.trkId = truck.truckId
                # trkpkgids.append(key)
                truck.pkg_ids.append(key)
    # print(trkpkgids)


#sorts the packages in a trucks package id list
#O(N^2) for both space and time complexity since it calls findnearestneighbor, which runs in O(N) and is called
# in the loop of this method
def sortpkgontruck(truck, packagelist,
                   hashtbl):
    sorted = []
    pkglist = packagelist
    currentaddress = truck.hubloc
    while len(pkglist) > 0:
        nearestneighbor = findnearestneighbor(currentaddress, pkglist, hashtbl)
        nearestneighborId = nearestneighbor.internalId
        sorted.append(nearestneighborId)
        currentaddress = nearestneighbor.Address
        pkglist.remove(nearestneighborId)
    truck.pkg_ids = sorted


#sort that is called on a list of packages that don't have constraints. This gets
# called before remaining packages are autoloaded. This ensures that when
#the method for autoloading the remaining packages is called, the initial list is already mostly sorted.
#Then, when each package is sorted again on its respective truck, the total distance traveled for the day is
#reduced. This was tested and shaved off about 15 miles.
#O(N^2) for space and for time since findnearestneighbor is called in the loop
def initialsort(pklist, hashtbl): #put the nonconstraint list in?
    sorted = []
    pkgList = pklist
    currAddress = '4001 South 700 East'
    while len(pkgList) > 0:
        nearestneighbor = findnearestneighbor(currAddress, pkgList, hashtbl)
        nearestneighborId = nearestneighbor.internalId
        sorted.append(nearestneighborId)
        currAddress = nearestneighbor.Address
        pkgList.remove(nearestneighborId)
    return sorted


#O(N) for time and space, finds the nearest neighbor of the current package in a list
def findnearestneighbor(curAddress, pkglist, hashtbl):  # need to test
    nearestneighbor = None
    nearestneighbordist = None
    for key in pkglist:
        pkg = hashtbl.search(key)  # gets the package we are interacting with, key is just an int id
        if pkg is not None:
            if nearestneighbor is None:
                nearestneighbor = pkg
                nearestneighboraddress = nearestneighbor.Address
                nearestneighbordist = finddistance(nearestneighboraddress, curAddress)

            else:
                pkgaddress = pkg.Address
                pkgdistance = finddistance(pkgaddress, curAddress)
                if pkgdistance < nearestneighbordist:
                    nearestneighbor = pkg
                    nearestneighbordist = pkgdistance

    return nearestneighbor

#O(1) for both space and time, finds the distance between two points
def finddistance(address1, address2):
    #add1 = address1[0:5]
    #add2 = address2[0:5]
    distancelist = loadDistances2()
    addresslist = loadAddresses()
    addressindex1 = addresslist.index(address1)
    addressindex2 = addresslist.index(address2)
    distancebetween = distancelist[addressindex1][addressindex2]
    return distancebetween

#O(N), though funcionally O(1) since we only have 3 trucks
#prints out the mileage for each truck, then the total for the day
def totalmileage(trucklist):
    miles = 0
    m_list = []
    for truck in trucklist:
        mileage = truck.mileage
        mileage = round(mileage, 2)
        truckid = truck.truckId
        print(f'Mileage for truck {truckid} is {mileage}')
        m_list.append(mileage)
    for m in m_list:
        miles += m

    miles = round(miles, 2)
    print(f"Total miles traveled by all trucks: {miles}")


#O(N) for space, time complexities. Delivers the packages that are on a given truck.
#The calls made in this method serve to record information about all packages
#such as departure times, status updates, as well as calculate the distance
#between the current and next address, which is used as input for the truck class
#deliverypkg method that calculates distance traveled for the truck as well as delivery
#timestamps and total mileage traveled.
def deliverpackages(truck, startTime, hashtbl):
    curAddress = truck.hubloc
    pkglist = truck.pkg_ids

    '''startDTobject = datetime.strptime(startTime, "%H:%M")
    starttime = startDTobject.time()'''
    truck.enroute = True
    index = 0

    #update statuses of packages
    for pkg in truck.pkg_ids:
        pak = hashtbl.search(pkg)
        pak.status = 'en route'
        pak.departtime = startTime
    #while there are packages on the truck, deliver the packages
    while len(truck.pkg_ids) > 0:
        pkg = truck.pkg_ids[0]
        pak = hashtbl.search(pkg)
        # pak.departtime = starttime
        deliveryAddress = pak.Address
        distanceBetween = finddistance(curAddress, deliveryAddress)

        truck.deliverpkg(hashtbl, pkg, distanceBetween)
        curAddress = deliveryAddress

    distToHub = finddistance(curAddress, truck.hubloc)
    truck.returnTruck(distToHub)

#calls the truck intro animation for WGUPS
def animation():
    # subprocess.run('python', 'animationtest.py')
    runpy.run_path('animationtruck.py')









# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    #animation()
    print('Welcome to WGUPS Delivery Management')
    print('Enter the F key to proceed or any other key to quit')
    userval = input()
    if userval != 'f' and userval != 'F':
        # print(userval)

        quit()
    else:
        animation()

        loadPackages()
        myHash = loadPackages()

        loadAddresses()

        #identify packages that don't have constraints
        nonconstraintlist = idnoncontraintpkgs(myHash)
        nonconstraintlist = initialsort(nonconstraintlist, myHash) #sorts the initial list of packages before assigning to trucks, reduces mileage

        # print(nonconstraintlist)
        #initialize and load truck 1
        #manually load constraint packages first
        '''Instead of manually selecting and placing these, I could have created methods to further work with my identifyconstraintpkgs(hashtbl)
         that could handle specific constraints (ie if deadline ! EOD and deadline < 11:30: assign to truck 1...if truck1 full, assign to truck2)
         or group packages together based on the content of the package.info object. The same could be used for the wrong address listed case'''
        truck1 = Truck(1)
        #manually adjust the load size to optimize distance traveled, ensure time constraints are met
        truck1.pkg_max = 13
        trk1constraints = [15, 14, 16, 19, 20, 13, 1, 37, 40]
        loadmanualpkgs(truck1, trk1constraints, myHash)
        # truck1.printpkgs()
        # print(truck1.pkgs)

        #initialize and load truck 2
        truck2 = Truck(2)
        truck2.pkg_max = 16

        #trk2constraints = [3, 6, 25, 18, 10, 29, 30, 31, 34, 36, 38]
        trk2constraints = [3, 18, 10, 29, 30, 31, 34, 36, 38]
        loadmanualpkgs(truck2, trk2constraints, myHash)
        # truck2.printpkgs()

        #initialize and load truck 3
        truck3 = Truck(3)
        trk3constraints = [6, 25, 28, 32, 9, 2, 4, 5, 7, 8]
        #trk3constraints = [28, 32, 9, 2, 4, 5, 7, 8]
        loadmanualpkgs(truck3, trk3constraints, myHash)

        #autoload remaining packages on the trucks
        autoloadremaining(truck1, nonconstraintlist, myHash)
        autoloadremaining(truck2, nonconstraintlist, myHash)
        autoloadremaining(truck3, nonconstraintlist, myHash)
        print(truck1.pkg_ids)
        print(truck2.pkg_ids)
        print(truck3.pkg_ids)

        #sort each truck's package list
        sortpkgontruck(truck1, truck1.pkg_ids, myHash)
        sortpkgontruck(truck2, truck2.pkg_ids, myHash)
        sortpkgontruck(truck3, truck3.pkg_ids, myHash)

        #truck3 has a later departure, so it is important for certain deadlines to be met on truck3
        for pkg in truck3.pkg_ids:
            pak = myHash.search(int(pkg))
            if pak.deadline != 'EOD':
                truck3.pkg_ids.remove(pkg)
                truck3.pkg_ids.insert(0, pkg)
        print(truck3.pkg_ids)


        trucklist = [truck1, truck2, truck3]

        #testing purposes
        for truck in trucklist:
            print(truck.pkg_ids)
        #set the initial start time
        starttime = '08:00'
        startDTobject = datetime.strptime(starttime, "%H:%M")
        startTime = startDTobject.time()

        #deliver the packages for trucks 1 and 2. There are only two drivers, so truck 1 and 2 go out first. Truck 3 goes out as soon as
        #one of the trucks comes back.
        deliverpackages(truck1, startTime,
                        myHash)  # 5/30 deliver packages not working for all pkgs, maybe has to do with same addresses for some of them?
        t2startTime = '08:00'
        t2startTimeObject = datetime.strptime(t2startTime, "%H:%M")
        t2starttime = t2startTimeObject.time()
        #truck2.timediff = truck2.timediff + timedelta(minutes=65)
        deliverpackages(truck2, t2starttime, myHash)
        #deliverpackages(truck2, startTime, myHash)

        #capture return times of first trucks
        t1return = truck1.returntime
        print(f'sooner return t1 {t1return}')
        t2return = truck2.returntime
        print(f'sooner return t2 {t2return}')

        #determine which truck returned first
        soonerReturn = t1return
        if t1return < t2return:
            soonerReturn = t1return
        else:
            soonerReturn = t2return

        #set the start time for truck3 as the return time of the truck that returns first
        truck3.timediff = soonerReturn # need this to ensure delivery times occur after departure times

        #convertsoonerreturn to time
        timeobj = datetime.strptime(str(soonerReturn), '%H:%M:%S')

        soonerReturn = timeobj.time()
        deliverpackages(truck3, soonerReturn, myHash)

        #myHash.print()

        #print(truck2.mileage)
        #myHash.print_bucket(6)
        userinterface(myHash)  # loads userinterface and can be called to go back to home screen of UI in the program


