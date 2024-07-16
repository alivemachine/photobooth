import cv2
import os
import numpy as np
from pygrabber.dshow_graph import FilterGraph
from datetime import datetime
import pygame  # Import pygame for sound handling

# Initialize pygame mixer
pygame.mixer.init()

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Load your sound file
camera_switch_sound_path = resource_path('photo.wav')  
camera_switch_sound = pygame.mixer.Sound(camera_switch_sound_path)

def play_sound(sound):
    """ Play the given sound """
    sound.play()

camera_index = 0
min_neighbors = 5

def list_cameras():
    graph = FilterGraph()
    devices = graph.get_input_devices()
    return [(i, name) for i, name in enumerate(devices)]

# Initialize the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Directory to save images
save_dir = 'saved_images'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# Function to set the maximum resolution
def set_max_resolution(cap):
    # List of common resolutions (width, height)
    resolutions = [
        (1920, 1080), (1280, 720), (1024, 768), (800, 600), (640, 480), (320, 240)
    ]
    
    for width, height in resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if cap.get(cv2.CAP_PROP_FRAME_WIDTH) == width and cap.get(cv2.CAP_PROP_FRAME_HEIGHT) == height:
            print(f"Resolution set to {width}x{height}")
            break

def create_menu_window():
    global min_neighbors
    devices = list_cameras()
    menu_window = np.zeros((500, 600, 3), dtype=np.uint8)
    cv2.putText(menu_window, 'Select Camera:', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    y_offset = 100
    for i, (_, device_name) in enumerate(devices):
        cv2.putText(menu_window, f'{i}: {device_name}', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y_offset += 30
    cv2.putText(menu_window, 'Press Enter to confirm', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    y_offset += 50
    cv2.putText(menu_window, f'sensitivity: {min_neighbors}', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.putText(menu_window, 'Use +/- to adjust', (50, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    cv2.imshow('Menu', menu_window)

    global camera_index
    
    while True:
        key = cv2.waitKey(1)
        if key == 27:  # Escape key
            break
        elif key == 13:  # Enter key
            cv2.destroyWindow('Menu')
            return devices[camera_index][0]  # Return the device ID
        elif ord('0') <= key <= ord('9'):
            camera_index = min(len(devices) - 1, max(0, key - ord('0')))
        elif key == ord('+'):
            min_neighbors += 1
        elif key == ord('-'):
            min_neighbors = max(1, min_neighbors - 1)

        # Update menu window
        menu_window.fill(0)
        cv2.putText(menu_window, 'Select Camera:', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        y_offset = 100
        for i, (_, device_name) in enumerate(devices):
            color = (0, 255, 0) if i == camera_index else (255, 255, 255)
            cv2.putText(menu_window, f'{i}: {device_name}', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 1)
            y_offset += 30
        y_offset += 50
        cv2.putText(menu_window, f'sensitivity: {min_neighbors}', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        cv2.putText(menu_window, 'Use +/- to adjust (0:fast, 20:slow)', (50, y_offset + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        y_offset += 100
        cv2.putText(menu_window, 'Press Enter to confirm', (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        cv2.imshow('Menu', menu_window)

create_menu_window()
print(f"Opening camera {camera_index} with minNeighbors={min_neighbors}")

# Initialize the video capture
cap = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

# Set the maximum resolution
set_max_resolution(cap)

# Track the last time an image was saved
last_saved_time = datetime.now()

# Create a named window and set it to full screen
cv2.namedWindow('Webcam Feed', cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty('Webcam Feed', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

# Get screen dimensions
screen_width = cv2.getWindowImageRect('Webcam Feed')[2]
screen_height = cv2.getWindowImageRect('Webcam Feed')[3]

def switch_camera():
    global current_index
    global cap
    max_channels = 20
    start_index = current_index

    def attempt_switch(i):
        global cap
        if cap.isOpened():
            cap.release()
        
        cap = cv2.VideoCapture(i)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                current_index = i
                set_max_resolution(cap)
                print(f"Successfully switched to camera {i}")
                return i
            else:
                print(f"Failed to read frame from camera {i}")
        else:
            print(f"Failed to open camera {i}")
        return None

    # First, iterate from start_index to max_channels
    for i in range(start_index + 1, max_channels):
        print(f"Attempting to switch to camera {i}")
        if attempt_switch(i) is not None:
            return i

    # If no working camera found, iterate from 0 to start_index
    for i in range(0, start_index):
        print(f"Attempting to switch to camera {i}")
        if attempt_switch(i) is not None:
            return i

    print("No working camera found within 20 channels")
    return -1

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("No frame captured, attempting to switch camera.")
    else:
        # Create a white frame to illuminate the room
        white_frame = 255 * np.ones_like(frame, dtype=np.uint8)
        # Convert the frame to grayscale (required for face detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=min_neighbors, minSize=(30, 30))

        # Save the whole frame if at least one second has passed since the last save
        current_time = datetime.now()
        if (current_time - last_saved_time).total_seconds() >= 1 and len(faces) > 0:
            cv2.imshow('Webcam Feed', white_frame)
            cv2.waitKey(100)
            # Save the image
            timestamp = current_time.strftime('%Y%m%d_%H%M%S_%f')
            cv2.imwrite(os.path.join(save_dir, f'image_{timestamp}.png'), frame)
            play_sound(camera_switch_sound) 
            last_saved_time = current_time
            cv2.waitKey(100)  # Display the white frame for 100 milliseconds

        # Resize the frame to fit inside the screen while maintaining aspect ratio
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height

        if screen_width / screen_height > aspect_ratio:
            new_height = screen_height
            new_width = int(aspect_ratio * new_height)
        else:
            new_width = screen_width
            new_height = int(new_width / aspect_ratio)

        resized_frame = cv2.resize(frame, (new_width, new_height))

        # Create a black background to fit the resized frame
        background = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
        y_offset = (screen_height - new_height) // 2
        x_offset = (screen_width - new_width) // 2
        background[y_offset:y_offset+new_height, x_offset:x_offset+new_width] = resized_frame

        cv2.imshow('Webcam Feed', background)

        # Break the loop if 'q' or 'Escape' is pressed
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:  # 27 is the Escape key
            break
        elif key == ord('c'):
            switch_camera()

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
