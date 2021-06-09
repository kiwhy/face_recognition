import cv2
import numpy as np
import numpy
from flask import Flask, render_template, Response

app = Flask(__name__)
video_capture = cv2.VideoCapture(0)
modelFile = "models/res10_300x300_ssd_iter_140000.caffemodel"
configFile = "models/deploy.prototxt.txt"
net = cv2.dnn.readNetFromCaffe(configFile, modelFile)

@app.route('/')
def index():
    "video streaming"
    return render_template('index.html')

def cap():
    while True:
        ret, img = video_capture.read()
        if ret == True:
            img = cv2.resize(img, None, fx=0.5, fy=0.5)
            h, w = img.shape[:2]
            blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)),
                                         1.0, (300, 300), (104.0, 117.0, 123.0))
            net.setInput(blob)
            net.setInput(blob)
            faces = net.forward()
            # to draw faces on image
            for i in range(faces.shape[2]):
                confidence = faces[0, 0, i, 2]
                if confidence > 0.5:
                    box = faces[0, 0, i, 3:7] * np.array([w, h, w, h])
                    (x, y, x1, y1) = box.astype("int")
                    cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)

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