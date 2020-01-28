# USAGE
# python recognize_video.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle

"""
## modifier le code pour qu'il soient opti pour rasberry pi
Clean le code / opti 
+
	 if new user :
		 lance extract_embedding[openFace]/[facenet?] (add data aug ici après l'extraction du visage avec juste les  aug voulus) --> 
		 train_model.py [svm]
	 if new video : 
		 lance recognize_video ok
		 // add --> id moving object --> average all detection to give a better guess of the personne OK
		 //							 --> add new unknow face X to data set (to observe same X guy) 
		 /////// imposible :
		 // add emotion detection
		 // add body detection id to tell what they are doing

Problèmes :
- 2 personnes peuvent avoir le même id (si id 0 sort de la video et une autre personne rentre dans la video)
- comment dire qui c'est ? : 
	- prendre tout les % à chaque test, prendre la moyenne de chacun et conservé la meilleur moyenne OK
	- prendre celui qui à le plus souvent le meilleur % OK (mieux si je retourn le % de fois où il est reconnus)
	- comment je confirme que c'est bien lui ? 
		- test model avec nos têtes
		- test avec inconus 
		- model avec face alignement (+ re modifier le data augmentation)
		- je pref faux negatifs
	- comment gere les visages non blasé ? data aug distortion d'image ? (coupé haut / bas visage, flexibilité )
"""



# import the necessary packages
from pyimagesearch.centroidtracker import CentroidTracker
from imutils.video import VideoStream
from imutils.video import FPS
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

def recognize_video_test(video_input=1):
	# construct the argument parser and parse the arguments
	path = str(pathlib.Path(__file__).parent.absolute())
	args = {"protoPath" : path +r"\face_detection_model\deploy.prototxt","modelPath" : path+r"\face_detection_model\res10_300x300_ssd_iter_140000.caffemodel", "embedding_model" : path+r"\openface_nn4.small2.v1.t7" , "recognizer" : path+r"\output\recognizer.pickle", "le" : path+r"\output\le.pickle", "confidence" : 0.5}
	
	# initialize our centroid tracker and frame dimensions
	ct = CentroidTracker()

	# load our serialized face detector from disk
	print("[INFO] loading face detector...")
	#protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
	#modelPath = os.path.sep.join([args["detector"],"res10_300x300_ssd_iter_140000.caffemodel"])
	detector = cv2.dnn.readNetFromCaffe(args["protoPath"], args["modelPath"])

	# load our serialized face embedding model from disk
	print("[INFO] loading face recognizer...")
	embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

	# load the actual face recognition model along with the label encoder
	recognizer = pickle.loads(open(args["recognizer"], "rb").read())
	le = pickle.loads(open(args["le"], "rb").read())

	if video_input == 1 :
		# initialize the video stream, then allow the camera sensor to warm up
		print("[INFO] starting video stream...")
		vs = VideoStream(src=0).start()
		time.sleep(2.0)
		best_id_count = {}
		best_id_moy = {}

	else  :
		cap = cv2.VideoCapture(video_input)
		# all info extracted from video
		best_id_count = {}
		best_id_moy = {}

	# start the FPS throughput estimator
	fps = FPS().start()
	
	# loop over frames from the video file stream
	while True:
		if video_input == 1 :
			# grab the frame from the threaded video stream
			frame = vs.read()

		else :
			# grab the frame from the video data send to me
			_, frame = cap.read()

		# resize the frame to have a width of 600 pixels (while
		# maintaining the aspect ratio), and then grab the image
		# dimensions
		try:
			frame = imutils.resize(frame, width=600)
		#this most likely means that the video is finish 
		except AttributeError:	
			return  best_id_count , best_id_moy

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
				# ensure the face width and height are sufficiently large
				if fW < 20 or fH < 20:
					continue

				for (objectID, centroid) in objects.items():
					this_centroid = np.array([int(abs(startX - endX) / 2 + startX), int(abs(startY - endY) / 2 + startY)])
					if centroid[0] == this_centroid[0] and centroid[1] == this_centroid[1]:
						test = objectID
					else:
						continue
						

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
				#best recognize
				proba = preds[j]
				name = le.classes_[j]

				#take the proba of all the faces
				formatted_preds = [ '%.3f' % elem for elem in preds ]
				all_preds = dict(zip(le.classes_, formatted_preds))
				
				# draw the bounding box of the face along with the
				# associated probability
				text = "{}: {:.2f}%".format(name, proba * 100)
				y = startY - 10 if startY - 10 > 10 else startY + 10
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					(0, 0, 255), 2)
				cv2.putText(frame, text, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)


				try :
					best_id_count[test][name] = best_id_count[test][name] + 1
				except KeyError:
					try:	
						best_id_count[test][name] = 1
						#print('first time name',_id)
					except KeyError:
						best_id_count[test] = {}
						best_id_count[test][name] = 1
						#print('first time see this id',_id)
				if test in best_id_moy:
					#print('moy',_id)
					best_id_moy[test] = {k:  round((float(best_id_moy[test][k]) * (sum(best_id_count[test].values())-1) + float(all_preds[k]))/sum(best_id_count[test].values()),3) for k in all_preds}
				else:
					#print('first time moy',_id)
					best_id_moy[test] = all_preds



		# loop over the tracked objects
			for (objectID, centroid) in objects.items():
				# draw both the ID of the object and the centroid of the
				# object on the output frame
				text = "ID {}".format(objectID)
				cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
				cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)
					

		# update the FPS counter
		fps.update()

		# send notification
		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			return return_best_id(best_id_count) , return_best_id(best_id_moy)
			break

	if video_input == 1 :
		# stop the timer and display FPS information
		fps.stop()
		print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
		print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

		# do a bit of cleanup
		cv2.destroyAllWindows()
		vs.stop()

if __name__ == "__main__":
	#953
	best_id_count, best_id_moy = recognize_video_test(r"C:\Users\utilisateur\Desktop\xvkogaqmqz.avi")
	print(best_id_count, best_id_moy)


	