# USAGE
# python extract_embeddings.py --dataset dataset --embeddings output/embeddings.pickle \
#	--detector face_detection_model --embedding-model openface_nn4.small2.v1.t7

# import the necessary packages
from imutils import paths
import numpy as np
import imutils
import pickle
import cv2
import os
from data_aug_face import data_aug
import dlib
from imutils.face_utils import FaceAligner
import pathlib

def extract_embeddings() :
	# construct the argument parser and parse the arguments
	path = str(pathlib.Path(__file__).parent.absolute())
	args = {"shape_predictor" : path +r"\shape_predictor_68_face_landmarks.dat", "dataset" : path +r"\dataset\"", "embeddings" : path +r"\output\embeddings.pickle", "protoPath" : path +r"\face_detection_model\deploy.prototxt","modelPath" : path+r"\face_detection_model\res10_300x300_ssd_iter_140000.caffemodel", "embedding_model" : path +r"\openface_nn4.small2.v1.t7", "confidence" : 0.5}

	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	detector = cv2.dnn.readNetFromCaffe(args["protoPath"], args["modelPath"])

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])


	
	# initialize dlib's face detector (HOG-based) and then create
	# the facial landmark predictor and the face aligner
	predictor = dlib.shape_predictor(args["shape_predictor"])
	fa = FaceAligner(predictor, desiredFaceWidth=256)
	


	# grab the paths to the input images in our dataset
	print("[INFO] quantifying faces...")
	imagePaths = list(paths.list_images(args["dataset"][0:~1]))
	# initialize our lists of extracted facial embeddings and
	# corresponding people names
	knownEmbeddings = []
	knownNames = []

	
	# initialize the total number of faces processed
	total = 0
	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		print("[INFO] processing image {}/{}".format(i + 1,
			len(imagePaths)))
		name = imagePath.split(os.path.sep)[-2]

		# load the image, resize it to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		image = cv2.imread(imagePath)
		image = imutils.resize(image, width=600)
		(h, w) = image.shape[:2]

		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(image, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()

		# ensure at least one face was found
		if len(detections) > 0:
			# we're making the assumption that each image has only ONE
			# face, so find the bounding box with the largest probability
			i = np.argmax(detections[0, 0, :, 2])
			confidence = detections[0, 0, i, 2]

			# ensure that the detection with the largest probability also
			# means our minimum probability test (thus helping filter out
			# weak detections)
			if confidence > args["confidence"]:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI and grab the ROI dimensions
				face = image[startY:endY, startX:endX]
				"""
				#gray scale 
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				#data augmentation with only face 
				faceBoxRectangleS = dlib.rectangle(left=startX, top=startY, right=endX, bottom=endY)
				faceAligned = fa.align(image, gray, faceBoxRectangleS)
				cv2.imshow("facealigned", faceAligned)
				cv2.imshow("Original", face)
				#### redetect face 
				
				faceAligned = imutils.resize(faceAligned, width=300)
				(h, w) = faceAligned.shape[:2]
				imageBlob = cv2.dnn.blobFromImage(
				cv2.resize(faceAligned, (125, 125)), 1.0, (125, 125),
				(104.0, 177.0, 123.0), swapRB=False, crop=False)
				print(imageBlob)
				detector.setInput(imageBlob)
				detections = detector.forward()
				print(len(detections))
				i = np.argmax(detections[0, 0,:, 2])
				confidence = detections[0, 0, i, 2]
				print(confidence)
				print(detections[0, 0, i, 3:7])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")
				print((startX, startY, endX, endY))
				face_zoomed = faceAligned[startY:endY, startX:endX]
				cv2.imshow("face_zoomed", face_zoomed)
				####
				cv2.waitKey(0)
				"""
				
				face_aug = data_aug(face) 

				# construct a blob for the face ROI, then pass the blob
				# through our face embedding model to obtain the 128-d
				# quantification of the face
				for face in face_aug :
					faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
						(96, 96), (0, 0, 0), swapRB=True, crop=False)
					embedder.setInput(faceBlob)
					vec = embedder.forward()

					# add the name of the person + corresponding face
					# embedding to their respective lists
					knownNames.append(name)
					knownEmbeddings.append(vec.flatten())
				total += 1

	# dump the facial embeddings + names to disk
	print("[INFO] serializing {} encodings...".format(total))
	data = {"embeddings": knownEmbeddings, "names": knownNames}
	f = open(args["embeddings"], "wb")
	f.write(pickle.dumps(data))
	f.close()
if __name__ == "__main__":
	extract_embeddings()