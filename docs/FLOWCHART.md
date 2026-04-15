# 流程圖文件 (Flowchart) - 活動報名系統

本文件根據 PRD 與系統架構文件，梳理系統的使用者操作流程、系統背後的資料互動邏輯，並對應到開發時會用到的路徑清單。

## 1. 使用者流程圖 (User Flow)

以下展示兩類主要使用者（**活動主辦人**與**參加學生**）在系統中的操作路徑。

```mermaid
flowchart LR
    Start([進入網站首頁]) --> UserType{我是什麼角色？}
    
    %% 主辦人流程
    UserType -->|活動主辦人| AdminAction[點擊「建立活動」]
    AdminAction --> AdminForm[填寫活動資訊與名額]
    AdminForm --> AdminSubmit{資料無誤送出?}
    AdminSubmit -->|Yes| AdminSuccess([顯示建立成功並返回首頁])
    AdminSubmit -->|No| AdminForm
    
    %% 學生流程
    UserType -->|參加學生| StudentAction[瀏覽活動清單]
    StudentAction --> StudentChoice{要做什麼？}
    
    %% 學生查詢進度
    StudentChoice -->|查詢進度| QueryNav[點擊「進度查詢」]
    QueryNav --> QueryForm[輸入學號]
    QueryForm --> QueryShow([顯示報名狀態：成功/候補])
    
    %% 學生報名
    StudentChoice -->|參加活動| EventDetail[點擊「活動詳情」]
    EventDetail --> RegForm[填寫報名表單]
    RegForm --> RegSubmit{資料無誤送出?}
    RegSubmit -->|Yes| RegResult([顯示報名結果：成功/候補])
    RegSubmit -->|No| RegForm
```

## 2. 系統序列圖 (Sequence Diagram)

以下以最核心的「**學生送出線上報名表**」功能為例，展示前端瀏覽器、Flask 後端與資料庫之間的互動序列與自動候補判斷。

```mermaid
sequenceDiagram
    actor Student as 學生 (User)
    participant Browser as 瀏覽器 (Front-end)
    participant Flask as Flask Route (Controller)
    participant Model as Event/Registration 模型
    participant DB as SQLite 資料庫

    Student->>Browser: 填寫資料並點擊「送出報名」
    Browser->>Flask: POST /event/{id}/register (傳送 Form Data)
    Flask->>Model: 呼叫報名邏輯 (傳遞驗證後的資料)
    
    %% DB 互動區塊
    rect rgb(240, 240, 240)
        Model->>DB: 查詢該活動目前「已報名人數」與「名額上限」
        DB-->>Model: 回傳人數數據
        alt 已報名人數 < 名額上限
            Model->>DB: 新增報名紀錄 (Status = 報名成功)
            DB-->>Model: 寫入完成
        else 已報名人數 >= 名額上限
            Model->>DB: 新增報名紀錄 (Status = 候補中)
            DB-->>Model: 寫入完成
        end
    end
    
    Model-->>Flask: 回傳報名結果 (成功 / 候補)
    Flask-->>Browser: 重定向 (Redirect) 到結果頁面並帶上訊息
    Browser-->>Student: 顯示「報名成功」或「候補中」畫面
```

## 3. 功能清單與路徑對照表

總結上述的所有功能操作，並對應到 Flask 的路由設計：

| 功能名稱 | HTTP 方法 | URL 路徑 (Route) | 負責渲染的視圖 (Template) | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁/活動清單** | `GET` | `/` | `index.html` | 顯示所有開放中與結束的活動 |
| **建立活動專頁 (表單)** | `GET` | `/admin/events/new` | `create.html` | 顯示主辦人建立活動的表單頁面 |
| **送出建立活動** | `POST` | `/admin/events/new` | (Redirect) | 接收主辦人表單資料，寫入資料記錄 |
| **活動詳細內容** | `GET` | `/event/<int:id>` | `event.html` | 顯示特定活動詳細資訊及下方報名表單 |
| **送出活動報名** | `POST` | `/event/<int:id>/register` | (Redirect) | 處理學生報名資料，判定並處理候補邏輯 |
| **報名進度查詢入口** | `GET` | `/status` | `search.html` | 顯示「輸入學號查詢」的頁面 |
| **顯示進度查詢結果** | `POST` 或 `GET` | `/status` | `search.html` | 驗證學號後查詢名下所有報名狀態並顯示在同頁面下方 |
