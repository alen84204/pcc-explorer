"""
PCC Proactive Dictionary Manager
Version: v2.5 (v4.25.20)
Function: Dual-README update (Root & Orglist).
"""
import requests
import json
import os
import csv
import re
from datetime import datetime

SOURCE_URL = 'https://www.dgpa.gov.tw/open/code/orglist.csv'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

ACTIVE_FILE = os.path.join(BASE_DIR, 'units_Active.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'units_History.json')
ORG_README = os.path.join(BASE_DIR, 'README.md')
ROOT_README = os.path.join(ROOT_DIR, 'README.md')

def convert_id_standard(oid):
    if not oid or len(oid) < 9: return oid
    parts = [oid[0:1], oid[1:3], oid[3:5], oid[5:7], oid[7:9]]
    while len(parts) > 1 and parts[-1] == '00': parts.pop()
    res = [parts[0]]
    for p in parts[1:]:
        c = p.lstrip('0')
        res.append(c if c else '0')
    return ".".join(res)

def update_all_readmes(official_date):
    today_str = datetime.now().strftime('%Y%m%d')
    # 1. 更新 Root README
    if os.path.exists(ROOT_README):
        with open(ROOT_README, 'r', encoding='utf-8') as f:
            c = f.read()
        c = re.sub(r'官方機關名冊日期：\d{8}', f'官方機關名冊日期：{official_date}', c)
        c = re.sub(r'系統最後運行時間：\d{8}', f'系統最後運行時間：{today_str}', c)
        with open(ROOT_README, 'w', encoding='utf-8') as f: f.write(c)
    
    # 2. 更新 Sub README
    if os.path.exists(ORG_README):
        with open(ORG_README, 'r', encoding='utf-8') as f:
            c = f.read()
        c = re.sub(r'官方機關名冊日期：\d{8}', f'官方機關名冊日期：{official_date}', c)
        c = re.sub(r'系統最後檢查時間：\d{8}', f'系統最後檢查時間：{today_str}', c)
        with open(ORG_README, 'w', encoding='utf-8') as f: f.write(c)
    print(f"README 更新完成 (官方: {official_date}, 運行: {today_str})")

def auto_update_dictionary():
    print("--- [v4.25.20] 字典同步管家 ---")
    try:
        head = requests.head(SOURCE_URL, verify=False)
        last_mod = head.headers.get('Last-Modified')
        date_str = datetime.strptime(last_mod, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y%m%d') if last_mod else datetime.now().strftime('%Y%m%d')
        
        target_filename = os.path.join(BASE_DIR, f"orglist_{date_str}.csv")
        if not os.path.exists(target_filename):
            res = requests.get(SOURCE_URL, verify=False)
            with open(target_filename, 'wb') as f: f.write(res.content)
        
        active_map = {}
        history_map = {}
        with open(target_filename, 'r', encoding='cp950') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if len(row) >= 8:
                    pcc_id = convert_id_standard(row[0].strip())
                    info = {"機關代碼": row[0].strip(), "機關名稱": row[1].strip(), "郵遞區號": row[3].strip(), 
                            "縣市": row[4].strip()[:3], "主管代碼": row[6].strip(), "主管名稱": row[7].strip()}
                    if len(row) > 12 and row[12].strip() == '是': history_map[pcc_id] = info
                    else: active_map[pcc_id] = info

        with open(ACTIVE_FILE, 'w', encoding='utf-8') as f: json.dump(active_map, f, ensure_ascii=False, indent=2)
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f: json.dump(history_map, f, ensure_ascii=False, indent=2)
        
        update_all_readmes(date_str)
        
    except Exception as e: print(f"同步失敗: {e}")

if __name__ == "__main__":
    auto_update_dictionary()
