from celery import shared_task
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from .models import Mockup
import os
import uuid

@shared_task
def generate_mockup(text, font='arial', text_color='#000000', shirt_colors=None):
    if shirt_colors is None:
        shirt_colors = ['white', 'black', 'blue', 'red']

    results = []
    base_path = os.path.join(settings.MEDIA_ROOT, 'mockups')
    os.makedirs(base_path, exist_ok=True)

    for color in shirt_colors:
        # یه تصویر ساده به عنوان تیشرت می‌سازیم
        img = Image.new('RGB', (400, 400), color=color)
        draw = ImageDraw.Draw(img)

        # نوشتن متن وسط تصویر
        draw.text((100, 180), text, fill=text_color)

        # ذخیره‌ی تصویر
        filename = f"{uuid.uuid4()}.png"
        path = os.path.join(base_path, filename)
        img.save(path)

        # ذخیره در دیتابیس
        Mockup.objects.create(
            text=text,
            font=font,
            text_color=text_color,
            shirt_color=color,
            image=f"mockups/{filename}",
        )

        results.append(filename)

    return results

