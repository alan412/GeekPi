from GPSController import *


distances = (1,2,5,10,25,50,100,200,300,400,500,600,700,800,900,1000)

class Location(object) :
   def __init__(self, lat, lon, name):
       self.lat = lat
       self.lon = lon 
       self.name = name
       self.lastDistance = -1
   def getString(self, lat, lon):
       newDistance = METERS_TO_MILES * EarthDistance((lat, lon), (self.lat, self.lon))
       result = ""
       print "(" + str(newDistance) + ")"
       for distance in distances:
          if(self.lastDistance > distance) and (newDistance < distance):
             if(distance == 1):
                result = "under 1 mile away from " + name
             else:
                result = "under " + str(distance) + " miles away from " + name
       self.lastDistance = newDistance
       return result

QualcommRal = Location(35.906033,-78.777359,"Qualcomm Raleigh")
ArkUnion = Location(36.068880, -95.175907, "Razorback Invitational")
Home = Location(35.769422333, -78.83893282, "Home")

if __name__ == '__main__':
#  dest = ArkUnion 
  dest = Home  
# create the controller
  gpsc = GpsController() 
  try:
      # start controller
      gpsc.start()
      while True:
          if gpsc.fix.mode == MODE_3D: 
            print "latitude ", gpsc.fix.latitude
            print "longitude ", gpsc.fix.longitude
            dispStr = dest.getString(gpsc.fix.latitude, gpsc.fix.longitude)
            if dispStr:
              print dispStr
          else:
            print "No fix yet"
          time.sleep(0.5)

  #Ctrl C
  except KeyboardInterrupt:
      print "User cancelled"

  #Error
  except:
      print "Unexpected error:", sys.exc_info()[0]
      raise

  finally:
      print "Stopping gps controller"
      gpsc.stopController()
      #wait for the tread to finish
      gpsc.join()
      
  print "Done"
