from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.db_models import Event

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/events/new', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        event_date = request.form.get('event_date')
        location = request.form.get('location')
        capacity = request.form.get('capacity')
        
        if not title or not event_date or not location or not capacity:
            flash("請填寫所有必填欄位", "danger")
            return render_template('create.html')
            
        try:
            Event.create(title, description, event_date, location, int(capacity))
            flash("活動建立成功！", "success")
            return redirect(url_for('events.index'))
        except Exception as e:
            flash(f"建立活動時發生錯誤: {str(e)}", "danger")
            
    return render_template('create.html')
