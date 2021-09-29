import recording
from recording import app
from flask import render_template,Response,redirect,url_for,request,flash
import cv2
import time

global term
term=True


def video_frames():
    camera=cv2.VideoCapture(0)
    frame_width = int(camera.get(3))
    frame_height = int(camera.get(4))
    size = (frame_width, frame_height)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    name = "C://Users//riya//Desktop//tutorial//project//recordingapp//recordedvideo//video.avi"
    result = cv2.VideoWriter(name,fourcc, 10,size)
    
    starttime=time.time()
    while int(time.time() - starttime) < 35:
        success,frame=camera.read()
        if not success:
            break
        else:
            result.write(frame)
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()

        yield(b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()
    result.release()
    cv2.destroyAllWindows()
    
@app.route('/')
def index():
    return render_template('index.html',check=term)

@app.route('/<check>/start')
def start(check):
    send=''
    if check=='start':
        term=False
    return render_template('index.html',check=term,txt=send)

@app.route('/video')
def record():
    return Response(video_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')