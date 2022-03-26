import cv2
import os
from imutils import face_utils
import time
import cv2
from mtcnn_cv2 import MTCNN

def main(image_path,dest,name):

    detector = MTCNN()
    image=cv2.imread(image_path)


    gray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = detector.detect_faces(gray)
    print("shape",image.shape)
    if len(result) > 0:
        for i in range(len(result)):
            bounding_box = result[i]['box']
            print(bounding_box)
        
            cv2.rectangle(gray,
                        (bounding_box[0], bounding_box[1]),
                        (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
                        (0,155,255),
                        2)
            cv2.imwrite(os.path.join(dest,name),gray)

