from flask import Blueprint

events_bp = Blueprint('events', __name__)

@events_bp.route('/', methods=['GET'])
def index():
    """
    首頁/活動清單
    
    取得所有活動並顯示在頁面上。
    
    回傳：
        渲染 index.html，帶有 events 資料
    """
    pass

@events_bp.route('/event/<int:id>', methods=['GET'])
def event_detail(id):
    """
    活動詳細內容
    
    根據給定的活動 id 取得活動資料，並顯示該活動詳情與報名表單。
    
    參數：
        id (int): 活動的唯一識別碼
        
    回傳：
        渲染 event.html，帶有 event 資料
    """
    pass
