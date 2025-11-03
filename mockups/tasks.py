from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
from .models import Mockup
import os
import uuid

@shared_task
def generate_mockup(text, font="arial", text_color="#000000", shirt_colors=None):
    tshirt_colors = shirt_colors or ["white", "black", "red"]
    base_dir = "media/tshirts"
    output_dir = "media/mockups"
    os.makedirs(output_dir, exist_ok=True)
    results = []

    for color in tshirt_colors:
        tshirt_path = os.path.join(base_dir, f"{color}.png")

        if not os.path.exists(tshirt_path):
            continue  # اگر مثلا تیشرت قرمز وجود نداشت، رد میشه

        img = Image.open(tshirt_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()

        # محاسبه موقعیت وسط تصویر
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (img.width - text_width) / 2
        y = (img.height - text_height) / 2

        # نوشتن متن روی تی‌شرت
        draw.text((x, y), text, fill="black", font=font)

        filename = f"{uuid.uuid4()}.png"
        output_path = os.path.join(output_dir, filename)
        img.save(output_path)

        mockup = Mockup.objects.create(
            text=text,
            font="arial",
            text_color="#000000",
            shirt_color=color,
            image=f"/mockups/{filename}"
        )

        results.append({
            "id": mockup.id,
            "text": text,
            "shirt_color": color,
            "image": mockup.image.url if hasattr(mockup.image, "url") else str(mockup.image),
        })

    return results

# ================
# from celery import shared_task
# from PIL import Image, ImageDraw, ImageFont
# from django.conf import settings
# from .models import Mockup
# import os
# import uuid

# @shared_task
# def generate_mockup(text, font='arial', text_color='#000000', shirt_colors=None):
#     if shirt_colors is None:
#         shirt_colors = ['white', 'black', 'blue', 'red']

#     results = []
#     base_path = os.path.join(settings.MEDIA_ROOT, 'mockups')
#     os.makedirs(base_path, exist_ok=True)

#     for color in shirt_colors:
#         # یه تصویر ساده به عنوان تیشرت می‌سازیم
#         img = Image.new('RGB', (400, 400), color=color)
#         draw = ImageDraw.Draw(img)

#         # نوشتن متن وسط تصویر
#         draw.text((100, 180), text, fill=text_color)

#         # ذخیره‌ی تصویر
#         filename = f"{uuid.uuid4()}.png"
#         path = os.path.join(base_path, filename)
#         img.save(path)

#         # ذخیره در دیتابیس
#         Mockup.objects.create(
#             text=text,
#             font=font,
#             text_color=text_color,
#             shirt_color=color,
#             image=f"mockups/{filename}",
#         )

#         results.append(filename)

#     return results

