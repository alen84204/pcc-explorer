# PCC Explorer 標案每日快報系統

專業的政府標案監控與機關代碼適配系統。透過自動化腳本同步官方名冊與最新標案資料。

## 📊 系統狀態 (System Status)
* **最新標案日期**：20260505
* **官方機關名冊最新日期**：20260302
* **系統最後檢測時間**：20260521 22:15

## 🚀 核心功能
* **每日快報**：自動抓取 PCC 最新公開招標資料。
* **智慧對照**：將官方 ID 轉換為標案點狀格式（如 `A.19.05.01`）。
* **雙軌字典**：區分「有效機關」與「歷史機關」，確保搜尋無死角。
* **機關快搜**：[線上查詢機關代碼](https://alen84204.github.io/pcc-explorer/org-search.html)。
* **自動化分流**：機關字典與標案抓取已拆成兩條 GitHub Actions workflow，各自負責各自資料域。

## 📁 目錄結構
* `pcc_crawler.py`：標案日報抓取流程。
* `index.html`：視覺化看板。
* `orglist/`：機關字典管理模組（含 CSV 正式來源、JSON 快照、內部 lookup、對外精簡 JSON、manifest 與同步工具）。
* `.github/workflows/orglist_sync.yml`：每天台灣時間（UTC+8）05:00 同步機關字典。
* `.github/workflows/tenders_sync.yml`：在機關字典同步成功後續跑，抓取每日標案資料。

## 🔀 自動化責任邊界
* **Orglist workflow**：只負責官方機關名冊同步、lookup / 精簡 JSON 輸出、`manifest.json`、`org-search.html` 與相關 README 狀態更新。
* **Tenders workflow**：只負責 `pcc_crawler.py`、`data.json` 與標案日期相關更新。
* **同一個 repo，不同資料域**：機關字典與標案資料仍共用同一 repo，但排程與提交責任已拆開。

---
本系統由 GitHub Actions 自動驅動，依既定排程更新。
