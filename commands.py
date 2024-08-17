import time
import logging

import shodan
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import SHODAN_API_KEY, ADMIN_ID, USER_DATA_FILE
from filters import FILTER_EXPLANATIONS
from helpers import update_user_data, save_user_data, get_cve_description, escape_markdown, format_date

api = shodan.Shodan(SHODAN_API_KEY)

logging.basicConfig(filename='shodan_bot.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def register_commands(bot, user_data):
    def user_approved(func):
        def wrapper(message):
            user_id = str(message.from_user.id)
            if user_id in user_data and user_data[user_id].get("approved", False):
                return func(message)
            else:
                bot.reply_to(message, "Bạn chưa được phê duyệt để sử dụng bot. Vui lòng đợi admin phê duyệt.")

        return wrapper

    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        user_id = str(message.from_user.id)
        user_name = message.from_user.first_name
        update_user_data(user_data, user_id, user_name)

        if user_id not in user_data or not user_data[user_id].get("approved", False):
            if user_id != str(ADMIN_ID):
                bot.reply_to(message, "Vui lòng đợi admin phê duyệt trước khi sử dụng bot.")
                admin_message = f"Người dùng mới: {user_name} (ID: {user_id}) muốn sử dụng bot."
                bot.send_message(ADMIN_ID, admin_message, reply_markup=create_approval_keyboard(user_id))
                return
            else:
                user_data[user_id]["approved"] = True
                save_user_data(user_data, USER_DATA_FILE)

        welcome_text = (
            "🤖 *Chào mừng đến với Shodan Telegram Bot!*\n\n"
            "🔍 *Các lệnh có sẵn:*\n"
            "• /start - 🚀 Khởi động bot\n"
            "• /help - ℹ️ Hiển thị trợ giúp\n"
            "• /search <truy vấn> <số lượng> - 🔎 Tìm kiếm trên Shodan\n"
            "• /filters - 🧰 Xem hướng dẫn về bộ lọc\n"
            "• /cve - 📊 Xem thông tin chi tiết CVE\n\n"
            "📝 *Ví dụ sử dụng:*\n"
            "• `/search apache 5` - Tìm 5 kết quả cho 'apache'\n"
            "• `/search hostname:example.com 3` - Tìm 3 kết quả cho hostname cụ thể\n\n"
            "🔐 *Lưu ý:* Sử dụng bot này một cách có trách nhiệm và tuân thủ các quy định pháp luật.\n\n"
            "🌟 Chúc bạn có trải nghiệm tuyệt vời với Shodan Bot!"
        )
        bot.reply_to(message, welcome_text, parse_mode='Markdown')

    @bot.callback_query_handler(func=lambda call: call.data.startswith(('approve_', 'deny_')))
    def callback_query(call):
        action, user_id = call.data.split('_')
        user_id = str(user_id)

        if action == 'approve':
            user_data[user_id] = user_data.get(user_id, {})
            user_data[user_id]["approved"] = True
            save_user_data(user_data, USER_DATA_FILE)
            bot.answer_callback_query(call.id, "Người dùng đã được phê duyệt.")
            bot.edit_message_text("Người dùng đã được phê duyệt.", call.message.chat.id, call.message.message_id)

            try:
                bot.send_message(int(user_id),
                                 "🎉 Xin chúc mừng! Bạn đã được phê duyệt để sử dụng Shodan Bot. Bạn có thể bắt đầu sử dụng các tính năng của bot. Nhập /help để xem các lệnh có sẵn.")
            except Exception as e:
                logger.error(f"Không thể gửi tin nhắn phê duyệt cho người dùng {user_id}: {str(e)}")

            bot.send_message(call.message.chat.id,
                             f"Người dùng {user_data[user_id]['name']} đã được phê duyệt để sử dụng bot.")
        elif action == 'deny':
            if user_id in user_data:
                del user_data[user_id]
                save_user_data(user_data, USER_DATA_FILE)
            bot.answer_callback_query(call.id, "Người dùng đã bị từ chối.")
            bot.edit_message_text("Người dùng đã bị từ chối.", call.message.chat.id, call.message.message_id)

        try:
            if call.message.reply_markup:
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=None)
        except telebot.apihelper.ApiTelegramException as e:
            if "message is not modified" not in str(e):
                logger.error(f"Lỗi khi chỉnh sửa markup tin nhắn: {str(e)}")

    @bot.message_handler(commands=['search'])
    @user_approved
    def search_shodan(message):
        args = message.text.split(maxsplit=2)
        if len(args) < 2:
            bot.reply_to(message, "❌ Vui lòng nhập truy vấn tìm kiếm. Ví dụ: `/search apache 5`",
                         parse_mode='MarkdownV2')
            return

        query = args[1] if len(args) == 2 else args[1] + ' ' + args[2]
        limit = 5

        query_parts = query.rsplit(maxsplit=1)
        if len(query_parts) > 1 and query_parts[-1].isdigit():
            query = query_parts[0]
            limit = int(query_parts[-1])

        update_user_data(user_data, message.from_user.id, message.from_user.first_name, query)

        try:
            logger.info(f"Yêu cầu API Shodan - Truy vấn: {query}, Giới hạn: {limit}")

            start_time = time.time()
            results = list(api.search(query, limit=limit)['matches'])
            end_time = time.time()

            logger.info(f"Phản hồi API Shodan - Thời gian: {end_time - start_time:.2f}s, Kết quả: {len(results)}")

            print(f"Yêu cầu API Shodan - Truy vấn: {query}, Giới hạn: {limit}")
            print(f"Phản hồi API Shodan - Thời gian: {end_time - start_time:.2f}s, Kết quả: {len(results)}")

            if not results:
                bot.reply_to(message, f"😔 Không tìm thấy kết quả nào cho `{escape_markdown(query)}`\\.",
                             parse_mode='MarkdownV2')
                return

            response = f"🔍 *Kết quả tìm kiếm cho* `{escape_markdown(query)}`*:*\n\n"
            response += f"📊 Số lượng kết quả hiển thị: `{len(results)}`\n\n"
            response += "👇 Nhấn vào các nút bên dưới để xem chi tiết từng kết quả\\."

            bot.reply_to(message, response, parse_mode='MarkdownV2', reply_markup=create_result_buttons(results))

            bot.set_state(message.from_user.id, 'search_results', message.chat.id)
            with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
                data['results'] = results

        except shodan.APIError as e:
            bot.reply_to(message, f"❌ Lỗi API Shodan: {escape_markdown(str(e))}", parse_mode='MarkdownV2')
        except Exception as e:
            bot.reply_to(message, f"❌ Đã xảy ra lỗi không mong muốn: {escape_markdown(str(e))}",
                         parse_mode='MarkdownV2')

    @bot.callback_query_handler(func=lambda call: call.data.startswith('details_'))
    def callback_query_details(call):
        try:
            index = int(call.data.split('_')[1])
            with bot.retrieve_data(call.from_user.id, call.message.chat.id) as data:
                results = data.get('results', [])
                if index < len(results):
                    result = results[index]
                    try:
                        logger.info(f"Yêu cầu API Shodan - Host: {result['ip_str']}")

                        start_time = time.time()
                        host = api.host(result['ip_str'])
                        end_time = time.time()

                        logger.info(f"Phản hồi API Shodan - Thời gian: {end_time - start_time:.2f}s")

                        print(f"Yêu cầu API Shodan - Host: {result['ip_str']}")
                        print(f"Phản hồi API Shodan - Thời gian: {end_time - start_time:.2f}s")

                        response = format_detailed_result(host)
                        bot.answer_callback_query(call.id)
                        bot.send_message(call.message.chat.id, response, parse_mode='Markdown')

                        if call.message.reply_markup:
                            new_keyboard = InlineKeyboardMarkup()
                            for i, button in enumerate(call.message.reply_markup.keyboard):
                                if i != index:
                                    new_keyboard.add(button[0])
                            try:
                                bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                              message_id=call.message.message_id,
                                                              reply_markup=new_keyboard)
                            except telebot.apihelper.ApiTelegramException as e:
                                if "message is not modified" not in str(e):
                                    logger.error(f"Lỗi khi chỉnh sửa markup tin nhắn: {str(e)}")
                    except shodan.APIError as e:
                        bot.answer_callback_query(call.id, f"Lỗi khi lấy thông tin chi tiết: {str(e)}")
                else:
                    bot.answer_callback_query(call.id, "Không tìm thấy thông tin chi tiết.")
        except Exception as e:
            bot.answer_callback_query(call.id, f"Đã xảy ra lỗi: {str(e)}")

    @bot.message_handler(commands=['ex'])
    @user_approved
    def explain_filter(message):
        filter_text = message.text.split('/ex', 1)[1].strip().lower()

        matching_filter = next((f for f in FILTER_EXPLANATIONS if f in filter_text), None)

        if matching_filter:
            filter_info = FILTER_EXPLANATIONS[matching_filter]
            response = f"🔍 *Giải thích về bộ lọc: {filter_info['example']}*\n\n"
            response += f"📝 *Mô tả:*\n{filter_info['explanation']}\n\n"
            response += f"🚀 *Truy vấn mẫu:*\n`{filter_info['sample_query']}`\n\n"
            response += "Để sử dụng truy vấn này, hãy sao chép và dán vào chat, hoặc chỉnh sửa theo nhu cầu của bạn."
        else:
            response = "Xin lỗi, tôi không có giải thích cụ thể cho bộ lọc đó. Vui lòng kiểm tra lệnh /filters để xem danh sách các bộ lọc có sẵn."

        bot.reply_to(message, response, parse_mode='Markdown')

    from helpers import escape_markdown

    from helpers import escape_markdown

    @bot.message_handler(commands=['filters'])
    @user_approved
    def show_filters(message):
        filters_text = """
*🔍 𝔹𝕒̉𝕟𝕘 𝕥𝕣𝕒̣̂𝕟 𝔹𝕠̣̂ 𝕝𝕠̣𝕔 𝕊𝕙𝕠𝕕𝕒𝕟*

*🔰 Bộ lọc cơ bản:*
• 🖥️ `ip:1.1.1.1` - Tìm kiếm theo địa chỉ IP
• 🚪 `port:80` - Tìm kiếm theo số cổng
• 🏳️ `country:US` - Tìm kiếm theo mã quốc gia
• 🌐 `hostname:example.com` - Tìm kiếm theo tên miền
• 💻 `os:"Windows 10"` - Tìm kiếm theo hệ điều hành
• 🏙️ `city:"New York"` - Tìm kiếm theo thành phố
• 🏢 `org:"Google"` - Tìm kiếm theo tổ chức

*🌐 Bộ lọc mạng:*
• 🔢 `net:192.168.0.0/16` - Tìm kiếm theo dải IP (ký hiệu CIDR)
• 🔗 `asn:AS15169` - Tìm kiếm theo Số Hệ thống Tự trị
• 📡 `isp:"Comcast"` - Tìm kiếm theo Nhà cung cấp dịch vụ Internet

*🌍 Bộ lọc web:*
• 📑 `http.title:"Index of"` - Tìm kiếm theo tiêu đề trang web
• 🟢 `http.status:200` - Tìm kiếm theo mã trạng thái HTTP
• 🧩 `http.component:"Apache"` - Tìm kiếm theo công nghệ web
• 🔒 `ssl:"Google"` - Tìm kiếm chứng chỉ SSL

*📦 Bộ lọc thiết bị & phần mềm:*
• 🛠️ `product:"Apache"` - Tìm kiếm theo tên phần mềm/sản phẩm
• 🔢 `version:"1.6.2"` - Tìm kiếm theo phiên bản phần mềm
• 🛡️ `vuln:CVE-2014-0160` - Tìm kiếm theo lỗ hổng CVE
• 🏷️ `brand:"Cisco"` - Tìm kiếm theo thương hiệu thiết bị
• 📱 `devicetype:"router"` - Tìm kiếm theo loại thiết bị

*🚀 Bộ lọc nâng cao:*
• ⏮️ `before:01/01/2023` - Kết quả trước ngày này
• ⏭️ `after:01/01/2022` - Kết quả sau ngày này
• #️⃣ `hash:-1169765817` - Tìm kiếm theo mã băm banner
• 🖼️ `has_screenshot:true` - Thiết bị có ảnh chụp màn hình
• 💰 `bitcoin.ip:any` - Các nút Bitcoin
• 🦠 `malware:wannacry` - Thiết bị nhiễm phần mềm độc hại cụ thể

*🔣 Toán tử:*
• ➕ `apache port:80` - VÀ (ngầm định)
• 🔀 `apache OR nginx` - HOẶC
• ➖ `apache -nginx` - KHÔNG
• 🔤 `"exact phrase"` - Khớp cụm từ chính xác

*💡 Mẹo sử dụng:*
• 🔗 Kết hợp các bộ lọc để tìm kiếm cụ thể hơn
• 🔠 Sử dụng dấu ngoặc kép cho cụm từ có dấu cách
• 🧮 Sử dụng dấu ngoặc đơn cho các truy vấn phức tạp

*📝 Ví dụ sử dụng:*
`/search "Apache" port:80 country:US city:"San Francisco" -"Not Found" after:01/01/2023 5`
🔍 Điều này sẽ tìm kiếm các máy chủ Apache trên cổng 80 ở San Francisco, Hoa Kỳ, loại trừ các trang 'Not Found', chỉ lấy kết quả sau ngày 1 tháng 1 năm 2023, giới hạn 5 kết quả.

*🚨 Lưu ý:* Sử dụng các bộ lọc này một cách có trách nhiệm và tuân thủ tất cả các luật và quy định hiện hành."""

        try:
            bot.send_message(message.chat.id, filters_text, parse_mode='Markdown')
        except telebot.apihelper.ApiTelegramException as e:
            if "can't parse entities" in str(e):
                # Nếu gặp lỗi parse, gửi tin nhắn không có định dạng Markdown
                bot.send_message(message.chat.id,
                                 "Xin lỗi, có lỗi xảy ra khi hiển thị bộ lọc. Dưới đây là nội dung không có định dạng:")
                bot.send_message(message.chat.id, filters_text.replace('*', '').replace('`', ''))
            else:
                # Nếu là lỗi khác, gửi thông báo lỗi
                bot.send_message(message.chat.id, "Xin lỗi, có lỗi xảy ra khi hiển thị bộ lọc. Vui lòng thử lại sau.")

        update_user_data(user_data, message.from_user.id, message.from_user.first_name)

    @bot.message_handler(commands=['cve'])
    @user_approved
    def show_cve_info(message):
        args = message.text.split(maxsplit=1)
        if len(args) < 2:
            bot.reply_to(message, "❌ Vui lòng nhập ID CVE. Ví dụ: `/cve CVE-2023-31417`", parse_mode='MarkdownV2')
            return

        cve_id = args[1]
        try:
            description = get_cve_description(cve_id)
            bot.reply_to(message, description, parse_mode='Markdown')
        except Exception as e:
            bot.reply_to(message, f"❌ Lỗi khi tìm kiếm CVE: {escape_markdown(str(e))}", parse_mode='MarkdownV2')

    @bot.message_handler(commands=['stats'])
    def show_stats(message):
        if str(message.from_user.id) != str(ADMIN_ID):
            bot.reply_to(message, "Bạn không có quyền xem thống kê.")
            return

        args = message.text.split()
        if len(args) > 1:
            user_identifier = args[1].lstrip('@')
            user_stats = get_user_stats(user_identifier, full_history=True)
            if user_stats:
                bot.send_message(message.chat.id, user_stats, parse_mode='MarkdownV2')
            else:
                bot.reply_to(message, f"Không tìm thấy thông tin cho người dùng {user_identifier}")
        else:
            stats = "*📊 Thống kê sử dụng bot*\n\n"
            for user_id, data in user_data.items():
                stats += get_user_stats_summary(user_id, data, full_history=False)

            max_length = 4096
            if len(stats) > max_length:
                parts = [stats[i:i + max_length] for i in range(0, len(stats), max_length)]
                for part in parts:
                    bot.send_message(message.chat.id, part, parse_mode='MarkdownV2')
            else:
                bot.send_message(message.chat.id, stats, parse_mode='MarkdownV2')

    @bot.message_handler(func=lambda message: True)
    def echo_all(message):
        bot.reply_to(message, "❓ Tôi không hiểu lệnh này. Vui lòng sử dụng /help để xem danh sách các lệnh có sẵn.")


def create_approval_keyboard(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("Phê duyệt", callback_data=f"approve_{user_id}"),
        InlineKeyboardButton("Từ chối", callback_data=f"deny_{user_id}")
    )
    return keyboard


def create_result_buttons(results):
    keyboard = InlineKeyboardMarkup()
    for i, result in enumerate(results):
        ip = result.get('ip_str', 'N/A')
        hostnames = result.get('hostnames', ['N/A'])
        hostname = hostnames[0] if hostnames else 'N/A'
        country = result.get('location', {}).get('country_name', 'N/A')

        hostname = (hostname[:15] + '...') if len(hostname) > 18 else hostname
        country = (country[:10] + '...') if len(country) > 13 else country

        ip_part = f"🖥️ {ip:<15}"
        hostname_part = f"🏛️ {hostname:<20}"
        country_part = f"🌍 {country:<15}"

        button_text = f"{ip_part} | {hostname_part} | {country_part}"
        keyboard.add(InlineKeyboardButton(button_text, callback_data=f"details_{i}"))
    return keyboard


def format_detailed_result(host):
    try:
        response = f"🌐 *Chi tiết về {host.get('ip_str', 'N/A')}*\n\n"
        response += f"🏛️ Tên: `{', '.join(host.get('hostnames', ['N/A']))}`\n"
        response += f"🌍 Quốc gia: `{host.get('country_name', 'N/A')}`\n"
        response += f"🏙️ Thành phố: `{host.get('city', 'N/A')}`\n"
        response += f"🏢 Tổ chức: `{host.get('org', 'N/A')}`\n\n"

        open_ports = host.get('ports', [])
        if open_ports:
            response += "🚪 *Các cổng mở:*\n"
            for port in open_ports:
                service = next((item for item in host.get('data', []) if item['port'] == port), None)
                if service:
                    response += f"   • `{port}`: {service.get('product', 'N/A')} {service.get('version', '')}\n"
                else:
                    response += f"   • `{port}`\n"
        else:
            response += "🚪 *Các cổng mở:* Không tìm thấy\n"
        response += "\n"

        vulns = host.get('vulns', [])
        if vulns:
            sorted_vulns = sorted(vulns, key=lambda x: x.split('-')[1], reverse=True)
            response += "🛡️ *Các lỗ hổng:*\n"
            for vuln in sorted_vulns[:5]:  # Giới hạn hiển thị 5 lỗ hổng đầu tiên
                response += f"   • `{vuln}`\n"
            if len(vulns) > 5:
                response += f"   ... và {len(vulns) - 5} lỗ hổng khác\n"
        else:
            response += "🛡️ *Các lỗ hổng:* Không tìm thấy\n"
        response += "\n"

        http_data = next((item for item in host.get('data', []) if item['port'] == 80 or item['port'] == 443), None)
        if http_data and 'http' in http_data:
            response += "🌐 *Công nghệ Web:*\n"
            for tech, details in list(http_data['http'].get('components', {}).items())[
                                 :5]:  # Giới hạn hiển thị 5 công nghệ đầu tiên
                response += f"   • `{tech}`: {details.get('version', 'N/A')}\n"
            if len(http_data['http'].get('components', {})) > 5:
                response += f"   ... và {len(http_data['http'].get('components', {})) - 5} công nghệ khác\n"
        else:
            response += "🌐 *Công nghệ Web:* Không có thông tin\n"

        return response
    except Exception as e:
        return f"❌ Lỗi khi định dạng kết quả: {str(e)}"


def get_user_stats(user_identifier, full_history=False):
    for user_id, data in user_data.items():
        if user_id == user_identifier or data.get('name') == user_identifier:
            return get_user_stats_summary(user_id, data, full_history)
    return None


def get_user_stats_summary(user_id, data, full_history=False):
    user_stats = (
        f"👤 *{escape_markdown(data['name'])}* \\(ID: `{user_id}`\\)\n"
        f"📅 Ngày tạo: `{format_date(data['created'])}`\n"
        f"🔢 Số lần sử dụng: `{data['usage_count']}`\n"
    )

    if data['search_history']:
        user_stats += "🔍 *Lịch sử tìm kiếm:*\n"
        history = data['search_history'] if full_history else data['search_history'][-3:]
        for search in history:
            query = escape_markdown(search['query'][:30])
            timestamp = format_date(search['timestamp'])
            user_stats += f"    • `{query}` \\[{timestamp}\\]\n"

        if not full_history and len(data['search_history']) > 3:
            user_stats += f"    \\.\\.\\. và {len(data['search_history']) - 3} tìm kiếm khác\n"

    user_stats += "\n"
    return user_stats


def user_approved(func):
    def wrapper(message):
        user_id = str(message.from_user.id)
        if user_id in user_data and user_data[user_id].get("approved", False):
            return func(message)
        else:
            bot.reply_to(message, "Bạn chưa được phê duyệt để sử dụng bot. Vui lòng đợi admin phê duyệt.")

    return wrapper

# Các hàm hỗ trợ khác có thể được thêm vào đây nếu cần

# Kết thúc file commands.py
