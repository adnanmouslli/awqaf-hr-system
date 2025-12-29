# توثيق API البطاقات التعريفية

## نظرة عامة
تم تطوير نظام كامل لتوليد البطاقات التعريفية للموظفين بوجهين (أمامي وخلفي) باستخدام قوالب HTML ديناميكية.

## الملفات المُنشأة

### 1. القوالب (Templates)
- **`app/templates/id_card_front.html`**: قالب الوجه الأمامي للبطاقة
- **`app/templates/id_card_back.html`**: قالب الوجه الخلفي للبطاقة

### 2. المسارات (Routes)
- **`app/routes/id_card.py`**: يحتوي على جميع endpoints الخاصة بالبطاقات

---

## API Endpoints

### 1. الحصول على الوجه الأمامي للبطاقة (HTML)

**Endpoint:**
```
GET /api/employees/<emp_id>/id-card/front
```

**Headers:**
```
Authorization: Bearer <your-token>
```

**Response:**
- صفحة HTML كاملة للوجه الأمامي للبطاقة
- يمكن عرضها مباشرة في المتصفح
- جاهزة للطباعة

**مثال:**
```
GET http://localhost:5000/api/employees/1/id-card/front
```

---

### 2. الحصول على الوجه الخلفي للبطاقة (HTML)

**Endpoint:**
```
GET /api/employees/<emp_id>/id-card/back
```

**Headers:**
```
Authorization: Bearer <your-token>
```

**Response:**
- صفحة HTML كاملة للوجه الخلفي للبطاقة
- تحتوي على QR Code للتحقق

**مثال:**
```
GET http://localhost:5000/api/employees/1/id-card/back
```

---

### 3. الحصول على بيانات البطاقة (JSON) - للاستخدام في Flutter

**Endpoint:**
```
GET /api/employees/<emp_id>/id-card/data
```

**Headers:**
```
Authorization: Bearer <your-token>
Content-Type: application/json
```

**Response:**
```json
{
    "success": true,
    "employee_id": 1,
    "employee_name": "عدنان الموصللي",
    "data": {
        "front": {
            "fingerprint_id": "12345",
            "full_name": "عدنان الموصللي",
            "employee_type": "موظف دائم",
            "position": "مطور برمجيات",
            "national_id": "010213123213",
            "photo_url": "http://localhost:5000/uploads/photos/12345_images.png",
            "logo_url": "http://localhost:5000/uploads/logos/12345_logo.png",
            "republic_logo_url": "http://localhost:5000/uploads/Syrian Arab Republic_1.png",
            "ministry_name": "وزارة الأوقاف",
            "ministry_location": "مديرية أوقاف حلب"
        },
        "back": {
            "qr_code_url": "http://localhost:5000/uploads/barcodes/12345_qrcode.png",
            "barcode": "EMP-12345-2024",
            "logo_url": "http://localhost:5000/uploads/logos/12345_logo.png",
            "republic_logo_url": "http://localhost:5000/uploads/Syrian Arab Republic_1.png",
            "ministry_name": "وزارة الأوقاف"
        }
    }
}
```

**مثال:**
```
GET http://localhost:5000/api/employees/1/id-card/data
```

---

### 4. الحصول على بطاقات متعددة (Batch)

**Endpoint:**
```
POST /api/employees/id-cards/batch
```

**Headers:**
```
Authorization: Bearer <your-token>
Content-Type: application/json
```

**Request Body:**
```json
{
    "employee_ids": [1, 2, 3, 4, 5]
}
```

**Response:**
```json
{
    "success": true,
    "count": 5,
    "cards": [
        {
            "employee_id": 1,
            "employee_name": "عدنان الموصللي",
            "fingerprint_id": 12345,
            "data": {
                "front": { ... },
                "back": { ... }
            }
        },
        {
            "employee_id": 2,
            "employee_name": "محمد أحمد",
            "fingerprint_id": 12346,
            "data": {
                "front": { ... },
                "back": { ... }
            }
        }
        // ... بقية البطاقات
    ]
}
```

**مثال:**
```bash
curl -X POST http://localhost:5000/api/employees/id-cards/batch \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"employee_ids": [1, 2, 3]}'
```

---

## البيانات الديناميكية في القوالب

### الوجه الأمامي (Front)
يتم تمرير المتغيرات التالية للقالب:
- `fingerprint_id`: رقم البطاقة
- `full_name`: الاسم الكامل
- `employee_type`: نوع الموظف (دائم/مؤقت)
- `position`: المسمى الوظيفي
- `national_id`: الرقم الوطني
- `photo_url`: رابط صورة الموظف
- `logo_url`: رابط شعار الوزارة
- `republic_logo_url`: رابط شعار الجمهورية
- `ministry_name`: اسم الوزارة
- `ministry_location`: موقع المديرية

### الوجه الخلفي (Back)
- `qr_code_url`: رابط QR Code
- `logo_url`: رابط شعار الوزارة
- `republic_logo_url`: رابط شعار الجمهورية
- `ministry_name`: اسم الوزارة

---

## الاستخدام في Flutter

### 1. جلب بيانات البطاقة

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<Map<String, dynamic>> getEmployeeIdCard(int empId, String token) async {
  final response = await http.get(
    Uri.parse('http://your-server:5000/api/employees/$empId/id-card/data'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
  );

  if (response.statusCode == 200) {
    return json.decode(utf8.decode(response.bodyBytes));
  } else {
    throw Exception('Failed to load ID card data');
  }
}
```

### 2. عرض الصور في Flutter

```dart
import 'package:cached_network_image/cached_network_image.dart';

class EmployeeIdCard extends StatelessWidget {
  final Map<String, dynamic> cardData;
  final String token;

  const EmployeeIdCard({
    required this.cardData,
    required this.token,
  });

  @override
  Widget build(BuildContext context) {
    final frontData = cardData['data']['front'];

    return Column(
      children: [
        // صورة الموظف
        CachedNetworkImage(
          imageUrl: frontData['photo_url'],
          httpHeaders: {
            'Authorization': 'Bearer $token',
          },
          placeholder: (context, url) => CircularProgressIndicator(),
          errorWidget: (context, url, error) => Icon(Icons.person),
        ),

        // بقية المعلومات
        Text('${frontData['full_name']}'),
        Text('${frontData['position']}'),
        // ...
      ],
    );
  }
}
```

### 3. جلب بطاقات متعددة

```dart
Future<List<Map<String, dynamic>>> getBatchIdCards(
  List<int> employeeIds,
  String token
) async {
  final response = await http.post(
    Uri.parse('http://your-server:5000/api/employees/id-cards/batch'),
    headers: {
      'Authorization': 'Bearer $token',
      'Content-Type': 'application/json',
    },
    body: json.encode({
      'employee_ids': employeeIds,
    }),
  );

  if (response.statusCode == 200) {
    final data = json.decode(utf8.decode(response.bodyBytes));
    return List<Map<String, dynamic>>.from(data['cards']);
  } else {
    throw Exception('Failed to load batch ID cards');
  }
}
```

---

## ملاحظات مهمة

1. **التوثيق (Authentication)**: جميع Endpoints تتطلب token صالح في header
2. **الصور**: يجب أن تكون صور الموظفين والشعارات محملة مسبقاً في مجلد `uploads`
3. **QR Code**: يتم توليده تلقائياً عند إنشاء الموظف
4. **التصميم**: القوالب مصممة للطباعة وتحتوي على أبعاد محددة (1050x650 بكسل)
5. **اللغة**: القوالب تدعم العربية بالكامل مع RTL layout

---

## أمثلة على استخدام Postman

### 1. الحصول على الوجه الأمامي
```
GET http://localhost:5000/api/employees/1/id-card/front
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 2. الحصول على البيانات JSON
```
GET http://localhost:5000/api/employees/1/id-card/data
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### 3. Batch Request
```
POST http://localhost:5000/api/employees/id-cards/batch
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "employee_ids": [1, 2, 3]
}
```

---

## حل المشاكل الشائعة

### 1. الصور لا تظهر
- تأكد من وجود الصور في مجلد `uploads`
- تحقق من صلاحيات القراءة للمجلد
- تأكد من صحة المسارات في قاعدة البيانات

### 2. خطأ 404 عند طلب البطاقة
- تأكد من وجود الموظف في قاعدة البيانات
- تحقق من صحة `emp_id` المُرسل

### 3. القالب لا يعرض البيانات
- تأكد من أن القوالب موجودة في مجلد `app/templates`
- تحقق من أن Flask يمكنه الوصول لمجلد القوالب

---

## التحديثات المستقبلية المقترحة

1. إضافة إمكانية تصدير البطاقات كـ PDF
2. دعم قوالب متعددة حسب نوع الموظف
3. إضافة watermark للبطاقات
4. دعم الطباعة المباشرة
5. إضافة signature رقمي

---

**تم التطوير بواسطة:** Claude Code Assistant
**التاريخ:** 2025-12-29
**الإصدار:** 1.0
