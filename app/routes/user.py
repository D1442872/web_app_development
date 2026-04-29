from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.db_models import Registration

user_bp = Blueprint('user', __name__)

@user_bp.route('/event/<int:id>/register', methods=['POST'])
def register(id):
    student_id = request.form.get('student_id')
    name = request.form.get('name')
    phone = request.form.get('phone')
    
    if not student_id or not name or not phone:
        flash("請填寫所有報名資訊", "danger")
        return redirect(url_for('events.event_detail', id=id))
        
    try:
        reg_id, status = Registration.create(id, student_id, name, phone)
        if status == '成功':
            flash("報名成功！", "success")
        else:
            flash("活動已額滿，您已自動排入候補名單！", "warning")
    except Exception as e:
        flash(f"報名發生錯誤: {str(e)}", "danger")
        
    return redirect(url_for('events.event_detail', id=id))

@user_bp.route('/status', methods=['GET', 'POST'])
def status_search():
    registrations = None
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if not student_id:
            flash("請輸入學號", "warning")
        else:
            registrations = Registration.get_by_student(student_id)
            if not registrations:
                flash("查無此學號的報名紀錄", "info")
                
    return render_template('search.html', registrations=registrations)
