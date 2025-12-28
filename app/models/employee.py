# employee.py

from app import db
from sqlalchemy import NVARCHAR, event, CheckConstraint

from app.models.department import Department

class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    fingerprint_id = db.Column(db.String(50), nullable=False)  # رقم الموظف على جهاز البصمة
    full_name = db.Column(db.String(255), nullable=False)  # الاسم الرباعي
    employee_type = db.Column(db.String(50), nullable=True)  # 'permanent' or 'temporary'

    # New fields for department and branch connections
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=True)  # ربط مع الفرع
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)  # ربط مع القسم
    

    position = db.Column(db.Integer, db.ForeignKey('job_titles.id'), nullable=True)  # ربط مع جدول المسمى الوظيفي
    salary = db.Column(db.Numeric(10, 2), default=0)  # المرتب
    advancePercentage = db.Column(db.Numeric(5, 2), nullable=True)  # حقل نسبة السلفة
    certificates = db.Column(db.Text, nullable=True)  # الشهادات الحاصل عليها
    date_of_birth = db.Column(db.Date, nullable=True)  # تاريخ الولادة
    place_of_birth = db.Column(db.String(255), nullable=True)  # مكان الولادة
    id_card_number = db.Column(db.String(50), nullable=True)  # رقم البطاقة
    national_id = db.Column(db.String(50), nullable=True)  # الرقم الوطني
    residence = db.Column(db.String(255), nullable=True)  # مكان الإقامة
    mobile_1 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 1
    mobile_2 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 2
    mobile_3 = db.Column(db.String(15), nullable=True)  # رقم الموبايل 3
    worker_agreement = db.Column(db.Text, nullable=True)  # اتفاق العامل
    notes = db.Column(db.Text, nullable=True)  # ملاحظات

    work_system = db.Column(db.String(100), nullable=True)  # نظام العمل
    shift_id = db.Column(db.Integer, db.ForeignKey('shift.id'), nullable=True)  # رقم الوردية (ربط مع جدول الورديات)
    profession_id = db.Column(db.Integer, db.ForeignKey('professions.id'), nullable=True)  # ربط بالمهن المؤقتة

    insurance_deduction = db.Column(db.Float, default=0)  # خصم التأمينات
    allowances = db.Column(db.Float, default=0)  # البدلات
    insurance_start_date = db.Column(db.Date, nullable=True)
    insurance_end_date = db.Column(db.Date, nullable=True)

    # الحقول الجديدة المضافة
    overtime_multiplier = db.Column(db.Numeric(3, 2), default=1.5)  # معامل الإضافي (مثل 1.5 للوقت الإضافي)
    daily_rate = db.Column(db.Numeric(10, 2), nullable=True)  # سعر اليوم للموظف
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=True)  # سعر الساعة للموظف

    # حقول الصور والباركود
    logo_path = db.Column(db.String(255), nullable=True)  # مسار صورة اللوغو
    photo_path = db.Column(db.String(255), nullable=True)  # مسار صورة الموظف
    barcode = db.Column(db.String(100), unique=True, nullable=True)  # الباركود الخاص بالموظف (النص)
    barcode_image_path = db.Column(db.String(255), nullable=True)  # مسار صورة الباركود

    # حقول إضافية
    contact_number = db.Column(db.String(15), nullable=True)  # رقم تواصل
    blood_type = db.Column(db.String(5), nullable=True)  # زمرة الدم (A+, A-, B+, B-, AB+, AB-, O+, O-)
    card_expiry_date = db.Column(db.Date, nullable=True)  # تاريخ صلاحية البطاقة/تاريخ المنح

    date_of_joining = db.Column(db.Date, nullable=True)  # موعد التعيين
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # تاريخ الإضافة
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())  # تاريخ التحديث


    user_account = db.relationship('User', backref=db.backref('employee', lazy=True), uselist=False)

     # قيود إضافية
    __table_args__ = (
        # قيد للتأكد من أن تاريخ نهاية التأمين بعد تاريخ البداية
        CheckConstraint('insurance_end_date IS NULL OR insurance_end_date > insurance_start_date', name='check_insurance_dates'),
        # قيود للحقول الجديدة
        CheckConstraint('overtime_multiplier > 0', name='check_overtime_multiplier_positive'),
        CheckConstraint('daily_rate IS NULL OR daily_rate >= 0', name='check_daily_rate_non_negative'),
        CheckConstraint('hourly_rate IS NULL OR hourly_rate >= 0', name='check_hourly_rate_non_negative'),
    )

    def __repr__(self):
        return f"<Employee {self.full_name}>"
   
    def get_full_address(self):
        """الحصول على العنوان الكامل للموظف"""
        return self.residence or "لا يوجد عنوان مسجل"
    
    def get_age(self):
        """حساب عمر الموظف"""
        if self.date_of_birth:
            from datetime import datetime
            today = datetime.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None
    
    def has_user_account(self):
        """التحقق مما إذا كان للموظف حساب مستخدم"""
        return self.user_account is not None
    
    def get_job_title(self):
        """الحصول على المسمى الوظيفي"""
        if hasattr(self, 'job_title') and self.job_title:
            return self.job_title.title_name
        return None
    
    def get_user_type(self):
        """الحصول على نوع المستخدم المرتبط بالموظف"""
        if self.has_user_account():
            return self.user_account.user_type
        return None
    
    def is_department_head(self):
        """التحقق مما إذا كان الموظف رئيس قسم"""
        return self.has_user_account() and self.user_account.is_department_head()
    
    def is_branch_head(self):
        """التحقق مما إذا كان الموظف رئيس فرع"""
        return self.has_user_account() and self.user_account.is_branch_head()
    
    def calculate_overtime_pay(self, overtime_hours):
        """حساب أجر الساعات الإضافية"""
        if not self.hourly_rate or overtime_hours <= 0:
            return 0
        return float(self.hourly_rate) * float(self.overtime_multiplier) * overtime_hours
    
    def calculate_daily_overtime_pay(self, overtime_days):
        """حساب أجر الأيام الإضافية"""
        if not self.daily_rate or overtime_days <= 0:
            return 0
        return float(self.daily_rate) * float(self.overtime_multiplier) * overtime_days
    
    def auto_calculate_rates(self):
        """حساب تلقائي لسعر اليوم والساعة بناءً على الراتب الأساسي"""
        if self.salary:
            # افتراض 30 يوم في الشهر و 8 ساعات في اليوم
            monthly_salary = float(self.salary)
            self.daily_rate = monthly_salary / 30
            self.hourly_rate = self.daily_rate / 8
            return True
        return False

    def generate_barcode(self, upload_folder=None, base_url="http://localhost:5000"):
        """توليد QR Code فريد للموظف وحفظه كصورة

        Args:
            upload_folder: مجلد الرفع لحفظ صورة QR Code
            base_url: رابط الموقع الأساسي (يمكن تغييره لاحقاً)

        Returns:
            str: الباركود النصي الفريد
        """
        import uuid
        import os

        if not self.barcode:
            # توليد باركود فريد باستخدام fingerprint_id + UUID
            self.barcode = f"EMP-{self.fingerprint_id}-{uuid.uuid4().hex[:8].upper()}"

        # توليد صورة QR Code إذا تم توفير مجلد الحفظ
        if upload_folder:
            try:
                import qrcode
                from PIL import Image

                # إنشاء مجلد QR Codes إذا لم يكن موجوداً
                barcode_folder = os.path.join(upload_folder, 'barcodes')
                if not os.path.exists(barcode_folder):
                    os.makedirs(barcode_folder)

                # إنشاء رابط URL للموظف
                # سيتم استخدام id الموظف بعد حفظه في قاعدة البيانات
                # في حالة الموظف الجديد، سنستخدم fingerprint_id مؤقتاً
                employee_url = f"{base_url}/employee/{self.id if self.id else self.fingerprint_id}"

                # توليد QR Code
                qr = qrcode.QRCode(
                    version=1,  # حجم QR Code (1-40)
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,  # حجم كل مربع في QR Code
                    border=4,  # حجم الإطار حول QR Code
                )
                qr.add_data(employee_url)
                qr.make(fit=True)

                # إنشاء صورة QR Code
                qr_image = qr.make_image(fill_color="black", back_color="white")

                # حفظ QR Code كصورة
                barcode_filename = f"{self.fingerprint_id}_qrcode.png"
                barcode_path = os.path.join(barcode_folder, barcode_filename)
                qr_image.save(barcode_path)

                # تخزين المسار النسبي
                self.barcode_image_path = f"/uploads/barcodes/{barcode_filename}"

            except ImportError:
                # في حالة عدم تثبيت المكتبة، نترك barcode_image_path فارغاً
                print("Warning: qrcode library not installed. QR Code image not generated.")
                pass
            except Exception as e:
                print(f"Error generating QR Code: {str(e)}")
                pass

        return self.barcode

    @classmethod
    def get_by_barcode(cls, barcode):
        """البحث عن موظف باستخدام الباركود"""
        return cls.query.filter_by(barcode=barcode).first()