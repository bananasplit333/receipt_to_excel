import cv2
import pytesseract
import base64
import imutils 
from imutils.perspective import four_point_transform
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from skimage.filters import threshold_local




def find_contour(edge):
	# find the contours in the edged image, keeping only the
	# largest ones, and initialize the screen contour
	cnts = cv2.findContours(edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if our approximated contour has four points, then we
		# can assume that we have found our screen
		if len(approx) == 4:
			return approx 
	return None 

def alt_transform(image):
	warped = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	# show the original and scanned images
	print("STEP 3: Apply perspective transform")
	#cv2.imshow("Original", imutils.resize(orig, height = 650))
	#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
	cv2.waitKey(0)
	# Encode the processed image to base64
	_, buffer = cv2.imencode('.jpg', warped)
	base64_image = base64.b64encode(buffer).decode('utf-8')
	print("returning img")
	return base64_image

def edge_detection(image):
	# convert the image to grayscale, blur it slightly, and then apply
	# edge detection
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
	edged = cv2.Canny(blurred, 75, 200)
	print("STEP 1: Edge Detection")
	#cv2.imshow("Image", image)
	#cv2.imshow("Edged", edged)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return edged

def edit_batch(url):
	print("processsing" , url)
	orig = cv2.imread(url)
	image = orig.copy()
	image = imutils.resize(image, width=500)
	ratio = orig.shape[1] / float(image.shape[1])

	edged = edge_detection(image)
	screenCnt = find_contour(edged)
	if screenCnt is None: 
		print("screen contour not found, alternative method inc")
		return alt_transform(image)
	# show the contour (outline) of the piece of paper
	print("STEP 2: Find contours of paper")
	cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
	#cv2.imshow("Outline", image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	# apply the four point transform to obtain a top-down
	# view of the original image
	warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
	# convert the warped image to grayscale, then threshold it
	# to give it that 'black and white' paper effect
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	T = threshold_local(warped, 11, offset = 10, method = "gaussian")
	warped = (warped > T).astype("uint8") * 255
	# show the original and scanned images
	print("STEP 3: Apply perspective transform")
	#cv2.imshow("Original", imutils.resize(orig, height = 650))
	#cv2.imshow("Scanned", imutils.resize(warped, height = 650))
	cv2.waitKey(0)
	# Encode the processed image to base64
	_, buffer = cv2.imencode('.jpg', warped)
	base64_image = base64.b64encode(buffer).decode('utf-8')
	print("returning img")
	#cv2.imshow("hi", warped)
	return base64_image

def encode64(url):
	with open(url, "rb") as image_file:
			return base64.b64encode(image_file.read()).decode('utf-8')