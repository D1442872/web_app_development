from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/event/<int:id>/register', methods=['POST'])
def register(id):
    """
    送出活動報名
    
    處理學生報名資料，判斷是否額滿，若額滿則設為「候補中」，否則「成功」。
    完成後使用 flash() 提示訊息並重導向。
    
    參數：
        id (int): 活動的唯一識別碼
        
    表單參數：
        student_id (str): 學號
        name (str): 姓名
        phone (str): 連絡電話
        
    回傳：
        重導向回活動詳細頁面 (/event/<id>)
    """
    pass

@user_bp.route('/status', methods=['GET', 'POST'])
def status_search():
    """
    報名進度查詢
    
    GET: 顯示輸入學號的查詢表單。
    POST: 接收學號，查詢該學號所有報名紀錄與狀態並顯示。
    
    表單參數 (POST):
        student_id (str): 學號
        
    回傳：
        渲染 search.html。如果是 POST，則傳遞 registrations 查詢結果
    """
    pass
