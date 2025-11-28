from flask import Flask, render_template, jsonify, request, Response
from ultralytics import YOLO
import cv2
import threading
import os
from datetime import datetime
import base64
import winsound  # For Windows beep sound

app = Flask(__name__)

class CCTVApp:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        self.model_path = os.path.join('.', 'runs', 'detect', 'train4', 'weights', 'best.pt')
        self.model = YOLO(self.model_path)
        self.threshold = 0.3
        self.HIDE_FACE_CLASS_ID = 1
        
        self.recording = False
        self.out = None
        self.frame = None
        self.bareface_detected = False

    def play_beep(self):
        # Beep when bareface detected
        winsound.Beep(1000, 500)  # 1000 Hz, 500ms duration

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        frame = cv2.flip(frame, 1)
        results = self.model(frame)[0]
        self.bareface_detected = False
        
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > self.threshold:
                label = f"{results.names[int(class_id)].upper()} {score:.2f}"
                color = (0, 255, 0)
                if int(class_id) == self.HIDE_FACE_CLASS_ID:
                    color = (0, 0, 255)
                    self.bareface_detected = True
                    self.play_beep()  # Beep when bareface detected
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, color, 3)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        self.frame = frame
        return frame

    def encode_frame(self):
        if self.frame is None:
            return None
        _, buffer = cv2.imencode('.jpg', self.frame)
        return base64.b64encode(buffer).decode()

cctv = CCTVApp()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            frame = cctv.get_frame()
            if frame is None:
                continue
            encoded = cctv.encode_frame()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + 
                   base64.b64decode(encoded) + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_recording', methods=['POST'])
def start_recording():
    cctv.recording = True
    return jsonify({'status': 'Recording started'})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    cctv.recording = False
    return jsonify({'status': 'Recording stopped'})

@app.route('/sos_alert', methods=['POST'])
def sos_alert():
    threading.Thread(target=cctv.play_beep).start()  # Play beep sound in a separate thread
    return jsonify({'status': 'SOS alert triggered'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)