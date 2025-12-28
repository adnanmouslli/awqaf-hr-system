FROM python:3.9-slim

# تثبيت المتطلبات الأساسية
RUN apt-get update && apt-get install -y \
    gnupg2 \
    curl \
    apt-transport-https \
    iputils-ping \
    telnet \
    && rm -rf /var/lib/apt/lists/*

# إضافة مفتاح Microsoft GPG بشكل صحيح
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg

# إضافة مستودع Microsoft SQL Server
RUN curl -sSL https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list

# تحديث وتثبيت ODBC Driver
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17 unixodbc-dev build-essential && rm -rf /var/lib/apt/lists/*

# إنشاء مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيت باكدجات البايثون
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# نسخ سكربت الدخول وجعله قابل للتنفيذ
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# نسخ باقي الملفات
COPY . /app/

# إنشاء مجلد للتحميلات
RUN mkdir -p /app/uploads

# تعيين المتغيرات البيئية
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# تشغيل الـ entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python", "run.py"]

