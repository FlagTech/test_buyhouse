# 🏠 買房vs租房分析系統

一個基於 Flask + Dash 的台灣房地產分析工具，提供全台22個縣市的房價租金趨勢分析和投資決策輔助。

## ✨ 功能特色

### 📊 房價地圖頁面
- **互動式台灣地圖**：點擊各縣市查看即時房價資訊
- **趨勢分析圖表**：顯示房價、租金、物價指數等多維度趨勢
- **長條圖統計**：呈現各縣市房價收入比、平均月薪等數據
- **篩選功能**：支援房價、租金、全台平均等多種數據切換

### 🏡 買房vs租房比較頁面
- **圓餅圖分析**：比較買房vs租房的每月支出分配
- **30年資產累積圖**：視覺化長期資產變化趨勢
- **個人化參數設定**：可調整收入、消費、投資報酬率等參數
- **即時計算**：動態更新房屋總價、頭期款、貸款月付金等

## 🚀 技術架構

- **後端框架**：Flask + Dash
- **前端技術**：Bootstrap 5, jQuery, Plotly.js
- **資料視覺化**：Plotly (Python), D3.js
- **資料格式**：CSV (房價、租金歷史資料)
- **Python環境管理**：uv

## 📋 系統需求

- Python 3.8+
- uv (Python套件管理工具)

## 🔧 安裝與執行

### 1. 克隆專案
```bash
git clone -b update_data https://github.com/FlagTech/test_buyhouse.git
cd test_buyhouse
```

### 2. 初始化環境並執行
```bash
uv run wsgi.py
```

### 3. 瀏覽器訪問
開啟瀏覽器前往 `http://localhost:5000`

## 📈 資料說明

### 資料來源
- **房價資料**：內政部不動產交易實價登錄資料
- **租金資料**：內政部租金實價登錄資料
- **時間範圍**：105Q1 - 114Q2 (2016-2025)
- **地區涵蓋**：全台22個縣市

### 資料結構
```
app/static/assets/
├── date_data.csv          # 整合的時間序列資料
├── city_p.csv             # 各縣市房價資料
├── city_r.csv             # 各縣市租金資料
├── scale.csv              # 縣市統計資料
└── data/                  # 原始季度資料
    ├── 105Q1/
    ├── 105Q2/
    └── ...
```

## 🏗️ 專案結構

```
test_buyhouse/
├── app/
│   ├── dash_apps/          # Dash應用模組
│   │   ├── buyorrent.py    # 買房vs租房比較圖表
│   │   ├── city.py         # 城市資料處理
│   │   ├── Payment.py      # 付款計算邏輯
│   │   ├── plt_trend.py    # 趨勢圖表生成
│   │   ├── plt_income.py   # 收入分析圖表
│   │   └── readata.py      # 資料讀取處理
│   ├── static/             # 靜態資源
│   │   ├── assets/         # 資料檔案
│   │   ├── css/           # 樣式檔案
│   │   ├── js/            # JavaScript檔案
│   │   └── img/           # 圖片資源
│   ├── templates/          # HTML模板
│   │   ├── index.html     # 房價地圖頁面
│   │   └── buyhouse.html  # 買房vs租房頁面
│   ├── views.py           # 路由處理
│   └── __init__.py        # Flask應用初始化
├── main.py                # 應用程式進入點
├── wsgi.py               # WSGI配置
├── requirements.txt      # Python套件清單
├── pyproject.toml       # uv專案配置
└── README.md            # 專案說明文件
```

## 🌟 主要功能介紹

### 房價地圖分析
1. **點擊縣市**：選擇任一縣市查看詳細資訊
2. **趨勢篩選**：勾選/取消房價、租金、物價指數等指標
3. **數據比較**：查看該縣市與全台平均的差異
4. **時間軸分析**：觀察9年來的價格變化趨勢

### 買房vs租房計算
1. **基本設定**：選擇縣市、房型、屋齡、坪數
2. **個人資料**：輸入月收入、月消費、投資報酬率
3. **即時計算**：自動計算房屋總價、頭期款、月付金
4. **決策輔助**：比較買房vs租房30年後的資產差異

## 🎨 介面預覽

### 房價地圖頁面
- 左側：趨勢圖表 
- 右側：互動式台灣地圖 
- 下方：長條圖統計資料

### 買房vs租房頁面
- 左側：參數設定區域 
- 右側：地區選擇地圖
- 下方：比較圖表區域


## 📊 資料更新

系統包含完整的資料處理工具：
- `readata.py`：處理原始不動產交易資料
- 自動生成各縣市房價租金統計
- 支援新資料的批次匯入和處理

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

1. Fork 本專案
2. 建立功能分支 (`git checkout -b feature/新功能`)
3. 提交變更 (`git commit -m '新增：某某功能'`)
4. 推送分支 (`git push origin feature/新功能`)
5. 建立 Pull Request

## 📄 授權條款

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 📞 聯絡資訊

- 作者：FlagTech
- Email：kknono668@gmail.com
- GitHub：[@FlagTech](https://github.com/FlagTech)

---

**🤖 本專案部分功能由 [Claude Code](https://claude.ai/code) 協助開發**
