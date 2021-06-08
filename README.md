# WinOCR
[![Python](https://img.shields.io/pypi/pyversions/winocr.svg?style=plastic)](https://badge.fury.io/py/winocr)
[![PyPI](https://badge.fury.io/py/winocr.svg)](https://badge.fury.io/py/winocr)

# Installation
```powershell
pip install winocr
```

# Usage
## Pillow
```python
import winocr
from PIL import Image

img = Image.open('test.jpg')
print((await winocr.recognize_pil(img, 'ja')).text)
```

## OpenCV
```python
import winocr
import cv2

img = cv2.imread('test.jpg')
print((await winocr.recognize_cv2(img, 'ja')).text)
```

## Web API
Run server
```powershell
winocr_serve
```

### curl
```bash
curl localhost:8000?lang=ja --data-binary @test.jpg
```

### Python
```python
import requests

bytes = open('test.jpg', 'rb').read()
requests.post('http://localhost:8000/?lang=ja', bytes).json()['text']
```

### JavaScript
```javascript
// File
const file = document.querySelector('[type=file]').files[0]
await fetch('http://localhost:8000/', {method: 'POST', body: file}).then(r => r.json())

// Blob
const blob = await fetch('https://image.itmedia.co.jp/ait/articles/1706/15/news015_16.jpg').then(r=>r.blob())
await fetch('http://localhost:8000/?lang=ja', {method: 'POST', body: blob}).then(r => r.json())
```
