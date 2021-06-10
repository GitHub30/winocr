import asyncio
from winrt.windows.media.ocr import OcrEngine
from winrt.windows.globalization import Language
from winrt.windows.storage.streams import DataWriter
from winrt.windows.graphics.imaging import SoftwareBitmap, BitmapPixelFormat

def recognize_bytes(bytes, width, height, lang='en'):
    cmd = 'Add-WindowsCapability -Online -Name "Language.OCR~~~en-US~0.0.1.0"'
    assert OcrEngine.is_language_supported(Language(lang)), cmd
    writer = DataWriter()
    writer.write_bytes(list(bytes))
    sb = SoftwareBitmap.create_copy_from_buffer(writer.detach_buffer(), BitmapPixelFormat.RGBA8, width, height)
    return OcrEngine.try_create_from_language(Language(lang)).recognize_async(sb)

def recognize_pil(img, lang='en'):
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    return recognize_bytes(img.tobytes(), img.width, img.height, lang)

def recognize_cv2(img, lang='en'):
    import cv2
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    return recognize_bytes(img.tobytes(), img.shape[1], img.shape[0], lang)

def picklify(o):
    if hasattr(o, 'size'):
        return [picklify(e) for e in o]
    elif hasattr(o, '__module__'):
        return dict([(n, picklify(getattr(o, n))) for n in dir(o) if not n.startswith('_')])
    else:
        return o

async def to_coroutine(awaitable):
    return await awaitable

def recognize_pil_sync(img, lang='en'):
    return picklify(asyncio.run(to_coroutine(recognize_pil(img, lang))))

def recognize_cv2_sync(img, lang='en'):
    return picklify(asyncio.run(to_coroutine(recognize_cv2(img, lang))))

def serve():
    import json
    import uvicorn
    from PIL import Image
    from io import BytesIO
    from fastapi import FastAPI, Request, Response
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI()
    app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
    @app.post('/')
    async def recognize(request: Request, lang: str = 'en'):
        result = await recognize_pil(Image.open(BytesIO(await request.body())), lang)
        return Response(json.dumps(picklify(result), indent=2, ensure_ascii=False), media_type='application/json')
    uvicorn.run(app, host='0.0.0.0')

if __name__ == '__main__':
    serve()
