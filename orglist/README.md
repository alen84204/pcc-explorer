# PCC Agency Dictionary System (PADS)

本資料夾負責管理並維護政府標案系統的機關代碼對照表。

## 🎯 模組邊界
* **本模組只負責**：同步官方機關名冊、轉換 PCC 點狀代碼、輸出機關 lookup 與對外精簡 JSON。
* **本模組不負責**：標案主資料抓取、標案篩選商業邏輯、Tender 頁面展示。
* **正式同步策略**：每天 1 次，台灣時間（UTC+8）05:00。

## 📊 字典同步狀態
* **官方機關名冊最新日期**：20260302
* **系統最後檢測時間**：20260720 21:56
* **同步摘要**：`manifest.json` 會集中記錄來源檔、查核時間、更新頻率、檔案大小與 MD5。

## 🔎 快搜入口
* **線上機關快搜**：[org-search.html](https://alen84204.github.io/pcc-explorer/org-search.html)
* **資料位置說明**：`orglist/` 保留作為機關字典資料模組；公開搜尋頁維持在根目錄 `org-search.html`，避免破壞既有 GitHub Pages 網址與 JSON 讀取路徑。

## ✨ 核心功能特點

### 1. 自動化管理
* **主動偵測**：自動連線 DGPA 官網，解析 `Last-Modified` 標頭以識別官方更新日期。
* **精準取名**：依照官方發布日期自動進行資產命名（如 `orglist_20260302.csv`）。
* **雲端同步**：整合 GitHub Actions，以固定策略每日同步一次。

### 2. 資料清洗與轉換
* **跨編碼轉換**：自動將原始 Big5（CP950）CSV 轉換為標準 UTF-8 JSON 格式。
* **代碼適配器**：實作 1-2-2-2-2 拆分邏輯，去除子段落前導零與末尾無用位元。
* **地理資訊提取**：解析原始欄位並提取「縣市」層級資訊。

### 3. 輸出分層
* **內部完整 lookup**：保留 `units_Active.json`、`units_History.json` 供站內相容使用。
* **對外精簡輸出**：提供 `orgs_active_min.json`、`orgs_history_min.json`，每筆僅保留 `機關代碼`、`機關名稱`。
* **查核資訊**：`manifest.json` 提供頁面狀態與同步查核資訊。

## 1. 資料來源
* **官方來源入口**：[行政院人事行政總處 - 機關代碼資料集](https://data.gov.tw/dataset/7307)
* **正式來源**：`https://www.dgpa.gov.tw/open/code/orglist.csv`（CSV 為唯一正式來源）
* **官方快照**：`orglist_20260302.json`（保留檔／輔助檔，不視為正式來源）

## 2. 代碼轉換規則
1. `A19050100G -> A.19.5.1`（移除子段落前導零與末尾段落 `00`）
2. `310350000Q -> 3.10.35`

## 3. 資料結構
* `orglist_20260302.csv`：官方正式來源檔。
* `orglist_20260302.json`：官方快照檔。
* `units_Active.json`：現役機關完整 lookup（內部相容用途）。
* `units_History.json`：歷史機關完整 lookup（內部相容用途）。
* `orgs_active_min.json`：對外精簡版現役機關資料（僅保留 `機關代碼`、`機關名稱`）。
* `orgs_history_min.json`：對外精簡版歷史機關資料（僅保留 `機關代碼`、`機關名稱`）。
* `manifest.json`：同步清單／資料清單，記錄來源、更新頻率、檔案大小與 MD5。

## 4. 維護方式
本模組由獨立的 **GitHub Actions workflow** 維護：`.github/workflows/orglist_sync.yml`。
系統會於每天台灣時間（UTC+8）05:00 自動執行 `orglist/sync_orgs_and_clean.py`，偵測官方伺服器之 `Last-Modified` 標頭。若有更新即自動同步。`manifest.json` 會提供頁面查核資訊；對外資料取用請優先使用 `orgs_active_min.json` 與 `orgs_history_min.json`。
