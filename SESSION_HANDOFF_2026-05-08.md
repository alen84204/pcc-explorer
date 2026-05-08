# PCC 參考來源與整理存檔

建立時間：2026-05-08

這份文件是給換 session 後接續使用的整理稿。  
重點是把「資料集頁」和「下載檔」分開標示，也把第三方整理站和官方來源區分清楚。

## 1. 官方資料來源

### 政府資料開放平台（機關代碼資料集）
- `https://data.gov.tw/dataset/7307`
- 這是資料集入口頁，方便找到來源與說明。

### 機關代碼下載檔
- `https://www.dgpa.gov.tw/open/code/orglist.csv`
- 這是實際下載資料的 CSV 檔，不是一般網頁。

### 政府電子採購網
- `https://web.pcc.gov.tw/`
- 官方原始標案來源。

### 政府電子採購網查詢入口
- `https://web.pcc.gov.tw/pis/`
- 官方查詢入口。

### 行政院公共工程委員會
- `https://www.pcc.gov.tw/pcc/`
- 主管機關網站。

## 2. 第三方整理 / 民間站點

### PCC Viewer
- `https://openfunltd.github.io/pcc-viewer/index.html`
- 用官方資料做成的標案瀏覽站，介面清楚，適合快速查詢。

### 開放標案 g0v
- `https://pcc.mlwmlw.org/`
- 民間整理站，資料量大，但使用體驗你目前評價為「不好用」。

### pcc.g0v.ronny.tw
- `https://pcc.g0v.ronny.tw/`
- 舊版或鏡像型整理站，可用來比對資料。

### PCC API / 資料整合站
- `https://pcc-api.openfun.app/`
- 這不是官方 API；是用官方資料整理出來的資料服務或介面。

## 3. 商業 / 加值型站點

### TBN
- `https://www.taiwanbuying.com.tw/`
- 商業型標案平台，偏訂閱或加值查詢。

### ACE 台灣招標採購網
- `https://acebidx.com/zh-TW`
- 商業型平台，偏搜尋與追蹤。

### 台灣政府採購與標案情報站
- `https://ezbid.tw/`
- 商業型標案情報站。

### 標案雷達
- `https://bidacumen.bidacumen.workers.dev/`
- 商業或加值型服務入口。

### BidAcumen 官方站
- `https://bidacumen.com/`
- BidAcumen 的主站。

## 4. 機關代碼輔助頁

### PCC Explorer 機關代碼查詢
- `https://alen84204.github.io/pcc-explorer/org-search.html`
- 用來查機關名稱與代碼的輔助頁，不是標案主站。

## 5. 這次確認過的格式原則

- `資料集頁` 和 `下載檔` 要放在同一組。
- 下載檔要明確寫出它是檔案，不要只留資料集頁。
- `https://pcc-api.openfun.app/` 要標成第三方整理站，不要寫成官方 API。
- 參考來源最好用 `官方名稱 | 網址 | 說明` 這種格式。

## 6. 目前 repo 對應的最新日別資料

- `2026-05-05`
- 本地目前對應的日別檔案都是這一天。
- 相關檔案：
  - `listbydate_20260505_exclude_labor.json`
  - `listbydate_20260505_labor_and_other.json`
  - `listbydate_20260505_labor_no_islands.json`
  - `listbydate_20260505_labor_no_islands_open_tender.json`

## 7. 備註

- 這個 repo 的 `orglist/` 是機關代碼資料模組。
- `org-search.html` 是查機關代碼的輔助頁。
- `pcc_crawler.py` 會從標案資料來源抓日別資料，並產出本地檔案。
