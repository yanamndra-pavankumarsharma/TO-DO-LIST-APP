from flask import Flask, render_template, Response
import cv2

# Initialize the Flask application
app = Flask(__name__)

# Open a connection to the webcam (camera 0 by default)
camera = cv2.VideoCapture(0)

# This function generates the frames from the webcam feed
def cctv_live():
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()
        
        # Check if the frame was captured successfully
        if not success:
            break
        else:
            # Encode the frame as a JPEG image
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            # Yield the frame in byte format with proper headers
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define the index route which renders the HTML template
@app.route('/')
def index():
    # Render the index.html page, which you should have in the templates folder
    return render_template('index.html')

# Define the video route that returns the webcam feed
@app.route('/video')
def video():
    # Use the Response object to send the generated video frames
    return Response(cctv_live(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Main entry point for the Flask app
if __name__ == "__main__":
    app.run(debug=True)

