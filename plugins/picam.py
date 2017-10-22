from picamera.array import PiRGBArray
from picamera import PiCamera
from IPlugin import IPlugin
from threading import Thread
import numpy as np
import os
import time

# since we do not want to assume the existence of OpenCV module, we import it optionally
global has_opencv
try:
    import cv2123
    has_opencv = True
except ImportError:
    print("OpenCV is missing, so motion detection cannot be used")
    has_opencv = False

class RPICamera(IPlugin):
    def __init__(self, config):
        width = int(config['width'])
        height = int(config['height'])
        framerate = int(config['framerate'])
        self.cam = PiCamera()
        self.cam.resolution = (width, height)
        self.cam.framerate = framerate
        # this member is used to stop the motion detection thread
        self.motiondet_thread_running = False

    def capture(self, filename):
        self.cam.capture(filename)

    def start_recording(self, filename):
        self.cam.start_recording(filename)

    def wait_recording(self, duration):
        self.cam.wait_recording(duration)

    def stop_recording(self):
        self.cam.stop_recording()

    def change_resolution(self, width, height):
        self.cam.resolution = (width, height)
        
    def start_motiondet_thread(self, bot, msg, restart_flag):
        t = Thread(target=self.detect_motion, args=(bot, msg,))
        if restart_flag == False:
            msg.reply_text("Start motion detection in:")
            for i in range(0,3):
                time.sleep(1) 
                msg.reply_text(3-i) 
        else:
            msg.reply_text("Restart motion detection!")
        time.sleep(1)
        msg.reply_text("NOW I GONNA KILL EVERYBODY!")
        self.motiondet_thread_running = True
        t.start()

    def stop_motiondet_thread(self, bot, msg):
        self.motiondet_thread_running = False
        time.sleep(1)

    def handlemessage(self, bot, msg):
        if msg.text.lower() == 'activate':
            if has_opencv:
                self.start_motiondet_thread(bot, msg, False)
            else:
                msg.reply_text("Without OpenCV you cannot ask for motion detection, loser!")
            return True
        if msg.text.lower() == 'deactivate':
            if self.motiondet_thread_running:
                self.stop_motiondet_thread(bot, msg)
            else:
                msg.reply_text("Hey, watcha doin'? Motion detection was not active, so I gonna do nothin'!")
            return True
        if msg.text.lower() == 'show me':
            # save current state as member motiondet_thread_running is overwritten in stop_motiondet_thread()
            running_before = self.motiondet_thread_running
            # stop motion detection thread to free needed camera resources
            self.stop_motiondet_thread(bot, msg)
            # change resolution to maximum (to guarantee largest field of view)
            self.change_resolution(2592, 1944)
            # take photo
            self.capture('/tmp/image.jpg')
            # send photo via Telegram messenger
            bot.sendPhoto(chat_id=msg.chat.id, photo=open('/tmp/image.jpg', 'rb'))
            # restart motion detection thread if it was running beforehand
            if running_before:
                self.start_motiondet_thread(bot, msg, running_before)
            return True
        elif msg.text.lower() == 'move it':
            # save current state as member motiondet_thread_running is overwritten in stop_motiondet_thread()
            running_before = self.motiondet_thread_running
            # stop motion detection thread to free needed camera resources
            self.stop_motiondet_thread(bot, msg)
            # record video in H.264 format
            os.system("rm /tmp/video.h264")
            self.change_resolution(1920, 1080)
            self.start_recording('/tmp/video.h264')
            self.wait_recording(5)
            self.stop_recording()
            # convert video to mp4 format that can be played by Telegram messenger and send it
            if os.path.isfile("/usr/bin/MP4Box"):
                os.system("MP4Box -new -fps " + str(self.cam.framerate) + " -add /tmp/video.h264 /tmp/video.mp4")
                bot.sendVideo(chat_id=msg.chat.id, video=open('/tmp/video.mp4', 'rb'))
            else:
                msg.reply_text("Can\'t send you the video, buddy. The goddamn video converter is missing!")
            # restart motion detection thread if it was running beforehand
            if running_before:
                self.start_motiondet_thread(bot, msg, running_before)
            return True
        return False
      
    def detect_motion(self, bot, msg):
        # set camera parameters
        self.cam.resolution = (1920,1080)
        self.cam.framerate = 10
        stream = PiRGBArray(self.cam, size=(self.cam.resolution.width, self.cam.resolution.height))
        time.sleep(1)
        
        # store images in a circular buffer
        image_buffer = []
        image_buffer_size = 30
        
        # set image resize factor to achieve real-time processing (factor 1 uses original image size)
        resize_factor = 2
        
        # set motion detection parameters
        motion_thresh = 20 # threshold in difference image
        min_component_size = 200 // pow(resize_factor, 2) # minimum connected component area size
        motion_alarm_thresh = self.cam.framerate # minimum consecutive images with motion detected to raise alarm (one second)
        motion_alarm_counter = 0 # consecutive images with motion detected
        motion_next_alarm_counter = 10 * self.cam.framerate  # we want to have one alarm every ten seconds at maximum

        # short-term background image that is used to calculate the difference image
        background = np.zeros((self.cam.resolution.height // resize_factor, self.cam.resolution.width // resize_factor, 1), dtype="uint8")
        
        # read frames
        for frame in self.cam.capture_continuous(stream, format="bgr", use_video_port=True):

            # add image to circular image buffer
            image_buffer.append(frame.array.copy())
            if len(image_buffer) > image_buffer_size:
                image_buffer.pop(0)
                
            # convert current image to gray values and resize it for real-time motion detection
            imageLarge = cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)
            image = cv2.resize(imageLarge, (self.cam.resolution.width // resize_factor, self.cam.resolution.height // resize_factor), interpolation = cv2.INTER_AREA)
            
            # initialize background with first image
            if len(image_buffer) == 1:
                background = image.copy()

            # detect motion as soon as image buffer is filled
            m,n = image.shape
            pointUL = (n, m) # we expect one moving object only...
            pointLR = (0, 0) # ...so we combine all detections to one motion region represented by upper left and lower right point
            found = False
            if (len(image_buffer) == image_buffer_size):
                diff_image = cv2.absdiff(image, background)
                ret, thresh_image = cv2.threshold(diff_image, motion_thresh, 255, cv2.THRESH_BINARY)
                contour_image, contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) > min_component_size:
                        found = True
                        x,y,w,h = cv2.boundingRect(contour)
                        pointUL = (min(pointUL[0], x), min(pointUL[1], y))
                        pointLR = (max(pointLR[0], x+w), max(pointLR[1], y+h))
       
            # react to detected motion, if necessary
            if found:
                # draw detected motion into last frame of image buffer
                # extend upper left and lower right point of rectangle to have better view towards the moving object
                pointLargeUL = (max(0, resize_factor*(pointUL[0]-2)), max(0, resize_factor*(pointUL[1]-2)))
                pointLargeLR = (min(self.cam.resolution.width-1, resize_factor*(pointLR[0]+2)), min(self.cam.resolution.height-1, resize_factor*(pointLR[1]+2)))
                # image_buffer[-1] refers to the last index in the array image_buffer
                cv2.rectangle(image_buffer[-1], pointLargeUL, pointLargeLR, (0,0,255), 4)
                        
                # increment motion alarm counter as we want to avoid alarm polling          
                motion_alarm_counter += 1
               
                # motion detected for sure? then notify user and send video!
                if motion_alarm_counter == motion_alarm_thresh:
                    # first, send alarm via message
                    msg.reply_text("Motion detected, dude!")
                    
                    # then write video from single images
                    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                    video = cv2.VideoWriter('/tmp/video.mp4', fourcc, self.cam.framerate, (self.cam.resolution.width, self.cam.resolution.height), True)
                    for img in image_buffer:
                        video.write(img)
                    video.release()
                    
                    # finally, send video to user via Telegram (this always throws a warning in the console, but it works anyway)
                    bot.sendVideo(chat_id=msg.chat.id, video=open('/tmp/video.mp4', 'rb'))          
            else:
                # reset motion alarm counter
                motion_alarm_counter = 0
            
            # update background using floating average (short-term background contains images from 20 frames)
            background = cv2.addWeighted(image, 0.05, background, 0.95, 0)
  
            # reset motion alarm counter after some time (ten seconds) to enable a new alarm
            if motion_alarm_counter == motion_next_alarm_counter:
                motion_alarm_counter = 0
        
            # clear stream for next incoming image
            stream.truncate(0)
            
            # stop thread if desired
            if self.motiondet_thread_running == False:
                break

        # close image window and thread
        cv2.destroyAllWindows()
        
        # give feedback to the user that motion detection is stopped
        msg.reply_text("Motion detection stopped!")


__export__ = RPICamera
