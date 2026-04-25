# PCC Agency Dictionary System (PADS)

本資料夾負責管理並維護政府標案系統的機關代碼對照表。

## 📊 字典同步狀態
*   **官方機關名冊日期**：20260302
*   **系統最後檢查時間**：20260425

## 1. 資料來源 (Data Source)
*   **官方來源**：[行政院人事行政總處 - 機關代碼資料集](https://data.gov.tw/dataset/7307)
*   **自動下載網址**：`https://www.dgpa.gov.tw/open/code/orglist.csv`

## 2. 代碼轉換規則
1. A19050100G -> A.19.5.1 (移除子段落前導零與末尾段落00)
2. 310350000Q -> 3.10.35

## 3. 資料結構
*   `units_Active.json`：現役機關百科。
*   `units_History.json`：歷史機關百科。

## 4. 維護方式 (Maintenance)
本模組已整合至 **GitHub Actions** 自動化流程中。
系統會於每日凌晨自動執行 `orglist/sync_orgs_and_clean.py`，偵測官方伺服器之 `Last-Modified` 標頭。若有更新即自動同步。
