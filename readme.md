# Photobooth

This is a simple touchless photobooth app for Windows. 

It uses Python and OpenCV. It displays a webcam feed and saves images at 1fps when faces are detected. You can let it run anywhere at an event and nobody has to touch it, it will capture people passing by.

## Features

![](Screenshot%202024-07-15%20231906.png?raw=true)

- keyboard input to select the webcam feed
- auto-selected highest resolution 
- touchless photo capture from face detection
- maximum capture rate of 1 frame per second
- audio/visual feedback
- custom sensitivity setting for the capture frequency
- no install, one click executable
- free and open-source

## Installation

Clone the repository:
```
git clone https://github.com/alivemachine/photobooth
cd photobooth
```

## Usage

Run the photobooth application:
```sh
python photobooth.py
```

## Build

[Download the .exe here.](https://drive.google.com/file/d/1b2whv1LhDmlmkEVGTnO1spwc0Aavyu2q/view?usp=drive_link)

To build the project into a standalone executable, use pyinstaller:
```
pyinstaller --onefile --clean --add-data "C:/Users/grego/miniconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml;cv2/data" --hidden-import=pyimod02_importers --hidden-import=pep517 --hidden-import=pygame.fastevent --hidden-import=pygame.overlay --hidden-import=pygrabber.dshow_graph --hidden-import=comtypes.stream --add-data "photo.wav;." photobooth.py
```



## License
This project is licensed under the MIT License. See the LICENSE file for details.

```