import cv2
import sys
import os.path
# Get user supplied values

# Create the haar cascade
path = os.path.join('face_detect', 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(os.path.join(path))


def find_faces(img, scale_factor, min_neighbors):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if face_cascade.empty():
        print "cascade is empty!!!"

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=scale_factor,
        minNeighbors=min_neighbors,
        minSize=(200, 200),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )

    if len(faces) > 0:
        print "Found {0} faces!".format(len(faces))

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

        cv2.imshow("Faces found", img)
        cv2.waitKey(100)

    else:
        cv2.imshow("Faces found", img)
        cv2.waitKey(5)

    return faces

if __name__ == '__main__':
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    find_faces(cv2.imread('abba.png'), 1.05, 3)

