from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/events/new', methods=['GET', 'POST'])
def create_event():
    """
    建立活動專頁
    
    GET: 顯示建立活動的表單。
    POST: 接收表單並建立新活動寫入資料庫。
    
    表單參數 (POST):
        title (str): 活動名稱
        description (str): 活動描述
        event_date (str): 活動時間
        location (str): 活動地點
        capacity (int): 名額上限
        
    回傳：
        GET: 渲染 create.html
        POST: 成功後重導向至首頁 (/)，並顯示 flash() 提示。
    """
    pass
