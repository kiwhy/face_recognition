from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2
from mdsaver import EventWriter

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="path to the video file")
ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
ap.add_argument("-f", "--fps", type=int, default=20, help="FPS of output video")
ap.add_argument("-c", "--codec", type=str, default="DIVX", help="codec of output video")
ap.add_argument("-b", "--buffer-size", type=int, default=32, help="buffer size of video")
ap.add_argument("-o", "--output", required=True, help="path to output directory")
args = vars(ap.parse_args())

if args.get("video", None) is None:
    vs = VideoStream(0).start()
    time.sleep(2.0)

firstFrame = None

kcw = EventWriter(bufSize=args["buffer_size"])
consecFrames = 0

start = time.time()

while True:
    frame_saved = vs.read()
    frame = frame_saved
    frame = frame if args.get("video", None) is None else frame[1]
    text = "Unoccupied"

    if frame is None:
        break

    frame = imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if firstFrame is None:
        firstFrame = gray.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray, firstFrame, 0.01)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(firstFrame))

    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    for c in cnts:
        if cv2.contourArea(c) < args["min_area"]:
            continue

        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        text = "Occupied"

    cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] -10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)



    # if (time.time() - start >= 600):
    #     now = datetime.datetime.now().strftime("%y???%m???%d???%H???%M???-%S???")
    #     out = cv2.VideoWriter(now + ".avi", cv2.VideoWriter_fourcc(*'DIVX'), 60, (640, 480))
    #     start = time.time()

    if text != "Unoccupied":
        if not kcw.recording:
            timestamp = datetime.datetime.now()
            p="{}/{}.avi".format(args["output"], timestamp.strftime("%Y%m%d-%H%M%S"))
            kcw.start(p, cv2.VideoWriter_fourcc(*args["codec"]), args["fps"])
        consecFrames += 1
    kcw.update(frame)

    if text == "Occupied":
        kcw.finish()

    cv2.imshow("Security Feed", frame)
    cv2.imshow("Thresh", thresh)
    cv2.imshow("Frame Delta", frameDelta)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

vs.stop() if args.get("video", None) is None else vs.release()
cv2.destroyAllWindows()