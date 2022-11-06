import setuptools

api = ["Pillow", "fastapi", "uvicorn"]
cv2 = ["opencv-python"]
all = api + cv2

setuptools.setup(
    name="winocr",
    version="0.0.12",
    author="Tomofumi Inoue",
    author_email="funaox@gmail.com",
    description="Windows.Media.Ocr",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/GitHub30/winocr",
    project_urls={"Bug Tracker": "https://github.com/GitHub30/winocr/issues",},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
    ],
    install_requires=["winsdk"],
    extras_require={"all": all, "api": api, "cv2": cv2},
    py_modules=["winocr"],
    entry_points={"console_scripts": ["winocr_serve = winocr:serve"]},
)
# Publish commands
# https://packaging.python.org/tutorials/packaging-projects/
# pip install --upgrade pip build twine
# python -m build
# python -m twine upload dist/*

