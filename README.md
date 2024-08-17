# ShodanTelegramBot

## 🇻🇳 Tiếng Việt

ShodanTelegramBot là một bot Telegram tích hợp với API Shodan, cho phép người dùng thực hiện các tìm kiếm Shodan và xem kết quả trực tiếp trong Telegram.

### Tính năng chính:
- Tìm kiếm Shodan thông qua lệnh Telegram
- Hiển thị kết quả tìm kiếm chi tiết
- Hướng dẫn sử dụng các bộ lọc Shodan
- Tra cứu thông tin CVE
- Quản lý người dùng và phân quyền

### Cài đặt:
1. Clone repository:
   ```
   git clone https://github.com/dirtycoins/ShodanTelegramBot.git
   cd ShodanTelegramBot
   ```
2. Tạo môi trường ảo và kích hoạt:
   ```
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   ```
3. Cài đặt các thư viện cần thiết:
   ```
   pip install -r requirements.txt
   ```

### Cấu hình:
1. Tạo file `config.py` và thêm các thông tin sau:
   ```python
   TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
   SHODAN_API_KEY = 'your_shodan_api_key'
   ADMIN_ID = your_telegram_user_id
   ```
2. Thay thế các giá trị trên bằng token bot Telegram, API key Shodan, và ID Telegram của bạn.

### Sử dụng:
Chạy bot:
```
python main.py
```

#### Các lệnh có sẵn:
- `/start` hoặc `/help`: Hiển thị thông tin trợ giúp
- `/search <truy vấn> <số lượng>`: Tìm kiếm trên Shodan
- `/filters`: Xem hướng dẫn về bộ lọc Shodan
- `/cve <CVE-ID>`: Tra cứu thông tin về CVE
- `/ex <bộ lọc>`: Giải thích chi tiết về một bộ lọc cụ thể

#### Ví dụ sử dụng:
1. Tìm kiếm:
   ```
   /search "Apache" country:VN 5
   ```
   Tìm 5 kết quả về máy chủ Apache tại Việt Nam.

2. Xem thông tin CVE:
   ```
   /cve CVE-2021-44228
   ```
   Hiển thị thông tin về lỗ hổng Log4Shell.

3. Giải thích bộ lọc:
   ```
   /ex port:80
   ```
   Giải thích chi tiết về bộ lọc tìm kiếm theo cổng 80.

### Tác giả:
n3k0ch3n

---

## 🇬🇧 English

ShodanTelegramBot is a Telegram bot integrated with the Shodan API, allowing users to perform Shodan searches and view results directly within Telegram.

### Key Features:
- Shodan search via Telegram commands
- Display detailed search results
- Guide on using Shodan filters
- CVE information lookup
- User management and authorization

### Installation:
1. Clone the repository:
   ```
   git clone https://github.com/dirtycoins/ShodanTelegramBot.git
   cd ShodanTelegramBot
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required libraries:
   ```
   pip install -r requirements.txt
   ```

### Configuration:
1. Create a `config.py` file and add the following information:
   ```python
   TELEGRAM_BOT_TOKEN = 'your_telegram_bot_token'
   SHODAN_API_KEY = 'your_shodan_api_key'
   ADMIN_ID = your_telegram_user_id
   ```
2. Replace the above values with your Telegram bot token, Shodan API key, and your Telegram user ID.

### Usage:
Run the bot:
```
python main.py
```

#### Available commands:
- `/start` or `/help`: Display help information
- `/search <query> <number>`: Search on Shodan
- `/filters`: View guide on Shodan filters
- `/cve <CVE-ID>`: Look up information about a CVE
- `/ex <filter>`: Detailed explanation of a specific filter

#### Usage examples:
1. Search:
   ```
   /search "Apache" country:US 5
   ```
   Find 5 results about Apache servers in the United States.

2. View CVE information:
   ```
   /cve CVE-2021-44228
   ```
   Display information about the Log4Shell vulnerability.

3. Explain filter:
   ```
   /ex port:80
   ```
   Detailed explanation of the filter for searching port 80.

### Author:
n3k0ch3n

---

## 📝 License

[MIT License](LICENSE)
