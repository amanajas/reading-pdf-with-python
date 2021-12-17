import io
import sys

from PIL import Image
import pytesseract
from wand.image import Image as wi
from tika import parser


def extract_text_image(from_file, lang='deu', image_type='jpeg', resolution=300):
    print("-- Parsing image", from_file, "--")
    print("---------------------------------")
    pdf_file = wi(filename=from_file, resolution=resolution)
    image = pdf_file.convert(image_type)
    image_blobs = []
    for img in image.sequence:
        img_page = wi(image=img)
        image_blobs.append(img_page.make_blob(image_type))
    extract = []
    for img_blob in image_blobs:
        image = Image.open(io.BytesIO(img_blob))
        text = pytesseract.image_to_string(image, lang=lang)
        extract.append(text)
    for item in extract:
        for line in item.split("\n"):
            print(line)


def parse_text(from_file):
    print("-- Parsing text", from_file, "--")
    text_raw = parser.from_file(from_file)
    print("---------------------------------")
    print(text_raw['content'])
    print("---------------------------------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Must contain <file [<lang>]>")
    else:
        parse_text(sys.argv[1])
        if len(sys.argv) >= 3:
            extract_text_image(sys.argv[1], sys.argv[2])
