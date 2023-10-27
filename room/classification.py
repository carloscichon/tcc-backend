import numpy as np
import cv2
from keras.models import model_from_json

def teste(img_string):
    nparr=np.fromstring(img_string, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    cv2.imwrite("teste_cv2.png", frame)
    return "ok"


def process_image(img_string):
    #print(img_string)
    emotion_dict = {0: "angry", 1: "contempt", 2: "disgust", 3: "fear", 4: "happy", 5: "neutral", 6: "sad", 7: "surprise"}
    
    # load json and create model
    json_file = open('affect_model_200.json', 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    emotion_model = model_from_json(loaded_model_json)

    # load weights into new model
    emotion_model.load_weights("affect_model_200.h5")
    
    #decode base64 image
    nparr = np.fromstring(img_string, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    #frame = cv2.resize(frame, (1280, 720))
 
    #face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces available on camera
    num_faces = face_detector.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)

    # take each face available on the camera and Preprocess it
    for (x, y, w, h) in num_faces:
        cv2.rectangle(frame, (x, y-50), (x+w, y+h+10), (0, 255, 0), 4)
        roi_gray_frame = gray_frame[y:y + h, x:x + w]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray_frame, (224, 224)), -1), 0)

        # predict the emotions
        emotion_prediction = emotion_model.predict(cropped_img)
        maxindex = int(np.argmax(emotion_prediction))
        print(maxindex)
        return emotion_dict[maxindex]