# أمثلة اختبار API - Testing Examples

## 📝 ملاحظات مهمة / Important Notes

1. **التوكن**: استبدل `YOUR_TOKEN_HERE` بالتوكن الفعلي الخاص بك
2. **الصور**: لرفع الصور، يجب استخدام `multipart/form-data`
3. **QR Code**: يتم توليد QR Code تلقائياً عند إنشاء موظف جديد

---

## 1️⃣ إنشاء موظف - مثال كامل / Create Employee - Full Example

### استخدام Postman:

1. افتح Postman
2. استورد الملف: `postman_create_employee.json`
3. اختر "إنشاء موظف جديد - Create New Employee"
4. ضع التوكن في Authorization
5. أضف الصور إذا أردت (اختياري)
6. اضغط Send

### استخدام cURL (بدون صور):

```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=12345" \
  -F "full_name=أحمد محمد علي" \
  -F "employee_type=permanent" \
  -F "work_system=shift" \
  -F "position=5" \
  -F "salary=5000" \
  -F "contact_number=0911222333" \
  -F "blood_type=A+" \
  -F "card_expiry_date=2025-12-31"
```

### استخدام cURL (مع صور):

```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=12345" \
  -F "full_name=أحمد محمد علي" \
  -F "employee_type=permanent" \
  -F "work_system=shift" \
  -F "position=5" \
  -F "salary=5000" \
  -F "contact_number=0911222333" \
  -F "blood_type=A+" \
  -F "card_expiry_date=2025-12-31" \
  -F "logo=@/path/to/logo.png" \
  -F "photo=@/path/to/photo.jpg"
```

### النتيجة المتوقعة / Expected Response:

```json
{
  "message": "Employee created",
  "employee": {
    "id": 123,
    "full_name": "أحمد محمد علي",
    "position": 5,
    "certificates": null,
    "branch_id": null,
    "department_id": null,
    "overtime_multiplier": 1.5,
    "daily_rate": 166.67,
    "hourly_rate": 20.83,
    "barcode": "EMP-12345-A1B2C3D4",
    "barcode_image_path": "/uploads/barcodes/12345_qrcode.png",
    "logo_path": "/uploads/logos/12345_logo.png",
    "photo_path": "/uploads/photos/12345_photo.jpg",
    "contact_number": "0911222333",
    "blood_type": "A+",
    "card_expiry_date": "2025-12-31"
  }
}
```

---

## 2️⃣ البحث بالباركود / Search by Barcode

### استخدام cURL:

```bash
curl -X GET http://localhost:5000/api/employees/barcode/EMP-12345-A1B2C3D4 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### النتيجة المتوقعة:

```json
{
  "id": 123,
  "fingerprint_id": "12345",
  "full_name": "أحمد محمد علي",
  "employee_type": "permanent",
  "barcode": "EMP-12345-A1B2C3D4",
  "barcode_image_path": "/uploads/barcodes/12345_qrcode.png",
  "contact_number": "0911222333",
  "blood_type": "A+",
  "card_expiry_date": "2025-12-31",
  ...
}
```

---

## 3️⃣ جلب موظف بالـ ID / Get Employee by ID

```bash
curl -X GET http://localhost:5000/api/employees/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 4️⃣ جلب جميع الموظفين / Get All Employees

```bash
curl -X GET http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 5️⃣ تحديث بيانات موظف / Update Employee

```bash
curl -X PUT http://localhost:5000/api/employees/123 \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "salary": 6000,
    "contact_number": "0922333444",
    "blood_type": "B+",
    "card_expiry_date": "2026-12-31"
  }'
```

**ملاحظة**: الصور (logo, photo) والباركود لا يمكن تحديثهم عبر هذا الـ endpoint

---

## 🧪 اختبار QR Code / Test QR Code

### 1. إنشاء موظف جديد
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=99999" \
  -F "full_name=موظف اختبار" \
  -F "employee_type=permanent" \
  -F "work_system=shift" \
  -F "position=1" \
  -F "contact_number=0911111111" \
  -F "blood_type=O+"
```

### 2. احصل على مسار QR Code من الاستجابة
```json
{
  "employee": {
    "barcode_image_path": "/uploads/barcodes/99999_qrcode.png"
  }
}
```

### 3. افتح الصورة
افتح الملف: `uploads/barcodes/99999_qrcode.png`

### 4. امسح QR Code بكاميرا الجوال
- افتح كاميرا الجوال
- وجهها نحو QR Code
- سيفتح رابط: `http://localhost:5000/employee/{employee_id}`

**ملاحظة**: لكي يعمل الرابط على الجوال، يجب أن يكون الموقع متاحاً على الإنترنت أو على نفس الشبكة المحلية

---

## 🎯 أمثلة لحالات مختلفة

### موظف دائم / Permanent Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=10001" \
  -F "full_name=علي أحمد" \
  -F "employee_type=permanent" \
  -F "work_system=shift" \
  -F "position=3" \
  -F "salary=4500" \
  -F "blood_type=AB+"
```

### موظف مؤقت / Temporary Employee
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=20001" \
  -F "full_name=سارة محمد" \
  -F "employee_type=temporary" \
  -F "work_system=daily" \
  -F "profession=2" \
  -F "daily_rate=200" \
  -F "blood_type=O-"
```

### موظف مع جميع البيانات / Employee with All Data
```bash
curl -X POST http://localhost:5000/api/employees \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -F "fingerprint_id=30001" \
  -F "full_name=محمود خالد عمر السوري" \
  -F "employee_type=permanent" \
  -F "work_system=shift" \
  -F "position=5" \
  -F "salary=7000" \
  -F "allowances=1000" \
  -F "insurance_deduction=300" \
  -F "advancePercentage=25" \
  -F "birth_date=1985-03-20" \
  -F "birth_place=دمشق" \
  -F "id_number=987654321" \
  -F "national_id=01234567890123" \
  -F "residence=دمشق - المزة" \
  -F "phone1=0911111111" \
  -F "phone2=0922222222" \
  -F "date_of_joining=2020-01-15" \
  -F "branch_id=1" \
  -F "department_id=3" \
  -F "shift_id=2" \
  -F "contact_number=0933333333" \
  -F "blood_type=A+" \
  -F "card_expiry_date=2026-12-31"
```

---

## 🔧 تغيير رابط QR Code

إذا أردت تغيير الرابط الذي يفتحه QR Code:

1. افتح الملف: `app/config.py`
2. غير قيمة `BASE_URL`:
```python
BASE_URL = "https://yourwebsite.com"
```
3. أعد تشغيل التطبيق
4. الموظفين الجدد سيحصلون على QR Code بالرابط الجديد

---

## 📊 الحقول المطلوبة vs الاختيارية

### حقول مطلوبة (Required):
- `fingerprint_id` - رقم البصمة
- `full_name` - الاسم الكامل
- `employee_type` - نوع الموظف (permanent / temporary)
- `work_system` - نظام العمل
- `position` - المسمى الوظيفي (للموظف الدائم فقط)
- `profession` - المهنة (للموظف المؤقت فقط)

### حقول اختيارية (Optional):
- جميع الحقول الأخرى اختيارية
- `logo`, `photo` - الصور
- `contact_number`, `blood_type`, `card_expiry_date` - الحقول الجديدة
- `barcode` - يتم توليده تلقائياً إذا لم يُدخل

---

## ❗ استكشاف الأخطاء / Troubleshooting

### خطأ: "Missing fields"
تأكد من إرسال جميع الحقول المطلوبة

### خطأ: "Position is required for permanent employees"
إذا كان `employee_type=permanent`، يجب إرسال `position`

### خطأ: "Profession is required for temporary employees"
إذا كان `employee_type=temporary`، يجب إرسال `profession`

### QR Code لا يتولد
تأكد من:
1. تثبيت مكتبة qrcode: `pip install qrcode[pil]`
2. وجود مجلد `uploads/barcodes`
3. صلاحيات الكتابة على المجلد

---

## 📱 مسح QR Code على الجوال

### للاختبار على الشبكة المحلية:

1. تأكد أن السيرفر يعمل على: `0.0.0.0` وليس `localhost`
2. اعرف IP الجهاز:
   - Windows: `ipconfig`
   - Linux/Mac: `ifconfig`
3. غير `BASE_URL` في config.py:
```python
BASE_URL = "http://192.168.1.100:5000"  # ضع IP جهازك
```
4. أنشئ موظف جديد
5. امسح QR Code بالجوال - سيفتح الرابط!

---

## ✅ Checklist للاختبار

- [ ] إنشاء موظف دائم مع الحقول الأساسية
- [ ] إنشاء موظف مؤقت
- [ ] إنشاء موظف مع صور (logo, photo)
- [ ] إنشاء موظف مع الحقول الجديدة (contact_number, blood_type, card_expiry_date)
- [ ] التحقق من توليد QR Code
- [ ] البحث عن موظف بالباركود
- [ ] مسح QR Code بكاميرا الجوال
- [ ] تحديث بيانات موظف
- [ ] جلب موظف بالـ ID
- [ ] جلب جميع الموظفين
