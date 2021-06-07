import face_recognition
import cv2
import numpy as np
import os
import io
from flask import Flask, render_template, Response

app = Flask(__name__)
video_capture = cv2.VideoCapture(0, cv2.CAP_V4L2)

known_face_names = []
known_face_encodings = []

dirname = 'knowns'
files = os.listdir(dirname)
for filename in files:
    Name, ext = os.path.splitext(filename)
    if ext == '.jpg':
        known_face_names.append(Name)
        pathname = os.path.join(dirname, filename)
        img = face_recognition.load_image_file(pathname)
        known_face_encoding = face_recognition.face_encodings(img)[0]
        known_face_encodings.append(known_face_encoding)

face_locations = []
face_encodings = []
face_names = []

@app.route('/')
def index():
    "video streaming"
    return render_template('index.html')

def gen():
    while True:
        process_this_frame = True
        ret, frame = video_capture.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = small_frame[:, :, ::-1]

        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]

                face_names.append(name)

        process_this_frame = not process_this_frame

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        ret, frame = cv2.imencode('.jpg', frame)
        frame = io.BytesIO(frame)

        yield (b'--frame\r\n'
               b'content-type: image/jpg\r\n\r\n' + frame.read() + b'\r\n')

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video_capture.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)