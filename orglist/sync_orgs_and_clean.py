"""
PCC Proactive Dictionary Manager
Version: v2.6 (orglist refactor)
Function: Sync official CSV, build lookup files, and refresh manifests/docs.
"""

import csv
import hashlib
import json
import os
import re
import unicodedata
from datetime import datetime

import requests

SOURCE_URL = 'https://www.dgpa.gov.tw/open/code/orglist.csv'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)

ACTIVE_FILE = os.path.join(BASE_DIR, 'units_Active.json')
HISTORY_FILE = os.path.join(BASE_DIR, 'units_History.json')
MANIFEST_FILE = os.path.join(BASE_DIR, 'manifest.json')
ORG_README = os.path.join(BASE_DIR, 'README.md')
ROOT_README = os.path.join(ROOT_DIR, 'README.md')
ORG_SEARCH_HTML = os.path.join(ROOT_DIR, 'org-search.html')


def convert_id_standard(oid):
    if not oid or len(oid) < 9:
        return oid
    parts = [oid[0:1], oid[1:3], oid[3:5], oid[5:7], oid[7:9]]
    while len(parts) > 1 and parts[-1] == '00':
        parts.pop()
    res = [parts[0]]
    for p in parts[1:]:
        c = p.lstrip('0')
        res.append(c if c else '0')
    return '.'.join(res)


def normalize_text(value):
    return (
        unicodedata.normalize('NFKC', value or '')
        .replace('臺', '台')
        .lower()
        .replace('\u3000', ' ')
    )


def compact_text(value):
    return re.sub(r'[\s\u3000]+', '', normalize_text(value))


def build_aliases(row, pcc_id):
    aliases = []
    candidates = [
        row[1].strip(),
        row[7].strip(),
        row[0].strip(),
        pcc_id,
        row[0].strip().replace('.', ''),
        compact_text(row[1].strip()),
        compact_text(row[7].strip()),
    ]
    for candidate in candidates:
        if candidate and candidate not in aliases:
            aliases.append(candidate)
    return aliases


def md5_of_file(path):
    h = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def write_json(path, payload):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def build_manifest(official_date, checked_at, last_modified):
    entries = []
    for label, path, kind in [
        ('source_csv', os.path.join(BASE_DIR, f'orglist_{official_date}.csv'), 'source'),
        ('snapshot_json', os.path.join(BASE_DIR, f'orglist_{official_date}.json'), 'snapshot'),
        ('lookup_active', ACTIVE_FILE, 'lookup'),
        ('lookup_history', HISTORY_FILE, 'lookup'),
    ]:
        if os.path.exists(path):
            entries.append({
                'label': label,
                'kind': kind,
                'file': os.path.basename(path),
                'size': os.path.getsize(path),
                'md5': md5_of_file(path),
            })

    payload = {
        'official_date': official_date,
        'system_last_checked': checked_at,
        'source_url': SOURCE_URL,
        'source_last_modified': last_modified,
        'source_formats': ['csv'],
        'snapshot_formats': ['json'],
        'files': entries,
    }
    write_json(MANIFEST_FILE, payload)


def refresh_readme(path, official_date, checked_at):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(
        r'(官方機關名冊(?:最新)?日期(?:\*\*)?：)\d{8}',
        rf'\g<1>{official_date}',
        content,
    )
    content = re.sub(
        r'(系統最後(?:檢查|檢測|運行)時間(?:\*\*)?：)\d{8}(?:\s+\d{2}:\d{2})?',
        rf'\g<1>{checked_at}',
        content,
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


def update_readmes(official_date, checked_at):
    refresh_readme(ROOT_README, official_date, checked_at)
    refresh_readme(ORG_README, official_date, checked_at)


def fetch_source_date():
    head = requests.head(SOURCE_URL, verify=False, timeout=30)
    head.raise_for_status()
    last_mod = head.headers.get('Last-Modified')
    if last_mod:
        try:
            return datetime.strptime(last_mod, '%a, %d %b %Y %H:%M:%S %Z').strftime('%Y%m%d'), last_mod
        except ValueError:
            pass
    return datetime.now().strftime('%Y%m%d'), last_mod


def build_record(row):
    pcc_id = convert_id_standard(row[0].strip())
    return pcc_id, {
        '機關代碼': row[0].strip(),
        '機關名稱': row[1].strip(),
        '郵遞區號': row[3].strip(),
        '縣市': row[4].strip()[:3],
        '主管代碼': row[6].strip(),
        '主管名稱': row[7].strip(),
        'aliases': build_aliases(row, pcc_id),
    }


def auto_update_dictionary():
    print('--- [v2.6] 字典同步管家 ---')
    try:
        date_str, last_mod = fetch_source_date()

        target_filename = os.path.join(BASE_DIR, f'orglist_{date_str}.csv')
        if not os.path.exists(target_filename):
            res = requests.get(SOURCE_URL, verify=False, timeout=60)
            res.raise_for_status()
            with open(target_filename, 'wb') as f:
                f.write(res.content)

        active_map = {}
        history_map = {}
        with open(target_filename, 'r', encoding='cp950') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) >= 8:
                    pcc_id, info = build_record(row)
                    if len(row) > 12 and row[12].strip() == '是':
                        history_map[pcc_id] = info
                    else:
                        active_map[pcc_id] = info

        write_json(ACTIVE_FILE, active_map)
        write_json(HISTORY_FILE, history_map)

        checked_at = datetime.now().strftime('%Y%m%d %H:%M')
        build_manifest(date_str, checked_at, last_mod)
        update_readmes(date_str, checked_at)

    except Exception as e:
        print(f'同步失敗: {e}')


if __name__ == '__main__':
    auto_update_dictionary()
