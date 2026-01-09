"""
Flask Routes for ID Card Generation
مسارات API لإنشاء البطاقات التعريفية
"""

from flask import Blueprint, request, jsonify, current_app, render_template, url_for
from app import db
from app.models.employee import Employee
from app.models.job_title import JobTitle
from app.utils import token_required
import os

id_card_bp = Blueprint('id_card', __name__)


def get_file_url(relative_path, base_url=None):
    """
    تحويل المسار النسبي إلى URL كامل
    """
    if not relative_path:
        return None

    if base_url is None:
        base_url = request.host_url.rstrip('/')

    # إزالة /uploads/ من البداية إذا كان موجوداً
    clean_path = relative_path.replace('/uploads/', '').replace('\\', '/')

    return f"{base_url}/uploads/{clean_path}"


@id_card_bp.route('/api/employees/<int:emp_id>/id-card/front', methods=['GET'])
@token_required
def get_id_card_front(current_user, emp_id):
    """
    الحصول على الوجه الأمامي للبطاقة التعريفية كـ HTML

    Returns:
        HTML: صفحة HTML للوجه الأمامي للبطاقة
    """
    try:
        employee = Employee.query.get(emp_id)

        if not employee:
            return "<h1 style='text-align:center; color:red; font-family:Cairo'>الموظف غير موجود</h1>", 404

        # تحضير بيانات الموظف
        job_title_name = None
        if employee.position:
            job_title = JobTitle.query.get(employee.position)
            if job_title:
                job_title_name = job_title.title_name

        # تحديد نوع الموظف بالعربي
        employee_type_ar = 'موظف دائم' if employee.employee_type == 'permanent' else 'موظف مؤقت'

        # تحضير الـ URLs للصور
        base_url = request.host_url.rstrip('/')
        photo_url = get_file_url(employee.photo_path, base_url) if employee.photo_path else None
        # logo_url = get_file_url(employee.logo_path, base_url) if employee.logo_path else None

        # صورة شعار الجمهورية (يمكن تخزينها في مجلد ثابت)
        republic_logo_url = f"{base_url}/uploads/Syrian_Arab_Republic.png"
        logo_url = f"{base_url}/uploads/logo.png"

        # تحضير تاريخ ومكان الولادة
        birth_date_str = employee.date_of_birth.strftime('%Y/%m/%d') if employee.date_of_birth else ''
        birth_place_str = employee.place_of_birth or ''

        # دمج تاريخ ومكان الولادة
        if birth_date_str and birth_place_str:
            birth_date_place = f"{birth_place_str} - {birth_date_str}"
        elif birth_date_str:
            birth_date_place = birth_date_str
        elif birth_place_str:
            birth_date_place = birth_place_str
        else:
            birth_date_place = 'غير محدد'

        # عرض القالب
        return render_template(
            'id_card_front.html',
            fingerprint_id=employee.fingerprint_id,
            full_name=employee.full_name,
            employee_type=employee_type_ar,
            position=job_title_name or 'غير محدد',
            national_id=employee.national_id or 'غير محدد',
            birth_date_place=birth_date_place,
            photo_url=photo_url,
            logo_url=logo_url,
            republic_logo_url=republic_logo_url,
            ministry_name='وزارة الأوقاف',
            ministry_location='مديرية أوقاف حلب'
        ), 200

    except Exception as e:
        print(f"خطأ في إنشاء الوجه الأمامي للبطاقة: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"<h1 style='color:red'>خطأ: {str(e)}</h1>", 500


@id_card_bp.route('/api/employees/<int:emp_id>/id-card/back', methods=['GET'])
@token_required
def get_id_card_back(current_user, emp_id):
    """
    الحصول على الوجه الخلفي للبطاقة التعريفية كـ HTML

    Returns:
        HTML: صفحة HTML للوجه الخلفي للبطاقة
    """
    try:
        employee = Employee.query.get(emp_id)

        if not employee:
            return "<h1 style='text-align:center; color:red; font-family:Cairo'>الموظف غير موجود</h1>", 404

        # تحضير الـ URLs للصور
        base_url = request.host_url.rstrip('/')
        # logo_url = get_file_url(employee.logo_path, base_url) if employee.logo_path else None
        qr_code_url = get_file_url(employee.barcode_image_path, base_url) if employee.barcode_image_path else None

        # صورة شعار الجمهورية
        republic_logo_url = f"{base_url}/uploads/Syrian_Arab_Republic.png"
        logo_url = f"{base_url}/uploads/logo.png"

        # عرض القالب
        return render_template(
            'id_card_back.html',
            qr_code_url=qr_code_url,
            logo_url=logo_url,
            republic_logo_url=republic_logo_url,
            ministry_name='وزارة الأوقاف',
            workplace=employee.work_location or 'غير محدد',
            department=employee.division_section or 'غير محدد',
            expiry_date=employee.card_expiry_date.strftime('%Y/%m/%d') if employee.card_expiry_date else 'غير محدد'
        ), 200

    except Exception as e:
        print(f"خطأ في إنشاء الوجه الخلفي للبطاقة: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"<h1 style='color:red'>خطأ: {str(e)}</h1>", 500
