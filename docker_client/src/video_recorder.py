import cv2
import time
class VideoRecorder:
    #def __init__(self):

    def record(self, name):
        # The duration in seconds of the video captured
        time.sleep(2) #wait 2 sec
        capture_duration = 10

        # Create a VideoCapture object
        cap = cv2.VideoCapture(0)
            
        # Check if camera opened successfully
        if (cap.isOpened() == False): 
            print("Unable to read camera feed")
            
        # Default resolutions of the frame are obtained.The default resolutions are system dependent.
        # We convert the resolutions from float to integer.
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))
            
        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
        out = cv2.VideoWriter(name,cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame_width,frame_height))

        start_time = time.time() 
        while( int(time.time() - start_time) < capture_duration ):
            ret, frame = cap.read()
            if ret == True: 
                    
                # Write the frame into the file 'output.avi'
                out.write(frame)
                
                # Display the resulting frame    
                cv2.imshow('frame',frame)
                
                # Press Q on keyboard to stop recording
                #if cv2.waitKey(1) & 0xFF == ord('q'):
                #    break
            # Break the loop
            else:
                break 
            
        # When everything done, release the video capture and video write objects
        cap.release()
        out.release()
            
        # Closes all the frames
        cv2.destroyAllWindows() 
