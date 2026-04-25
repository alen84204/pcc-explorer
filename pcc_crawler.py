"""
PCC Tender Crawler
Version: v4.25.19
Updates: Automatic documentation update in orglist/README.md.
"""
import requests
import json
import os
import re
from datetime import datetime, timedelta

VERSION = "v4.25.19"
ACTIVE_FILE = os.path.join('orglist', 'units_Active.json')
HISTORY_FILE = os.path.join('orglist', 'units_History.json')
README_FILE = os.path.join('orglist', 'README.md')
BASE_API = "https://pcc-api.openfun.app/api"

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}
    return {}

def update_readme_tender_date(date_str):
    """更新 README.md 中的標案資料日期"""
    if os.path.exists(README_FILE):
        with open(README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        content = re.sub(r'最新資料時間：\d{8}', f'最新資料時間：{date_str}', content)
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"README.md 已更新標案日期: {date_str}")

def infer_category(title, original_cat):
    if original_cat and any(k in original_cat for k in ['工程','財物','勞務']):
        if "工程" in original_cat: return "工程"
        if "財物" in original_cat: return "財物"
        if "勞務" in original_cat: return "勞務"
    t = title.lower()
    if any(k in t for k in ['工程', '建置', '維修', '裝修', '改良', '修復']): return "工程"
    if any(k in t for k in ['採購', '設備', '租賃', '零件', '材料', '器材', '儀器']): return "財物"
    if any(k in t for k in ['勞務', '維護', '委外', '服務', '研究', '規劃', '清潔']): return "勞務"
    return "其他"

def fetch_data(date_str):
    active_map = load_json(ACTIVE_FILE)
    history_map = load_json(HISTORY_FILE)
    url = f"{BASE_API}/listbydate?date={date_str}"
    print(f"[{VERSION}] 抓取日期: {date_str}")
    
    res = requests.get(url, timeout=30)
    res.raise_for_status()
    records = res.json().get('records', [])
    
    results = []
    for r in records:
        uid = r['unit_id']
        name = r.get('unit_name')
        if not name or name == "未知機關":
            info = active_map.get(uid) or history_map.get(uid)
            name = info.get('機關名稱', f"未知機關({uid})") if isinstance(info, dict) else (info or f"未知機關({uid})")

        title = r['brief'].get('title', '')
        results.append({
            '公告日期': date_str,
            '採購性質': infer_category(title, r['brief'].get('category', '')),
            '機關名稱': name,
            '機關代碼': uid,
            '標案名稱': title,
            '標案案號': r['job_number'],
            '公告類型': r['brief'].get('type', ''),
            '連結': f"https://openfunltd.github.io/pcc-viewer/tender.html?unit_id={uid}&job_number={r['job_number']}"
        })
    return results

if __name__ == "__main__":
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
    try:
        data = fetch_data(yesterday)
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        # 同步更新文件
        update_readme_tender_date(yesterday)
        print(f"[{VERSION}] 抓取完成！")
    except Exception as e:
        print(f"執行出錯: {e}")
