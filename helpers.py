import json
import os
from datetime import datetime
import requests
from functools import lru_cache
import logging


def load_user_data(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}

def save_user_data(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def update_user_data(user_data, user_id, user_name, search_query=None):
    user_id = str(user_id)
    if user_id not in user_data:
        user_data[user_id] = {
            "name": user_name,
            "created": datetime.now().isoformat(),
            "usage_count": 0,
            "search_history": [],
            "approved": user_id == str(ADMIN_ID)
        }
    user_data[user_id]["usage_count"] += 1
    if search_query:
        user_data[user_id]["search_history"].append({
            "query": search_query,
            "timestamp": datetime.now().isoformat()
        })

@lru_cache(maxsize=100)
def get_cve_description(cve_id):
    try:
        response = requests.get(f"https://cve.circl.lu/api/cve/{cve_id}", timeout=5)
        response.raise_for_status()
        cve_data = response.json()

        cve_id = cve_data.get('id', 'Không có ID')
        description = cve_data.get('summary', 'Không có mô tả')
        impact = cve_data.get('impact', {})
        cvss = cve_data.get('cvss', 'Không có CVSS')

        return f"""
🆔 CVE ID: {cve_id}
📜 Mô tả: {description}
📊 CVSS: {cvss}

🌐 Tác động:
- 📉 Tính khả dụng: {impact.get('availability', 'Không xác định')}
- 🔒 Bảo mật: {impact.get('confidentiality', 'Không xác định')}
- 🛡️ Tính toàn vẹn: {impact.get('integrity', 'Không xác định')}
"""
    except Exception as e:
        return f"Lỗi khi định dạng kết quả: {str(e)}"

def escape_markdown(text):
    escape_chars = '_*[]()~`>#+=|{}.!'
    return ''.join(f'\\{char}' if char in escape_chars else char for char in str(text))

def format_date(date_string):
    date_object = datetime.fromisoformat(date_string)
    return date_object.strftime("%Y/%m/%d %H:%M")