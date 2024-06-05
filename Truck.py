from datetime import timedelta

#truck class
class Truck:
    truckspeed = 18
    pkgmax = 16

    def __init__(self, truckId, pkgs=[], speed=truckspeed, pkg_max=pkgmax):
        self.truckId = truckId
        self.pkgs = pkgs  # this should be a list of pkgs
        self.pkg_ids = []
        self.speed = speed
        self.pkg_max = pkg_max
        self.departure = None
        self.deliveredtimes = []
        self.mileage = 0
        self.returntime = None
        self.hubloc = '4001 South 700 East'
        self.enroute = False
        self.timediff = timedelta(hours=8, minutes=0)


    #keeping for further testing but not used in current build
    def add_pkg_to_trk(self, package):
        if len(self.pkgs) < self.pkg_max:
            self.pkgs.append(package.Id)
            self.pkg_ids.append(package.Id)
            package.trkId = self.truckId
            package.status = 'en route'

    #the second add_pkg_to_trk method. Replaces the first one, which appends pkg ids to the truck
    #in the main program, the methods used to call this method will handle appending the ids to the pkg id list
    def add_pkg_to_trk2(self, packageid, hashtbl):
        if len(self.pkgs) < self.pkg_max:
            pkg = hashtbl.search(packageid)
            self.pkgs.append(pkg)
            #self.pkg_ids.append(packageid)
            pkg.trkId = self.truckId
            pkg.status = 'en route'

    #removes the package from the truck, sets the truck's en route status (probably could be more efficiently done elsewhere but not overly costly to performance),
    #updates the distance traveled by the truck, sets delivery time, updates package status to 'delivered', and appends the mileage and delivery stamps to the
    #delivery times list
    def deliverpkg(self, hashtbl, pkgId, distance):
        pak = hashtbl.search(pkgId)
        self.pkg_ids.remove(pkgId)
        self.enroute = True
        self.updateDistance(distance)
        self.timediff += timedelta(minutes=(distance / self.speed * 60))
        pak.deliverytime = self.timediff
        pak.status = 'Delivered'
        self.deliveredtimes.append([self.mileage, self.timediff])


    #updates the distance
    def updateDistance(self, milestraveled):
        self.mileage += milestraveled


    #Returns truck to hub. The distance to the hub is used as input. Sets the return time
    #and sets the truck's enroute status to false. Records mileage and timestamps of the return and updates
    #total distance traveled.
    def returnTruck(self, distance):
        self.updateDistance(distance)
        self.timediff += timedelta(minutes=(distance / self.speed * 60))
        self.deliveredtimes.append([self.mileage, self.timediff])
        self.enroute = False
        self.returntime = self.timediff
    '''def printpkgs(self):
        prntlist = []
        for pkg in self.pkgs:
            pakId = pkg.internalId
            prntlist.append(pakId)
        print(prntlist)'''
