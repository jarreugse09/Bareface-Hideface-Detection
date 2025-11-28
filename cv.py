import sys
import os
import cv2
import winsound  # For Windows beep sound (use alternative for other OS)
import threading
from ultralytics import YOLO
from PyQt5.QtCore import QTimer, QDateTime
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog
from PyQt5.QtGui import QImage, QPixmap

class CCTVApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CCTV - Hide-Face Detection")
        self.setGeometry(100, 100, 800, 600)

        # Initialize UI elements
        self.video_label = QLabel(self)
        self.video_label.resize(800, 450)

        self.time_label = QLabel(self)
        self.time_label.setText("Time: ")
        self.time_label.setStyleSheet("font-size: 18px;")

        self.start_button = QPushButton("Start Recording", self)
        self.start_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.video_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        # Initialize camera feed
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set frame width
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)  # Set frame height

        if not self.cap.isOpened():
            self.video_label.setText("Error: Could not open video capture.")
            return

        # Load the YOLO model
        self.model_path = os.path.join('.', 'runs', 'detect', 'train4', 'weights', 'best.pt')
        if not os.path.exists(self.model_path):
            self.video_label.setText(f"Error: Model file {self.model_path} does not exist.")
            self.cap.release()
            return

        self.model = YOLO(self.model_path)
        self.threshold = 0.3
        self.HIDE_FACE_CLASS_ID = 1  # Replace with your model's class ID for 'hide-face'

        # Timer for updating the video feed
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        self.recording = False
        self.out = None

    def play_beep(self):
        winsound.Beep(1000, 500)  # Frequency: 1000 Hz, Duration: 500 ms

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        # Flip the frame horizontally
        frame = cv2.flip(frame, 1)

        # Process frame for detection
        results = self.model(frame)[0]
        hide_face_detected = False

        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result
            if score > self.threshold:
                label = f"{results.names[int(class_id)].upper()} {score:.2f}"
                color = (0, 255, 0)

                if int(class_id) == self.HIDE_FACE_CLASS_ID:
                    hide_face_detected = True
                    color = (0, 0, 255)

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 4)
                cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX,
                            1.3, color, 3, cv2.LINE_AA)

        # Trigger beep if 'hide-face' is detected
        if hide_face_detected:
            threading.Thread(target=self.play_beep).start()

        # Add time overlay
        current_time = QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        cv2.putText(frame, current_time, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # Save the frame if recording
        if self.recording and self.out is not None:
            self.out.write(frame)

        # Convert frame to QImage for display
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.video_label.setPixmap(QPixmap.fromImage(qt_image))

        # Update time label
        self.time_label.setText(f"Time: {current_time}")

    def start_recording(self):
        import os
        from datetime import datetime

        default_dir = os.path.join(os.path.dirname(__file__), "recordings")
        os.makedirs(default_dir, exist_ok=True)
        default_name = datetime.now().strftime("record_%Y%m%d_%H%M%S.avi")
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Recording", os.path.join(default_dir, default_name), "Video Files (*.avi)")
        if save_path:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 20.0
            frame_size = (int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.out = cv2.VideoWriter(save_path, fourcc, fps, frame_size)
            self.recording = True
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)

    def stop_recording(self):
        self.recording = False
        if self.out is not None:
            self.out.release()
            self.out = None
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def closeEvent(self, event):
        self.cap.release()
        if self.out is not None:
            self.out.release()
        cv2.destroyAllWindows()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCTVApp()
    window.show()
    sys.exit(app.exec_())