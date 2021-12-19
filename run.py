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
    for img in image.sequence:
        img_page = wi(image=img)
        image = Image.open(io.BytesIO(img_page.make_blob(image_type)))
        text = pytesseract.image_to_string(image, lang=lang)
        for part in text.split("\n"):
            print("{}".format(part))


def parse_text(from_file):
    print("-- Parsing text", from_file, "--")
    text_raw = parser.from_file(from_file)
    print("---------------------------------")
    print(text_raw['content'].strip())
    print("---------------------------------")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Must contain <file [<lang>]>")
    else:
        parse_text(sys.argv[1])
        if len(sys.argv) >= 3:
            extract_text_image(sys.argv[1], sys.argv[2])
