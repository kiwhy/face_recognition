import face_recognition
import cv2
from flask import Flask, render_template, Response

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)

@app.route('/')
def index():
    "video streaming"
    return render_template('index.html')

def cap():
    while True:
        ret, img = video_capture.read()
        if ret == True:
            face_locations = face_recognition.face_locations(img)

            for face_location in face_locations:
                top, right, bottom, left = face_location

                img = cv2.rectangle(img, (left, top), (right, bottom), (255, 0, 0), 2)

            ret, img = cv2.imencode('.jpg', img)
            img = img.tobytes()

        yield (b'--frame\r\n'
               b'content-type: image/jpg\r\n\r\n' + img + b'\r\n')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    return Response(cap(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ =='__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)