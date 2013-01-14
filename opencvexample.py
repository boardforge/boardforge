## run canny edge detection algorithm
import cv

# setup webcam
capture = cv.CaptureFromCAM(0)

# setup file output
filenm = "output.avi"
codec = 0
fps = 15
width = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH))
height = int(cv.GetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT))
writer = cv.CreateVideoWriter(filenm, codec, fps, (width,height), 1)

count = 0
delay = 100
while count < 30:
	# capture frame from webcam
	rawimage = cv.QueryFrame(capture)
	
	# display frame on screen
	cv.ShowImage('Image_Window',rawimage)
	cv.WriteFrame(writer, rawimage)
	cv.WaitKey(delay)
	
	# convert frame to greyscale
	depth = 8
	channels = 1
	greyscaleimage = cv.CreateImage((width,height),depth,channels)
	cv.CvtColor(rawimage,greyscaleimage,cv.CV_BGR2GRAY)
	
	# display frame on screen
	cv.ShowImage('Image_Window',greyscaleimage)
	cv.WriteFrame(writer, greyscaleimage)	
	cv.WaitKey(delay)	
	
	# perform canny edge detection on frame
	depth = 8
	channels = 1
	lowerthreshold = 10
	upperthreshold = 100
	aperture = 3
	edgeimage = cv.CreateImage((width,height),depth,channels)
	cv.Canny(greyscaleimage,edgeimage,lowerthreshold,upperthreshold,aperture)
	
	# display frame on screen & write frame to file
	cv.ShowImage('Image_Window',edgeimage)
	cv.WriteFrame(writer, edgeimage)
	cv.WaitKey(delay)
	
	count+=1