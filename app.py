from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'iraq_tech_2024'

# إعداد قاعدة البيانات (سيتم إنشاء ملف باسم devices.db)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///devices.db'
db = SQLAlchemy(app)

# تعريف جدول الأجهزة في قاعدة البيانات
class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.String(50))
    battery = db.Column(db.String(20))
    memory = db.Column(db.String(20))
    ram = db.Column(db.String(20))
    image_url = db.Column(db.String(500))

# بيانات المشرفين الثلاثة
ADMINS = {
    "admin1": "1234",
    "admin2": "5678",
    "admin3": "9000"
}

@app.route('/')
def index():
    devices = Device.query.order_by(Device.id.desc()).all()
    return render_template('index.html', devices=devices)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user in ADMINS and ADMINS[user] == pw:
            session['logged_in'] = True
            session['user'] = user
            return redirect(url_for('admin_panel'))
        flash('خطأ في اسم المستخدم أو كلمة المرور')
    return render_template('login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_device = Device(
            name=request.form.get('name'),
            price=request.form.get('price'),
            battery=request.form.get('battery'),
            memory=request.form.get('memory'),
            ram=request.form.get('ram'),
            image_url=request.form.get('image_url')
        )
        db.session.add(new_device)
        db.session.commit()
        return redirect(url_for('index'))
    
    return render_template('admin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # إنشاء قاعدة البيانات عند أول تشغيل
    app.run(debug=True)
