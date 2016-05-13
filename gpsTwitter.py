import pygame
import os
from GPSController import *
import tweet
import buzzer
from picamera import PiCamera

distances = (1000, 900, 800, 700, 600, 500, 400, 300, 200, 100, 50, 25, 10, 5, 2, 1)

class ReportDistance(object):
   def __init__(self, location):
       self.location = location
       self.lastDistance = -1
       self.distancesReported = []
   def getReport(self, lat, lon):
       return self.getString(self.shouldReport(self.location.getDistance(lat, lon)))
   def shouldReport(self, newDistance):
       result = 0 
       for distance in distances:
          if(distance not in self.distancesReported) and (self.lastDistance > distance) and (newDistance < distance):
             self.distancesReported.append(distance)
             result = distance
       self.lastDistance = newDistance
       return result
   def getString(self, distance):
       if(distance == 0):
          return "" 
       elif(distance == 1):
          return "under 1 mile away from " + self.location.name
       return "under " + str(distance) + " miles away from " + self.location.name

class Location(object) :
   def __init__(self, lat, lon, name):
       self.lat = lat
       self.lon = lon 
       self.name = name
   
   def getDistanceString(self, lat, lon):
       return "%.2f miles away from %s" % (self.getDistance(lat, lon), self.name)
  
   def getDistance(self, lat, lon):
       return METERS_TO_MILES * EarthDistance((lat, lon), (self.lat, self.lon))

QualcommRal = Location(35.906033,-78.777359,"Qualcomm Raleigh")
ArkUnion = Location(36.068880, -94.175885, "Razorback Invitational")

WHITE = (255,255,255)
BLACK = (0,0,0)

if __name__ == '__main__':
  dest = QualcommRal
# dest = ArkUnion 
  rd = ReportDistance(dest)
  camera = PiCamera()
  camera.resolution = (800,480)
  twitter = tweet.Twitter()  
# create the controller
  gpsc = GpsController() 
  os.putenv('SDL_FBDEV', '/dev/fb0')
  pygame.init()
  pygame.mouse.set_visible(False)
  lcd = pygame.display.set_mode((800, 480), pygame.FULLSCREEN )
  lcd.fill(BLACK)
  pygame.display.update()

  font_big = pygame.font.Font(None, 100)
  font_med = pygame.font.Font(None, 50)  
  try:
      # start controller
      gpsc.start()
      while True:
          lcd.fill(BLACK)
          if gpsc.fix.mode == MODE_3D:
            text_surface = font_med.render("Coords %.5f, %.5f" % (gpsc.fix.latitude, gpsc.fix.longitude), True, WHITE)
            lcd.blit(text_surface, text_surface.get_rect(center = (400, 50)))
            
            text_surface = font_big.render(time.strftime("%I:%M%p %Z"), True, WHITE)
            lcd.blit(text_surface, text_surface.get_rect(center = (400, 125)))
            
            text_surface = font_big.render("%.2f miles from" % dest.getDistance(gpsc.fix.latitude, gpsc.fix.longitude), True, WHITE)
            lcd.blit(text_surface, text_surface.get_rect(center = (400, 300)))
            
            text_surface = font_big.render(dest.name, True, WHITE)
            lcd.blit(text_surface, text_surface.get_rect(center = (400, 400)))
            report = rd.getReport(gpsc.fix.latitude, gpsc.fix.longitude)
            if(report):
                camera.start_preview()
                buzzer.play5()
                filename = '/home/pi/Projects/capture' + str(dest.getDistance(gpsc.fix.latitude, gpsc.fix.longitude)) + '.jpg'
                camera.capture(filename, use_video_port = True)
                camera.stop_preview()
                twitter.tweet(report + hashtags, gpsc.fix.latitude, gpsc.fix.longitude, filename)
          else:
            text_surface = font_big.render("No Fix Yet", True, WHITE)
            lcd.blit(text_surface, text_surface.get_rect(center = (400, 150)))
          pygame.display.update() 
          if gpsc.fix.mode == MODE_3D:
             time.sleep(6)
          else:
             time.sleep(.5)

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
      #wait for the thread to finish
      gpsc.join()
      
  print "Done"
