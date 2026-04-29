# 路由與頁面設計文件 (Routes) - 活動報名系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/活動清單** | `GET` | `/` | `index.html` | 顯示所有開放中與結束的活動列表 |
| **活動詳細內容** | `GET` | `/event/<int:id>` | `event.html` | 顯示特定活動的詳細資訊與報名表單 |
| **送出活動報名** | `POST` | `/event/<int:id>/register` | — (Redirect) | 處理學生報名，根據剩餘名額判定「成功」或「候補」，並重導至結果頁 |
| **建立活動專頁** | `GET` | `/admin/events/new` | `create.html` | 顯示主辦人建立新活動的表單 |
| **送出建立活動** | `POST` | `/admin/events/new` | — (Redirect) | 接收主辦人表單資料並寫入 DB，完成後重導回首頁 |
| **報名進度查詢** | `GET` | `/status` | `search.html` | 顯示學號查詢輸入框 |
| **進度查詢結果** | `POST` | `/status` | `search.html` | 接收學號，查詢所有名下報名狀態，並將結果傳遞給同一個頁面進行渲染 |

---

## 2. 每個路由的詳細說明

### `events.py` (公開活動相關)

#### 1. `GET /` (首頁/活動清單)
- **輸入**: 無
- **處理邏輯**: 呼叫 `Event.get_all()` 取得所有活動紀錄。
- **輸出**: 渲染 `index.html`，並傳遞 `events` 資料清單。
- **錯誤處理**: 若無資料顯示「目前沒有活動」等提示訊息。

#### 2. `GET /event/<int:id>` (活動詳細內容)
- **輸入**: URL 參數 `id` (活動 ID)
- **處理邏輯**: 呼叫 `Event.get_by_id(id)` 取得指定活動的詳細資料。
- **輸出**: 渲染 `event.html`，傳遞 `event` 資料。
- **錯誤處理**: 若查無此活動，回傳 404 頁面或重導向至首頁帶有錯誤訊息。

---

### `user.py` (使用者報名與狀態相關)

#### 3. `POST /event/<int:id>/register` (送出活動報名)
- **輸入**: URL 參數 `id` (活動 ID)，表單欄位 (`student_id`, `name`, `phone`)
- **處理邏輯**: 
  - 呼叫 `Registration.create(event_id, student_id, name, phone)`。
  - Model 內會判定該活動名額 `capacity` 是否已滿。
  - 若已滿則狀態記為「候補中」，未滿則為「成功」。
- **輸出**: 使用 `flash()` 顯示成功或候補訊息，重導向至活動詳細頁 (`/event/<int:id>`)。
- **錯誤處理**: 表單驗證失敗或資料庫寫入錯誤時，顯示錯誤訊息並重導回報名頁。

#### 4. `GET /status` (報名進度查詢入口)
- **輸入**: 無
- **處理邏輯**: 單純顯示查詢表單。
- **輸出**: 渲染 `search.html`。
- **錯誤處理**: 無。

#### 5. `POST /status` (顯示進度查詢結果)
- **輸入**: 表單欄位 (`student_id`)
- **處理邏輯**: 呼叫 `Registration.get_by_student(student_id)` 取得與該學號關聯的所有報名紀錄（包含活動名稱與報名狀態）。
- **輸出**: 渲染 `search.html`，並傳遞查詢結果清單。若無結果，傳遞相應提示。
- **錯誤處理**: 若未輸入學號，提示「請輸入學號」。

---

### `admin.py` (主辦方管理相關)

#### 6. `GET /admin/events/new` (建立活動專頁)
- **輸入**: 無
- **處理邏輯**: 顯示建立活動表單。
- **輸出**: 渲染 `create.html`。
- **錯誤處理**: 無。

#### 7. `POST /admin/events/new` (送出建立活動)
- **輸入**: 表單欄位 (`title`, `description`, `event_date`, `location`, `capacity`)
- **處理邏輯**: 呼叫 `Event.create(...)` 將資料寫入資料庫。
- **輸出**: 建立成功後，使用 `flash()` 顯示成功訊息，並重導向至首頁 (`/`)。
- **錯誤處理**: 若必填欄位空白，顯示錯誤並返回原表單頁面 (`create.html`) 重新填寫。

---

## 3. Jinja2 模板清單

| 模板檔案 | 繼承自 | 說明 |
| :--- | :--- | :--- |
| `base.html` | — | 基礎版型，包含 HTML 架構、導覽列 (Navigation) 與頁尾，以及 Flask Flash 訊息顯示區塊。 |
| `index.html` | `base.html` | 首頁，負責條列顯示所有活動卡片/列表。 |
| `event.html` | `base.html` | 活動內頁，上方顯示活動詳細資訊，下方顯示給學生填寫的報名表單。 |
| `create.html`| `base.html` | 新增活動頁面，包含標題、日期、地點、人數上限等輸入框。 |
| `search.html`| `base.html` | 查詢進度頁面，上方是學號輸入框，下方顯示該學號的所有報名狀態結果。 |

---

## 4. 路由骨架程式碼

已在 `app/routes/` 下建立三個 Blueprint 檔案：
- `events.py`
- `user.py`
- `admin.py`

詳細程式碼骨架請參考各 `.py` 檔案。
