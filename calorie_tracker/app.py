from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Food, DietRecord
from forms import LoginForm, RegisterForm, FoodForm, DietRecordForm, EditDietRecordForm, UpdateProfileForm, UpdateAccountForm
from datetime import datetime, date
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'
if getattr(sys, 'frozen', False):
    # 如果是 PyInstaller 打包後執行
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # 平常執行
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
# 自動確保 instance 資料夾存在
instance_dir = os.path.join(BASE_DIR, 'instance')
os.makedirs(instance_dir, exist_ok=True)

# 設定資料庫路徑
db_path = os.path.join(BASE_DIR, 'instance', 'calories.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/calories.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('此帳號已存在，請使用其他帳號')
            return render_template('register.html', form=form)
        
        hashed_pw = generate_password_hash(form.password.data)
        user = User(
            username=form.username.data, 
            password_hash=hashed_pw,
            name=form.name.data,
            birthdate=form.birthdate.data,
            gender=form.gender.data,
            height=form.height.data,
            weight=form.weight.data
        )
        db.session.add(user)
        db.session.commit()
        flash('註冊成功！')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('overview'))
        flash('登入失敗，請檢查帳號或密碼')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/overview')
@login_required
def overview():
    # 取得今日紀錄
    today_start = datetime.combine(date.today(), datetime.min.time())
    today_end = datetime.combine(date.today(), datetime.max.time())

    today_records = DietRecord.query.filter(
        DietRecord.user_id == current_user.id,
        DietRecord.timestamp >= today_start,
        DietRecord.timestamp <= today_end
    ).all()

    total_calories = sum([r.calories or 0 for r in today_records])

    # 計算年齡
    today = date.today()
    birthdate = current_user.birthdate
    if birthdate:
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    else:
        age = None

    # BMI 計算
    if current_user.height and current_user.weight:
        height_m = current_user.height / 100
        bmi = round(current_user.weight / (height_m ** 2), 2)
        suggested_bmi = 21
        suggested_weight = round(suggested_bmi * (height_m ** 2), 1)
        weight_diff = round(suggested_weight - current_user.weight, 1)
    else:
        bmi = None
        suggested_bmi = None
        suggested_weight = None
        weight_diff = None

    # 建議卡路里（Mifflin-St Jeor）
    if current_user.gender and current_user.height and current_user.weight and age is not None:
        if current_user.gender == '男':
            bmr = 10 * current_user.weight + 6.25 * current_user.height - 5 * age + 5
        else:
            bmr = 10 * current_user.weight + 6.25 * current_user.height - 5 * age - 161
        suggested_calories = round(bmr)
    else:
        suggested_calories = None

    # 應增減攝取卡路里
    if bmi:
        if bmi > 24:
            calorie_adjustment = -500
        elif bmi < 18.5:
            calorie_adjustment = 500
        else:
            calorie_adjustment = 0
    else:
        calorie_adjustment = None
        
        
    # 建議飲水量
    if current_user.weight:
        suggested_water = int(current_user.weight * 30)  # ml
    else:
        suggested_water = None

    # BMI 分級
    bmi_category = get_bmi_category(bmi) if bmi else None

    return render_template(
        'overview.html',
        records=today_records,
        total_calories=total_calories,
        suggested_calories=suggested_calories,
        calorie_adjustment=calorie_adjustment,
        bmi=bmi,
        suggested_bmi=suggested_bmi,
        suggested_weight=suggested_weight,
        weight_diff=weight_diff,
        age=age,
        bmi_category=bmi_category,
        suggested_water=suggested_water
    )

@app.route('/diet_manage', methods=['GET', 'POST'])
@login_required
def diet_manage():
    form = DietRecordForm()
    edit_form = EditDietRecordForm()
    
    if form.validate_on_submit():
        record = DietRecord(
            user_id=current_user.id,
            timestamp=form.timestamp.data,
            food_name=form.food_name.data,
            food_type=form.food_type.data,
            calories=form.calories.data,
            location=form.location.data,
            notes=form.notes.data
        )
        db.session.add(record)
        if form.add_to_food.data:
            # Check if food already exists
            existing = Food.query.filter_by(name=form.food_name.data).first()
            if not existing:
                food = Food(
                    name=form.food_name.data,
                    type=form.food_type.data,
                    calories=form.calories.data,
                    location=form.location.data
                )
                db.session.add(food)
        db.session.commit()
        flash('新增紀錄完成！')
    records = DietRecord.query.filter_by(user_id=current_user.id).order_by(DietRecord.timestamp.desc()).all()
    return render_template('diet_manage.html', form=form, edit_form=edit_form, records=records)

@app.route('/edit_record/<int:record_id>', methods=['POST'])
@login_required
def edit_record(record_id):
    record = DietRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        flash('你沒有權限修改此紀錄')
        return redirect(url_for('diet_manage'))

    form = EditDietRecordForm()
    if form.validate_on_submit():
        record.timestamp = form.timestamp.data
        record.food_name = form.food_name.data
        record.food_type = form.food_type.data
        record.calories = form.calories.data
        record.location = form.location.data
        record.notes = form.notes.data
        db.session.commit()
        flash(f'紀錄修改完成！ {record}')
    else:
        flash('資料驗證失敗，請確認欄位格式')
    return redirect(url_for('diet_manage'))

@app.route('/delete_record/<int:record_id>', methods=['POST'])
@login_required
def delete_record(record_id):
    record = DietRecord.query.get_or_404(record_id)
    if record.user_id != current_user.id:
        flash('你沒有權限刪除此紀錄')
        return redirect(url_for('diet_manage'))
    
    db.session.delete(record)
    db.session.commit()
    flash('已刪除紀錄')
    return redirect(url_for('diet_manage'))


@app.route('/food_manage', methods=['GET', 'POST'])
@login_required
def food_manage():
    form = FoodForm()
    foods = Food.query.all()
    if form.validate_on_submit():
        food = Food(
            name=form.name.data,
            type=form.type.data,
            calories=form.calories.data,
            location=form.location.data
        )
        db.session.add(food)
        db.session.commit()
        flash('新增食品完成！')
        return redirect(url_for('food_manage'))
    return render_template('food_manage.html', form=form, foods=foods)

@app.route('/history')
@login_required
def history():
    records = DietRecord.query.filter_by(user_id=current_user.id).order_by(DietRecord.timestamp.desc()).all()
    return render_template('history.html', records=records)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    profile_form = UpdateProfileForm(obj=current_user)
    account_form = UpdateAccountForm()

    # 判斷是更新個人資料的表單送出
    if profile_form.profile_submit.data and profile_form.validate_on_submit():
        current_user.name = profile_form.name.data
        current_user.birthdate = profile_form.birthdate.data
        current_user.gender = profile_form.gender.data
        current_user.height = profile_form.height.data
        current_user.weight = profile_form.weight.data
        db.session.commit()
        flash('個人資料已更新！', 'success')
        return redirect(url_for('settings'))

    # 判斷是更新帳號密碼的表單送出
    if account_form.account_submit.data and account_form.validate_on_submit():
        if not check_password_hash(current_user.password_hash, account_form.current_password.data):
            flash('原密碼錯誤，請重新輸入', 'danger')
            return redirect(url_for('settings'))

        updated = False  # 記錄是否有做任何更新

        # 更新帳號
        if account_form.new_username.data:
            existing_user = User.query.filter_by(username=account_form.new_username.data).first()
            if existing_user and existing_user.id != current_user.id:
                flash('帳號已被使用', 'danger')
            else:
                current_user.username = account_form.new_username.data
                updated = True

        # 更新密碼
        if account_form.new_password.data:
            if not account_form.confirm_new_password.data:
                flash('請填入確認密碼', 'danger')
            elif account_form.new_password.data != account_form.confirm_new_password.data:
                flash('新密碼與確認密碼不一致', 'danger')
            else:
                current_user.password_hash = generate_password_hash(account_form.new_password.data)
                updated = True

        if updated:
            db.session.commit()
            flash('帳號/密碼已更新！', 'success')
        else:
            flash('沒有變更任何資料', 'info')

        return redirect(url_for('settings'))

    return render_template('settings.html', profile_form=profile_form, account_form=account_form)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return '過輕'
    elif 18.5 <= bmi < 24:
        return '正常'
    elif 24 <= bmi < 27:
        return '過重'
    elif 27 <= bmi < 30:
        return '輕度肥胖'
    elif 30 <= bmi < 35:
        return '中度肥胖'
    else:
        return '重度肥胖'


if __name__ == '__main__':
    # 自動檢查資料庫是否存在
    if not os.path.exists(db_path):
        print("尚未檢測到資料庫，正在建立 calories.db...")
        with app.app_context():
            db.create_all()
        print("✅ 資料庫已建立完成！")
    else:
        print("✅ 已檢測到資料庫 calories.db")

    app.run(debug=True)