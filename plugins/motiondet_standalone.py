from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


def main():
    image_buffer = []
    image_buffer_size = 30
    motion_thresh = 20
    min_component_size = 200

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.framerate = 10
    stream = PiRGBArray(camera, size=(1920,1080))
    time.sleep(1)

    background = np.zeros((1080,1920,1), dtype="uint8")

    # Read frames
    for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):

        start = time.clock()

        # Original image
        image = cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)
        
        # add image to circular image buffer
        image_buffer.append(image)
        if len(image_buffer) > image_buffer_size:
            image_buffer.pop(0)

        motion_areas = []
        if (len(image_buffer) == image_buffer_size):
            diff_image = cv2.absdiff(image, background)
            ret, thresh_image = cv2.threshold(diff_image, motion_thresh, 255, cv2.THRESH_BINARY)
            #cv2.imshow('difference image', thresh_image)
            contour_image, contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > min_component_size:
                    motion_areas.append(contour)
       
        # react to detected motion, if necessary
        if len(motion_areas) > 0:
            print("motion detected")
            for motion_area in motion_areas:
                x,y,w,h = cv2.boundingRect(motion_area)
                cv2.rectangle(image, (x,y), (x+w,y+h), (0,0,255), 2)
            # replace image in circular image buffer
            #cv2.imshow('motion image', image)
            image_buffer[-1] = image
        else:
	    # update background using floating average
            background = cv2.addWeighted(image, 0.1, background, 0.9, 0)
            #cv2.imshow('background', background)
	  
        # use this if you want to visualize the found motion in color
        #drawImage = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB) 
        #cv2.drawContours(drawImage, motion_areas, -1, (0, 0, 255), cv2.FILLED) 
        #for motion_area in motion_areas:
        #    x,y,w,h = cv2.boundingRect(motion_area)
        #    cv2.rectangle(drawImage, (x,y), (x+w,y+h), (0,0,255), 2)

        # Show computed image
        #cv2.imshow('current image',drawImage)

        end = time.clock()
        print(end-start)
        
        stream.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Close image window and thread
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
