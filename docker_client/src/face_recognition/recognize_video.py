# USAGE
# detect the personnes on the video and output the model guess 
#  best_id_count = the personne that the model predicted the most
#  best_id_moy  = the best average of all the resemblance % de model predicted

# import the necessary packages
from .pyimagesearch.centroidtracker import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import imutils
import pickle
import time
import cv2
import os
import operator
import pathlib

#extract the most likely person on the video
def return_best_id(dic) :
	maxi = []
	for key, value in dic.items():
		max_value = max(value.items(), key=operator.itemgetter(1))
		maxi.append([key, max_value])
	return maxi

def recognize_video(video_input = 1) :
	# construct the argument parser and parse the arguments
	path = str(pathlib.Path(__file__).parent.absolute())
	args = {"protoPath" : path +"/face_detection_model/deploy.prototxt","modelPath" : path+r"/face_detection_model/res10_300x300_ssd_iter_140000.caffemodel", "embedding_model" : path+r"/openface_nn4.small2.v1.t7" , "recognizer" : path+r"/output/recognizer.pickle", "le" : path+r"/output/le.pickle", "confidence" : 0.5}
	
	# initialize our centroid tracker and frame dimensions
	ct = CentroidTracker()

	# load our serialized face detector from disk
	detector = cv2.dnn.readNetFromCaffe(args["protoPath"], args["modelPath"])

	# load our serialized face embedding model from disk
	embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open(args["recognizer"], "rb").read())
	le = pickle.loads(open(args["le"], "rb").read())

	cap = cv2.VideoCapture(video_input)
	# all info extracted from video
	best_id_count = {}
	best_id_moy = {}
	
	# loop over frames from the video file stream
	while True:
		# grab the frame from the video data send to me
		_, frame = cap.read()

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		try:
			frame = imutils.resize(frame, width=600)
		#this most likely means that the video is finish 
		except AttributeError:	
			return  return_best_id(best_id_count) , return_best_id(best_id_moy)
		(h, w) = frame.shape[:2]
		# construct a blob from the image
		imageBlob = cv2.dnn.blobFromImage(
			cv2.resize(frame, (300, 300)), 1.0, (300, 300),
			(104.0, 177.0, 123.0), swapRB=False, crop=False)

		# apply OpenCV's deep learning-based face detector to localize
		# faces in the input image
		detector.setInput(imageBlob)
		detections = detector.forward()
		rects = []

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections
			if confidence > args["confidence"]:
				# compute the (x, y)-coordinates of the bounding box for
				# the face
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				"""just added"""
				rects.append(box.astype("int"))

				(startX, startY, endX, endY) = box.astype("int")

				# extract the face ROI
				face = frame[startY:endY, startX:endX]
				(fH, fW) = face.shape[:2]
				
				"""just added""" 
				objects = ct.update(rects)

				# loop over the tracked objects
				for (objectID, centroid) in objects.items():

					# construct a blob for the face ROI, then pass the blob
					# through our face embedding model to obtain the 128-d
					# quantification of the face
					faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
						(96, 96), (0, 0, 0), swapRB=True, crop=False)
					embedder.setInput(faceBlob)
					vec = embedder.forward()

					# perform classification to recognize the face
					preds = recognizer.predict_proba(vec)[0]
					j = np.argmax(preds)
					proba = preds[j]
					name = le.classes_[j]

					#take the proba of all the faces
					formatted_preds = [ '%.3f' % elem for elem in preds ]
					all_preds = dict(zip(le.classes_, formatted_preds))
					
					try :
						best_id_count[objectID][name] = best_id_count[objectID][name] + 1
					except KeyError:
						try:
							best_id_count[objectID][name] = 1
						except KeyError :
							best_id_count[objectID] = {}
							best_id_count[objectID][name] = 1
					if objectID in best_id_moy:
						best_id_moy[objectID] = {k:  round((float(best_id_moy[objectID][k]) * (sum(best_id_count[objectID].values())-1) + float(all_preds[k]))/sum(best_id_count[objectID].values()),3) for k in all_preds}
					else :
						best_id_moy[objectID] = all_preds

if __name__ == "__main__":
	path = str(pathlib.Path(__file__).parent.absolute())
	best_id_count, best_id_moy = recognize_video(video_input = path + r"\images\video_matthew.mp4")
	print(best_id_count, best_id_moy)