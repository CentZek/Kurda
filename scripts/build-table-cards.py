"""Create an A4 sheet of eleven 85 x 54 mm landscape menu cards.

Requires reportlab, qrcode and fonttools. Run from the repository root.
The six rotated cards are turned sideways solely for efficient imposition.
"""
from pathlib import Path
import shutil
import qrcode
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from fontTools.ttLib import TTFont as Font
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / 'output/pdf'
TMP = ROOT / 'tmp/pdfs'
OUTPUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
ASSETS = ROOT / 'dist/assets'
QR_DIR = ROOT / 'dist/menu/qr'
URL = 'https://www.kurda.com/menu'

# Embed a static instance of the same DM Sans used on the website.
font = Font(ASSETS / 'dm-sans-latin.woff2')
axes = {axis.axisTag: (500 if axis.axisTag == 'wght' else axis.defaultValue) for axis in font['fvar'].axes}
font = instantiateVariableFont(font, axes, inplace=True)
font.flavor = None
font.save(TMP / 'dm-sans-print.ttf')
pdfmetrics.registerFont(TTFont('DM', str(TMP / 'dm-sans-print.ttf')))
pdfmetrics.registerFont(TTFont('Georgia', 'C:/Windows/Fonts/georgia.ttf'))

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, border=4, box_size=1)
qr.add_data(URL)
qr.make(fit=True)
matrix = qr.get_matrix()
navy, gold = HexColor('#12132f'), HexColor('#e7b630')
dest = OUTPUT / 'kurda-table-cards-85x54mm-a4.pdf'
c = canvas.Canvas(str(dest), pagesize=(210*mm, 297*mm), pageCompression=1)
c.setTitle('Kurda menu table cards - 85 x 54 mm - 11 on A4')
c.setAuthor('Kurda')
c.setSubject('Print A4 portrait at Actual size / 100%. Eleven landscape cards with cutting guides.')

def text(x, y, value, size, font='DM', center=False):
    c.setFillColor(navy)
    c.setFont(font, size)
    (c.drawCentredString if center else c.drawString)(x*mm, y*mm, value)

def card():
    # Every element remains safely inside the final 85 x 54 mm trim.
    c.setFillColor(gold)
    c.roundRect(5*mm, 32.5*mm, 10*mm, .7*mm, .35*mm, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ASSETS/'kurda-logo-english.png')), 5*mm, 36*mm, width=29*mm, height=12.3975*mm, mask='auto')
    c.drawImage(ImageReader(str(ASSETS/'kurda-logo-kurdish.png')), 36*mm, 37.3*mm, width=7*mm, height=8.9444*mm, mask='auto')
    text(5, 25, 'Explore', 15, 'Georgia')
    text(5, 18.5, 'our menu', 15, 'Georgia')
    text(5, 12.8, 'Food / Coffee / Bar', 7)
    text(5, 5.5, 'www.kurda.com/menu', 6.8)
    text(63.5, 47.3, 'SCAN ME', 7, center=True)
    # Vector modules, including the four-module white quiet zone.
    module = 33*mm/len(matrix)
    c.setFillColorRGB(0, 0, 0)
    path = c.beginPath()
    for row, cells in enumerate(matrix):
        for col, dark in enumerate(cells):
            if dark:
                path.rect(47*mm+col*module, 12*mm+(len(matrix)-1-row)*module, module, module)
    c.drawPath(path, fill=1, stroke=0)
    text(63.5, 7, 'Scan to view the menu', 6.2, center=True)

def guides(x, y, w, h):
    # Solid black trim boundaries remain clear on ordinary office printers.
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(.8)
    c.setDash()
    c.rect(x*mm, y*mm, w*mm, h*mm, fill=0, stroke=1)
    c.setDash()
    c.setStrokeColorRGB(0, 0, 0)
    c.setLineWidth(1)
    for px in [x, x+w]:
        for py in [y, y+h]:
            sx = -1 if px == x else 1
            sy = -1 if py == y else 1
            c.line((px+sx*.4)*mm, py*mm, (px+sx*1.2)*mm, py*mm)
            c.line(px*mm, (py+sy*.4)*mm, px*mm, (py+sy*1.2)*mm)

# 199 x 282 mm occupied footprint, 3 mm gutters, centred on A4.
placements = [(5.5, 7.5+i*57, False) for i in range(5)]
placements += [(x, 18+i*88, True) for x in [93.5, 150.5] for i in range(3)]
for x, y, rotated in placements:
    w, h = (54, 85) if rotated else (85, 54)
    guides(x, y, w, h)
    c.saveState()
    if rotated:
        c.translate((x+54)*mm, y*mm)
        c.rotate(90)
    else:
        c.translate(x*mm, y*mm)
    card()
    c.restoreState()
c.showPage()
c.save()
shutil.copy2(dest, QR_DIR/dest.name)
print(f'Created {dest}: 11 cards, 85 x 54 mm, one A4 page.')
