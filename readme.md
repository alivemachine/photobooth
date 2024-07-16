build with
```
pyinstaller --onefile --clean --add-data "C:/Users/grego/miniconda3/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml;cv2/data" --hidden-import=pyimod02_importers --hidden-import=pep517 --hidden-import=pygame.fastevent --hidden-import=pygame.overlay --hidden-import=pygrabber.dshow_graph --hidden-import=comtypes.stream --add-data "photo.wav;." photobooth.py
```

