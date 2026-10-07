"""Set exact page boxes and restore original logo pixels; no content resampling.

Requires pypdf; optional --restore-logo also requires Pillow.
"""
import argparse
from pathlib import Path
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('input', type=Path)
parser.add_argument('output', type=Path)
parser.add_argument('--restore-logo', type=Path)
args = parser.parse_args()
reader = PdfReader(args.input)
if len(reader.pages) != 1:
    raise ValueError('Expected one page')
writer = PdfWriter()
writer.clone_document_from_reader(reader)
writer.pdf_header = reader.pdf_header
page = writer.pages[0]
box = RectangleObject([0, 0, 75 / 2.54 * 72, 120 / 2.54 * 72])
if abs(float(page.mediabox.width) - float(box.width)) > 0.1 or abs(float(page.mediabox.height) - float(box.height)) > 0.1:
    raise ValueError('Source dimensions differ by more than PowerPoint rounding')
page.mediabox = box
page.cropbox = RectangleObject(box)
if args.restore_logo:
    from PIL import Image
    original = Image.open(args.restore_logo).convert('RGBA')
    matches = []
    for reference in page['/Resources']['/XObject'].values():
        image = reference.get_object()
        if image.get('/Subtype') == '/Image' and (int(image['/Width']), int(image['/Height'])) == original.size:
            matches.append(image)
    if len(matches) != 1:
        raise ValueError('Expected exactly one matching logo image')
    image = matches[0]
    if image['/ColorSpace'] != '/DeviceRGB' or image.get('/DecodeParms'):
        raise ValueError('Unexpected logo color space or predictor')
    # PowerPoint can premultiply transparent PNG colors. Restore the exact
    # source color and alpha planes inside the PDF image XObject, losslessly.
    image.set_data(original.convert('RGB').tobytes())
    image['/SMask'].set_data(original.getchannel('A').tobytes())
writer.add_metadata({'/Title': 'A Prospective Rank Test of a Detector-Error-Model Weight Screen for Circuit-Level qLDPC Decoding', '/Author': 'Hung N. Dang and Quy X. Pham'})
args.output.parent.mkdir(parents=True, exist_ok=True)
with args.output.open('wb') as stream:
    writer.write(stream)
