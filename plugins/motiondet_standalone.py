from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np


def main():
    circular_image_buffer = []
    circular_buffer_size = 10
    motion_thresh = 20
    kernel = np.ones((5,5), np.uint8)
    min_component_size = 200

    camera = PiCamera()
    camera.resolution = (1920,1080)
    camera.framerate = 10
    stream = PiRGBArray(camera, size=(1920,1080))
    time.sleep(1)

    # Read frames
    for frame in camera.capture_continuous(stream, format="bgr", use_video_port=True):

        # Original image
        image = cv2.cvtColor(frame.array, cv2.COLOR_RGB2GRAY)
      
        motion_areas = []
        if len(circular_image_buffer) > 5:
            background = np.median(circular_image_buffer, axis=0)
            #background = np.float32(circular_image_buffer[0])
            #for img in circular_image_buffer:
            #    cv2.accumulateWeighted(img, background, 0.1)
            backgroundScaled = cv2.convertScaleAbs(background)
            diff_image = cv2.absdiff(image, backgroundScaled)
            ret, thresh_image = cv2.threshold(diff_image, motion_thresh, 255, cv2.THRESH_BINARY)
            closing = cv2.morphologyEx(thresh_image, cv2.MORPH_CLOSE, kernel)
            opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
            #cv2.imshow('background', backgroundScaled)
            #cv2.imshow('motion image', opening)
            contour_image, contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if cv2.contourArea(contour) > min_component_size:
                    motion_areas.append(contour)
            
        
        # update circular image buffer
        circular_image_buffer.append(image)
        if len(circular_image_buffer) > circular_buffer_size:
            circular_image_buffer.pop(0)

        # react to detected motion, if necessary
        if len(motion_areas) > 0:
            print("motion detected")
         
        drawImage = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB) 
        #cv2.drawContours(drawImage, motion_areas, -1, (0, 0, 255), cv2.FILLED) 
        for motion_area in motion_areas:
            x,y,w,h = cv2.boundingRect(motion_area)
            cv2.rectangle(drawImage, (x,y), (x+w,y+h), (0,0,255), 2)

        # Show computed image
        cv2.imshow('current image',drawImage)
        
        stream.truncate(0)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    # Close image window and thread
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
