# Mockup Generator (T-Shirt Text Overlay)

This project is a T-shirt mockup generator built with **Django**, **Celery**, **Redis**, and **Pillow**.  
It takes a text input, overlays it on plain T-shirt images of various colors, and stores the generated images in the `media/mockups/` directory.

---

## Setup and Installation

### 1. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate     # On Windows
# or
source venv/bin/activate  # On Linux/Mac
```

### 2. Install dependencies
If you have a `requirements.txt` file:
```bash
pip install -r requirements.txt
```
Otherwise, install manually:
```bash
pip install django pillow celery redis
```

---

## Django Configuration

### 3. Media settings
In `settings.py`, add the following lines:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

In your main `urls.py` (for example, `core/urls.py`):
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/mockups/', include('mockups.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## Folder Structure

### 4. Create the required directories
```
media/
 ├── tshirts/
 │    ├── white.png
 │    ├── black.png
 │    ├── blue.png
 │    └── yellow.png
 └── mockups/
```
The `tshirts/` folder should contain plain T-shirt images (without any text) named according to their color.

---

## Redis and Celery Setup

### 5. Run Redis
If you have Docker installed:
```bash
docker run -d -p 6379:6379 redis
```
If Redis is installed locally, ensure it is running:
```bash
redis-server
```

### 6. Start Celery worker
```bash
celery -A core worker -l info
```
If your Django project name is different from `core`, replace it accordingly.

---

## Running the Application

### 7. Start the Django server
```bash
python manage.py runserver
```

---

## API Endpoints

### 8. Generate a mockup
**Endpoint:**
```
POST /api/v1/mockups/generate/
```
**Request body (JSON):**
```json
{
    "text": "Hello World",
    "font": "arial",
    "text_color": "#000000"
}
```
**Response:**
```json
{
    "task_id": "1234abcd-5678-efgh-9012-ijklmnopqrst"
}
```

---

### 9. Check task status
**Endpoint:**
```
GET /api/v1/mockups/tasks/<task_id>/
```
**Example response:**
```json
{
    "task_id": "1234abcd-5678-efgh-9012-ijklmnopqrst",
    "status": "SUCCESS",
    "results": [
        {
            "id": 1,
            "text": "Hello World",
            "shirt_color": "white",
            "image": "/media/mockups/abcd1234.png"
        }
    ]
}
```

If the status is `FAILURE`, check the Celery terminal output for error logs.

---

## Output Files

All generated mockup images are saved in:
```
media/mockups/
```
Each file is named with a unique UUID and contains the text centered on the corresponding T-shirt.

---

## Notes

- Ensure that all base T-shirt images exist in `media/tshirts/` before generating mockups.
- If text is not visible on a certain color (e.g., yellow shirts), you can dynamically change text color depending on the shirt color.
- The font file (e.g., `arial.ttf`) must be available on the system or in the project directory.

##
Mockup Generator (Django + Celery + Redis)
Overview

This project is a Django-based API for generating T-shirt mockups with custom text.
It uses Celery for background task processing and Redis as the message broker.
Each request creates multiple T-shirt mockups with the desired text printed on different shirt colors.

How It Works

User Request
The user sends a POST request to the endpoint /api/v1/mockups/generate/ with parameters such as:

{
    "text": "Hello World",
    "font": "arial",
    "text_color": "#000000",
    "shirt_colors": ["white", "black", "blue", "yellow"]
}


Task Creation
The view (MockupGenerateView) receives the request and sends a background task to Celery using:

task = generate_mockup.delay(text, font, text_color, shirt_colors)


Django immediately responds with a task ID and a PENDING status.

Background Processing (Celery)
The Celery worker picks up the task and runs the generate_mockup function located in mockups/tasks.py.
This function:

Loads each T-shirt image from media/tshirts/

Draws the given text centered on the shirt using Pillow (PIL)

Saves the result in media/mockups/

Creates a database entry (Mockup model) for each generated image

Returns metadata (ID, color, image path, etc.)

Result Retrieval
The client can check the task status via:

GET /api/v1/mockups/tasks/<task_id>/


When processing is complete, the response includes all generated mockup data and image URLs.

Media Handling
Django serves the generated mockup files from media/mockups/.
The source T-shirt templates should be placed in:

media/tshirts/
├── white.png
├── black.png
├── blue.png
└── yellow.png

Project Structure
project_root/
│
├── core/                  # Main Django project settings
├── mockups/               # App for T-shirt mockup logic
│   ├── tasks.py           # Celery background task for image generation
│   ├── models.py          # Mockup model
│   ├── views.py           # API views and endpoints
│   └── urls.py            # App-level URLs
│
├── media/
│   ├── tshirts/           # Base T-shirt images (input)
│   └── mockups/           # Generated mockups (output)
│
├── manage.py
└── requirements.txt

Technologies Used

Django 5.x – web framework for API

Celery 5.x – background task queue

Redis – message broker and result backend

Pillow (PIL) – image processing

SQLite / PostgreSQL – database (configurable)

Run Instructions
1. Install dependencies
pip install -r requirements.txt

2. Run Redis

You must have Redis running locally (or in Docker):

docker run -d -p 6379:6379 redis

3. Run Django
python manage.py runserver

4. Run Celery worker
celery -A core worker -l info -P solo

5. Test API

Send a POST request to:

http://127.0.0.1:8000/api/v1/mockups/generate/


Then check the task result:

http://127.0.0.1:8000/api/v1/mockups/tasks/<task_id>/

## translate
مولد طرح تی‌شرت (Mockup Generator)
مقدمه

این پروژه یک API مبتنی بر Django است که وظیفه آن تولید طرح‌های (Mockup) تی‌شرت با متن دلخواه کاربر است.
پروژه از Celery برای اجرای تسک‌ها در پس‌زمینه و از Redis به عنوان Message Broker استفاده می‌کند.
هر درخواست (Request) باعث ایجاد چند تصویر از تی‌شرت با رنگ‌های مختلف و متن درج‌شده روی آن می‌شود.

نحوه عملکرد سیستم

درخواست کاربر (POST Request)
کاربر یک درخواست به مسیر زیر ارسال می‌کند:

/api/v1/mockups/generate/


همراه با پارامترهایی مانند:

{
    "text": "سلام دنیا",
    "font": "arial",
    "text_color": "#000000",
    "shirt_colors": ["white", "black", "blue", "yellow"]
}


ایجاد تسک در Celery
ویو MockupGenerateView درخواست را دریافت کرده و تسک را با دستور زیر به Celery ارسال می‌کند:

task = generate_mockup.delay(text, font, text_color, shirt_colors)


Django بلافاصله پاسخ می‌دهد که تسک با موفقیت ایجاد شده و وضعیت آن در حالت PENDING است.

اجرای تسک در پس‌زمینه
Celery Worker تسک را از Redis گرفته و تابع generate_mockup را در فایل mockups/tasks.py اجرا می‌کند.
این تابع:

عکس هر تی‌شرت را از مسیر media/tshirts/ بارگذاری می‌کند

متن را در مرکز تصویر رسم می‌کند (با کتابخانه Pillow)

نتیجه را در مسیر media/mockups/ ذخیره می‌کند

رکوردی از آن را در دیتابیس (Mockup model) ذخیره می‌کند

و در نهایت مشخصات هر خروجی (ID، رنگ، مسیر عکس و ...) را برمی‌گرداند

دریافت نتیجه تسک
برای بررسی وضعیت تسک، کاربر می‌تواند درخواست زیر را بفرستد:

GET /api/v1/mockups/tasks/<task_id>/


زمانی که وضعیت تسک SUCCESS شود، خروجی شامل مسیر تمام تصاویر تولیدشده است.

ساختار فایل‌های رسانه (Media)
تصاویر خام تی‌شرت‌ها باید در این مسیر باشند:

media/tshirts/
├── white.png
├── black.png
├── blue.png
└── yellow.png


خروجی تصاویر تولیدشده در:

media/mockups/

ساختار پروژه
project_root/
│
├── core/                  # تنظیمات اصلی Django
├── mockups/               # اپلیکیشن تولید ماکاپ
│   ├── tasks.py           # تسک‌های Celery برای تولید تصویر
│   ├── models.py          # مدل Mockup
│   ├── views.py           # ویوهای API
│   └── urls.py            # مسیرهای اپلیکیشن
│
├── media/
│   ├── tshirts/           # تصاویر خام تی‌شرت
│   └── mockups/           # خروجی تصاویر تولیدی
│
├── manage.py
└── requirements.txt

تکنولوژی‌های مورد استفاده

Django 5.x — فریم‌ورک اصلی وب

Celery 5.x — سیستم صف تسک‌ها

Redis — واسطه پیام‌ها و ذخیره نتایج

Pillow (PIL) — پردازش تصویر

SQLite / PostgreSQL — پایگاه داده

نحوه اجرا
۱. نصب وابستگی‌ها
pip install -r requirements.txt

۲. اجرای Redis (ترجیحاً در Docker)
docker run -d -p 6379:6379 redis

۳. اجرای Django
python manage.py runserver

۴. اجرای Celery Worker
celery -A core worker -l info -P solo

۵. ارسال درخواست برای تولید تصویر
POST http://127.0.0.1:8000/api/v1/mockups/generate/

۶. بررسی نتیجه تسک
GET http://127.0.0.1:8000/api/v1/mockups/tasks/<task_id>/

نحوه عملکرد کلی سیستم

Django مسئول دریافت درخواست از کاربر است.
Celery تسک تولید تصویر را به صورت غیربلاکینگ در پس‌زمینه اجرا می‌کند.
Redis پیام‌ها و وضعیت تسک‌ها را نگه می‌دارد.
Pillow متن را روی تصویر تی‌شرت رسم می‌کند.
در نهایت خروجی در پوشه media/mockups/ ذخیره می‌شود و از طریق API برگردانده می‌شود.