# Rally Results Reader

Reads results from a screenshot of the DiRT Rally 2.0 website and converts to a CSV file.
![5](https://user-images.githubusercontent.com/41238606/115768757-a26cc980-a3a2-11eb-8881-abb67dde64e4.png)

How to run:

1. Install Python 3
   https://www.python.org/downloads/
2. Install packages\
   `pip install opencv-python`\
   `pip install pytesseract`\
   `pip install pandas`
3. Download Tesseract and install to 'Program Files'\
   https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.0-alpha.20201127.exe
4. Make sure results screenshots are in the screenshots folder named 1 to 5 (.png) and cropped in the same way the above screenshot is
5. To run program: `python3 reader.py`
