import numpy as np

class FaceComparator:
    
    def face_distance(self, face_encodings, face_to_compare, tolerance = 60):
        """
        Given a list of face encodings, compare them to a known face encoding and get a euclidean distance
        for each comparison face. The distance tells you how similar the faces are.
        :param faces: List of face encodings to compare
        :param face_to_compare: A face encoding to compare against
        :return: A numpy ndarray with the distance for each face in the same order as the 'faces' array
        """
        if len(face_encodings) == 0:
            return np.empty((0))
        #print("tolerance:", tolerance)
        print("values :", np.linalg.norm(face_encodings - face_to_compare, axis=1) )
        return list(np.linalg.norm(face_encodings - face_to_compare, axis=1) <= tolerance)