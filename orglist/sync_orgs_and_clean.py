"""
PCC Proactive Dictionary Manager
Version: v2.4 (v4.25.19)
Function: Auto-sync and update README.md metadata.
"""
import requests
import json
import os
import csv
import re
from datetime import datetime

SOURCE_URL = 'https://www.dgpa.gov.tw/open/code/orglist.csv'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACTIVE_FILE = os.path.join(BASE_DIR, 'units_Active.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'units_History.json')
README_FILE = os.path.join(BASE_DIR, 'README.md')

def convert_id_standard(oid):
    if not oid or len(oid) < 9: return oid
    raw_parts = [oid[0:1], oid[1:3], oid[3:5], oid[5:7], oid[7:9]]
    while len(raw_parts) > 1 and raw_parts[-1] == '00':
        raw_parts.pop()
    formatted_parts = []
    for i, p in enumerate(raw_parts):
        if i == 0: formatted_parts.append(p)
        else:
            clean_p = p.lstrip('0')
            formatted_parts.append(clean_p if clean_p else '0')
    return ".".join(formatted_parts)

def update_readme_date(official_date):
    """更新 README.md 中的日期欄位"""
    if os.path.exists(README_FILE):
        with open(README_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 使用正規表達式替換日期
        content = re.sub(r'最新檢查時間：\d{8}', f'最新檢查時間：{official_date}', content)
        
        with open(README_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"README.md 已更新為最新檢查日期: {official_date}")

def auto_update_dictionary():
    print("--- [v4.25.19] 同步管家行動中 ---")
    try:
        # 下載與偵測 (忽略 SSL 憑證檢查)
        head = requests.head(SOURCE_URL, verify=False)
        last_mod = head.headers.get('Last-Modified')
        date_str = datetime.strptime(last_mod, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y%m%d') if last_mod else datetime.now().strftime('%Y%m%d')
        
        target_filename = os.path.join(BASE_DIR, f"orglist_{date_str}.csv")
        if not os.path.exists(target_filename):
            print(f"正在更新官方名冊...")
            res = requests.get(SOURCE_URL, verify=False)
            with open(target_filename, 'wb') as f:
                f.write(res.content)
        
        active_map = {}
        history_map = {}
        with open(target_filename, 'r', encoding='cp950') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 8:
                    raw_id = row[0].strip()
                    pcc_id = convert_id_standard(raw_id)
                    info = {
                        "招標機關代碼": pcc_id,
                        "機關代碼": raw_id,
                        "機關名稱": row[1].strip(),
                        "郵遞區號": row[3].strip(),
                        "縣市": row[4].strip()[:3],
                        "主管代碼": row[6].strip(),
                        "主管名稱": row[7].strip()
                    }
                    is_retired = (row[12].strip() == '是')
                    if is_retired: history_map[pcc_id] = info
                    else: active_map[pcc_id] = info

        with open(ACTIVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(active_map, f, ensure_ascii=False, indent=2)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history_map, f, ensure_ascii=False, indent=2)

        # 同步更新文件日期
        update_readme_date(date_str)
        print(f"同步完成！")
        
    except Exception as e:
        print(f"字典同步失敗: {e}")

if __name__ == "__main__":
    auto_update_dictionary()
