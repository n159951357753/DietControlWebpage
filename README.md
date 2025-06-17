
# 🍎 Calorie Tracker Webpage

> 一款簡潔直觀的熱量及營養追蹤網站，幫助使用者更有效管理每日飲食。本專案為 C# DietControlWebpage 專案中的 `calorie_tracker` 模組。

---

## 🎯 專案簡介

`calorie_tracker` 是一個基於 Web 的飲食紀錄工具，使用者可以：
- 新增每日餐點與熱量紀錄
- 查看每日總熱量
- 分析三大營養素（蛋白質、碳水化合物、脂肪）比例
- 篩選歷史紀錄（依日期區間）

適合追求健康管理、減重或營養均衡需求的使用者。

---

## 🧩 系統特色

- ✅ 使用者註冊/登入（可選社群登入）
- 🥗 新增 / 編輯 / 刪除餐點紀錄
- 📊 顯示每日熱量總和與營養比例
- 📅 支援按日期區間快速檢視歷史
- 📱 響應式設計，支援手機與桌面瀏覽器
- 📂 前後端分離架構：後端為 API，前端為 SPA 界面（如 Vue 或 React）

---

## 📸 預覽畫面

![主頁面預覽](screenshots/home.png)
*桌面版本：顯示熱量總和與營養比例圖*

![新增紀錄頁面](screenshots/add_entry.png)
*可輸入餐點名稱、份量、熱量與營養素*

![歷史紀錄頁](screenshots/history.png)
*按日期區間查看歷史紀錄與統計數字*

---

## ⚙️ 技術架構

```
[前端 SPA]
Vue.js / React / HTML+CSS + Axios
       ↓
[後端 RESTful API]
Node.js / Python(Django) / ASP.NET Core
       ↓
[資料庫]
MySQL / PostgreSQL / SQLite
```

---

## 🚀 快速開始

### 前提條件
- Node.js (v16+)
- Python 3.9+ 或 .NET 6+
- 資料庫（MySQL、PostgreSQL 或 SQLite）

### 一、後端部署

```bash
cd calorie_tracker/backend
npm install            # 或 pip install -r requirements.txt
npm run migrate        # or python manage.py migrate
npm run seed           # 初始資料建立
npm start              # 啟動 API 伺服器
```

### 二、前端部署

```bash
cd calorie_tracker/frontend
npm install
npm run serve          # 本機開啟 http://localhost:8080
```

### 三、使用網站
前後端都啟動後，打開 `http://localhost:8080` 開始使用。

---

## 🗃️ 資料模式（範例）

**Entry 餐點紀錄**

| 欄位        | 類型      | 描述               |
|------------|----------|--------------------|
| id         | integer  | 主鍵               |
| user_id    | integer  | 所屬使用者 ID      |
| date       | date     | 餐點日期           |
| name       | string   | 餐點名稱           |
| calories   | integer  | 熱量（大卡）       |
| protein    | float    | 蛋白質（克）       |
| carbs      | float    | 碳水化合物（克）   |
| fat        | float    | 脂肪（克）         |

---

## 🧪 測試

```bash
cd backend
npm test                # 或 pytest/test runner
```

前端可使用 Jest、Mocha、Cypress 等工具進行單元與端對端測試。

---

## 📝 常見問題

### Q：如何新增營養素記錄？
A：前端表單輸入後，前端會發送 `POST /api/entries/` 請求，將資料送到後端儲存。

### Q：為什麼看不到歷史？
A：請確認你是否登入，以及查詢日期區間。目前尚未支援匿名存取。

---

## 🔭 未來計畫

- 📈 加入圖表分析：每日、每週、每月趨勢視覺化
- 🧾 增加 CSV 匯出功能
- 🤝 與第三方食品資料庫整合
- 🔐 引入 JWT + OAuth 強化安全性

---

## ❤️ 如何貢獻

1. Fork 本儲存庫並建立 branch
2. 提交 PR（Include 說明與截圖）
3. 經過 code review 即可合併

---

## 📛 授權條款

MIT © 2025 DietControl 開發團隊  
詳細內容請見 `LICENSE` 檔案。
