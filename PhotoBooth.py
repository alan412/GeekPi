from datetime import date
import calendar
import tweet
import RPi.GPIO as GPIO
import time
from picamera import PiCamera, Color
#message ="2016 FLL Razorback"
#message = "                                                          \
#We visited 2016 FLL Razorback          \
#447: It's All Geek to Me's pit"
message = "               2016 FLL Razorback              \
447: It's All Geek to Me's pit"


GPIO.setmode(GPIO.BCM)

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)

camera = PiCamera()
camera.resolution = (800, 480)
camera.start_preview()
camera.annotate_text = str(message)
twitter = tweet.Twitter();
dayStr = calendar.day_name[date.today().weekday()]
numVisitor = 1
tweetStr =  dayStr + " Visitor " 
#hashtags = " #photobooth #fll @fllrazorbackinv"
hashtags =" #photobooth #fll"
try:
    while True: 
        input_state = GPIO.input(21);
        while input_state == True:
            input_state = GPIO.input(21);

        camera.annotate_text = ""
        camera.annotate_text_size = 160
        for x in range(1, 4):
            camera.annotate_text = str(4 - x)
            time.sleep(1)

        camera.annotate_text_size = 32
        camera.annotate_text = str(message)
        filename = '/home/pi/Projects/capture' + str(numVisitor) + dayStr + '.jpg'
        time.sleep(0.1)
        camera.capture(filename, use_video_port = True)
        camera.stop_preview()
        camera.start_preview() 
        twitter.tweet(tweetStr + str(numVisitor) + hashtags, 36.068880, -94.175885, filename)
        numVisitor = numVisitor + 1
#Ctrl C
except KeyboardInterrupt:
    print "User cancelled"
    
#Error
except:
   print "Unexpected error:", sys.exc_info()[0]
   raise

finally:
   camera.stop_preview()

