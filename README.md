# WinOCR
[![Python](https://img.shields.io/pypi/pyversions/winocr.svg)](https://badge.fury.io/py/winocr)
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
![](https://camo.qiitausercontent.com/63785b963fa5d67e9f2be1ac9e4953579f4c2584/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f33373061353463382d623536612d353362382d366632352d3634333363313630383866612e706e67)

## OpenCV

```python
import winocr
import cv2

img = cv2.imread('test.jpg')
print((await winocr.recognize_cv2(img, 'ja')).text)
```
![](https://camo.qiitausercontent.com/ad91376e61b0e32a243fdc92a4586e87c8f683ba/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f65383031336338362d613833322d393837632d353763382d3135383536356634313034322e706e67)

## Connect to local runtime on Colaboratory

![](https://i.imgur.com/gvj959U.png)

![](https://i.imgur.com/o9e0Fwk.png)

## Web API

Run server
```powershell
pip install winocr[api]
winocr_serve
```

### curl

```bash
curl localhost:8000?lang=ja --data-binary @test.jpg
```
![](https://camo.qiitausercontent.com/9dcb18830efe482d9bbb1c8a90d80205f71112ed/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f66643138343566632d653634372d306437662d353336652d3634653363303263633861312e706e67)

### Python

```python
import requests

bytes = open('test.jpg', 'rb').read()
requests.post('http://localhost:8000/?lang=ja', bytes).json()['text']
```

![](https://camo.qiitausercontent.com/04853be7fa2c389b3921ae4a098f1e41abab1a67/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f64373162333531362d326466652d616439312d626661352d6634376637623836633263632e706e67)

You can run OCR with the Colaboratory runtime with `./ngrok http 8000`

```python
from PIL import Image
from io import BytesIO

img = Image.open('test.jpg')
# Preprocessing
buf = BytesIO()
img.save(buf, format='JPEG')
requests.post('https://15a5fabf0d78.ngrok.io/?lang=ja', buf.getvalue()).json()['text']
```
![](https://camo.qiitausercontent.com/ee8498f92eef03632bb0d3abb26de1269970900c/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f33393064393539372d316435352d356431632d383532302d3135633461383131386464642e706e67)

```python
import cv2
import requests

img = cv2.imread('test.jpg')
# Preprocessing
requests.post('https://15a5fabf0d78.ngrok.io/?lang=ja', cv2.imencode('.jpg', img)[1].tobytes()).json()['text']
```
![](https://camo.qiitausercontent.com/e5f4e0bf0538b851ddd525879600a712a3ce978a/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f39613364613534612d363664362d396138322d373038662d6464343763323832313930302e706e67)

### JavaScript

If you only need to recognize Chrome and English, you can also consider the Text Detection API.

```javascript
// File
const file = document.querySelector('[type=file]').files[0]
await fetch('http://localhost:8000/', {method: 'POST', body: file}).then(r => r.json())

// Blob
const blob = await fetch('https://image.itmedia.co.jp/ait/articles/1706/15/news015_16.jpg').then(r=>r.blob())
await fetch('http://localhost:8000/?lang=ja', {method: 'POST', body: blob}).then(r => r.json())
```

It is also possible to run OCR Server on Windows Server.

# Information that can be obtained
You can get **angle**, **text**, **line**, **word**, **BoundingBox**.

```python
import pprint

result = await winocr.recognize_pil(img, 'ja')
pprint.pprint({
    'text_angle': result.text_angle,
    'text': result.text,
    'lines': [{
        'text': line.text,
        'words': [{
            'bounding_rect': {'x': word.bounding_rect.x, 'y': word.bounding_rect.y, 'width': word.bounding_rect.width, 'height': word.bounding_rect.height},
            'text': word.text
        } for word in line.words]
    } for line in result.lines]
})
```
![](https://camo.qiitausercontent.com/cea9240789734fc27486c62efec796b6397d7d35/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f63663534376231312d313038642d636335332d653863332d3136663337656432386163352e706e67)

# Language installation
```powershell
# Run as Administrator
Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"
Add-WindowsCapability -Online -Name "Language.OCR~~~ja-JP~0.0.1.0"

# Search for installed languages
Get-WindowsCapability -Online -Name "Language.OCR*"
# State: Not Present language is not installed, so please install it if necessary.
Name         : Language.OCR~~~hu-HU~0.0.1.0
State        : NotPresent
DisplayName  : ハンガリー語の光学式文字認識
Description  : ハンガリー語の光学式文字認識
DownloadSize : 194407
InstallSize  : 535714

Name         : Language.OCR~~~it-IT~0.0.1.0
State        : NotPresent
DisplayName  : イタリア語の光学式文字認識
Description  : イタリア語の光学式文字認識
DownloadSize : 159875
InstallSize  : 485922

Name         : Language.OCR~~~ja-JP~0.0.1.0
State        : Installed
DisplayName  : 日本語の光学式文字認識
Description  : 日本語の光学式文字認識
DownloadSize : 1524589
InstallSize  : 3398536

Name         : Language.OCR~~~ko-KR~0.0.1.0
State        : NotPresent
DisplayName  : 韓国語の光学式文字認識
Description  : 韓国語の光学式文字認識
DownloadSize : 3405683
InstallSize  : 7890408
```

If you hate Python and just want to recognize it with PowerShell, click [here](https://gist.github.com/GitHub30/8bc1e784148e4f9801520c7e7ba191ea)

# Multi-Processing

By processing in parallel, it is 3 times faster. You can make it even faster by increasing the number of cores!

```python
from PIL import Image

images = [Image.open('testocr.png') for i in range(1000)]
```

### 1 core(elapsed 48s)

The CPU is not used up.
![](https://camo.qiitausercontent.com/c9c991eb1473137866fb8693eb1d4bef7b6addfc/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f66613263326635322d396638362d643435322d643263372d6162336330653061663837642e706e67)

```python
import winocr

[(await winocr.recognize_pil(img)).text for img in images]
```
![](https://camo.qiitausercontent.com/5bab8b980fee37d662f73893df2a4c0b4b494dd1/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f65656536636332302d376663352d376462372d383464622d6361656165326465666139392e706e67)

### 4 cores(elapsed 16s)

I'm using 100% CPU.
![](https://camo.qiitausercontent.com/2722a602a190ac5e54df7164b9e3cf714cb48d42/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f37636565626631652d663232662d353065352d393635612d3430326666633738363435622e706e67)

Create a worker module.
```python
%%writefile worker.py
import winocr
import asyncio

async def ensure_coroutine(awaitable):
    return await awaitable

def recognize_pil_text(img):
    return asyncio.run(ensure_coroutine(winocr.recognize_pil(img))).text
```

```python
import worker
import concurrent.futures

with concurrent.futures.ProcessPoolExecutor() as executor:
  # https://stackoverflow.com/questions/62488423
  results = executor.map(worker.recognize_pil_text, images)
list(results)
```

![](https://camo.qiitausercontent.com/e172513d58e10c9ad6ddd148eeb78e1bc112f624/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3230383336332f61373136373537312d616135642d636231352d616461312d6132643230306535386562382e706e67)