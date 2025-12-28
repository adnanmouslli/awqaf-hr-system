from app import db, create_app
from flask_cors import CORS
from app.routes.auth import create_super_admin
import socket

# إعداد timeout عام للنظام
socket.setdefaulttimeout(300)  # 5 دقائق

app = create_app()
CORS(app)

# إعدادات Flask للعمليات الطويلة
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
app.config['PERMANENT_SESSION_LIFETIME'] = 300

# زيادة حد الطلبات الكبيرة
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_super_admin()
    
    # الطريقة الصحيحة لـ Flask Development Server
    app.run(host='0.0.0.0', port=3000, debug=True, threaded=True)