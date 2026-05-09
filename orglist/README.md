# PCC Agency Dictionary System (PADS)

本資料夾負責管理並維護政府標案系統的機關代碼對照表。

## 📊 字典同步狀態
*   **官方機關名冊最新日期**：20260302
*   **系統最後檢測時間**：20260509 16:42
*   **同步摘要**：`manifest.json` 會集中記錄來源檔、查核時間、檔案大小與 MD5。

## 🔎 快搜入口
*   **線上機關快搜**：[org-search.html](https://alen84204.github.io/pcc-explorer/org-search.html)
*   **資料位置說明**：`orglist/` 保留作為機關字典資料模組；公開搜尋頁維持在根目錄 `org-search.html`，避免破壞既有 GitHub Pages 網址與 JSON 讀取路徑。

## ✨ 核心功能特點 (Features)

### 1. 自動化管理 (Automated Management)
*   **主動偵測**：自動連線 DGPA 官網，解析 `Last-Modified` 標頭以識別官方更新日期。
*   **精準取名**：依照官方發布日期自動進行資產命名 (如 `orglist_20260302.csv`)。
*   **雲端同步**：完美整合 GitHub Actions，達成 24/7 無人值守自動更新。

### 2. 資料清洗與轉換 (Data Cleaning)
*   **跨編碼轉換**：自動將原始 Big5 (CP950) CSV 轉換為標準 UTF-8 JSON 格式。
*   **代碼適配器 (ID Fitter)**：實作 1-2-2-2-2 拆分邏輯，去除子段落前導零與末尾無用位元。
*   **地理資訊提取**：智慧解析原始地址，精確提取「縣市」層級資訊。

### 3. 機關屬性匹配 (Intelligence)
*   **新舊關聯**：支援新舊代碼並存，並依據 `裁撤註記` 進行階層式分類。
*   **主從關係**：保留主管機關 (Parent Org) 關聯，支援後續多維度篩選。
*   **字典階層化**：獨立產出 `units_Active` 與 `units_History` 字典，達到查詢效能最優化。

### 4. 系統文檔化 (Self-Documenting)
*   **自動化文件**：腳本執行完畢後會自動將最新狀態回傳更新至 README.md。
*   **結構清晰**：功能模組化設計，可獨立於主爬蟲系統運行。

## 1. 資料來源 (Data Source)
*   **官方來源入口**：[行政院人事行政總處 - 機關代碼資料集](https://data.gov.tw/dataset/7307)
*   **正式來源**：`https://www.dgpa.gov.tw/open/code/orglist.csv`（CSV 為唯一正式來源）
*   **官方快照**：`orglist_20260302.json`（保留檔／輔助檔，不視為正式來源）

## 2. 代碼轉換規則
1. A19050100G -> A.19.5.1 (移除子段落前導零與末尾段落00)
2. 310350000Q -> 3.10.35

## 3. 資料結構
*   `orglist_20260302.csv`：官方正式來源檔。
*   `orglist_20260302.json`：官方快照檔。
*   `units_Active.json`：現役機關 lookup。
*   `units_History.json`：歷史機關 lookup。
*   `manifest.json`：同步清單／資料清單，記錄來源、檔案大小與 MD5。

## 4. 維護方式 (Maintenance)
本模組已整合至 **GitHub Actions** 自動化流程中。
系統會於每日凌晨自動執行 `orglist/sync_orgs_and_clean.py`，偵測官方伺服器之 `Last-Modified` 標頭。若有更新即自動同步。`manifest.json` 會同步提供頁面查核資訊。
