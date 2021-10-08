import img2pdf
from PIL import Image

import io
from io import BytesIO 
from PIL import Image, ImageDraw




img = Image.open('pages/page1.png')
img.convert('RGB')

buf = BytesIO()
with io.BytesIO() as buf:
    img.save(buf, 'png')
    image_bytes = buf.getvalue()

with open('pages/page1test.png', 'wb') as fl:
    fl.write(image_bytes)

'''
# specify paper size (A4)
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)
with open("name.pdf","wb") as f:
	f.write(img2pdf.convert(img, layout_fun=layout_fun))

'''
