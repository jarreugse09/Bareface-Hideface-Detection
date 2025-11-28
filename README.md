# AI-SEE: Real-Time Hide-Face Detection

A real-time, in-browser application that uses a custom-trained YOLOv8 model to detect individuals who are not wearing face masks correctly ("hide-face"). The application streams video from a webcam, performs object detection, and highlights detections in the browser with a modern, user-friendly interface.

## ✨ Features

- **Real-Time Detection:** Utilizes YOLOv8 to perform high-speed object detection directly on the video stream.
- **Web-Based UI:** A clean and modern user interface built with HTML, CSS, and JavaScript, served by a Flask backend.
- **Dark/Light Mode:** Includes a theme toggler for user preference.
- **Recording Controls:** Allows users to start and stop video recording (backend functionality).
- **SOS Alert:** A dedicated button to trigger an alert.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Machine Learning:** PyTorch, Ultralytics YOLOv8
- **Frontend:** HTML5, CSS3, JavaScript
- **Annotation Tool:** [MakeSense.ai](https://www.makesense.ai/)

## ⚙️ Installation

To set up and run this project locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
2. Set up a Python virtual environment:

For Windows:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```
For macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
```
3. Install dependencies:
```
pip install flask ultralytics opencv-python
🚀 Usage
```
4. Run the Flask application:
```
python app.py
```
Open the application:
Open your web browser and navigate to http://localhost:5000. The application should start automatically, accessing your webcam feed.
