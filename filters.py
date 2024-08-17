FILTER_EXPLANATIONS = {
    "ip": {
        "example": "ip:8.8.8.8",
        "explanation": "Bộ lọc này tìm kiếm một địa chỉ IP cụ thể. Ví dụ, `ip:8.8.8.8` sẽ tìm thông tin về máy chủ DNS công cộng của Google.",
        "sample_query": "/search ip:8.8.8.8 5"
    },
    "port": {
        "example": "port:80",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có một cổng cụ thể đang mở. Ví dụ, `port:80` sẽ tìm các thiết bị có cổng HTTP mở, có thể là các máy chủ web.",
        "sample_query": "/search port:80 country:VN 10"
    },
    "country": {
        "example": "country:VN",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị ở một quốc gia cụ thể. Ví dụ, `country:VN` sẽ tìm các thiết bị đặt tại Việt Nam.",
        "sample_query": "/search country:VN apache 15"
    },
    "hostname": {
        "example": "hostname:example.com",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có tên miền cụ thể. Ví dụ, `hostname:example.com` sẽ tìm các thiết bị liên kết với tên miền example.com.",
        "sample_query": "/search hostname:gov.vn 5"
    },
    "os": {
        "example": "os:\"Windows 10\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị chạy một hệ điều hành cụ thể. Ví dụ, `os:\"Windows 10\"` sẽ tìm các thiết bị đang chạy Windows 10.",
        "sample_query": "/search os:\"Windows 10\" country:VN 10"
    },
    "city": {
        "example": "city:\"Ho Chi Minh City\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị ở một thành phố cụ thể. Ví dụ, `city:\"Ho Chi Minh City\"` sẽ tìm các thiết bị đặt tại Thành phố Hồ Chí Minh.",
        "sample_query": "/search city:\"Ho Chi Minh City\" port:443 8"
    },
    "org": {
        "example": "org:\"FPT Telecom\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị thuộc về một tổ chức cụ thể. Ví dụ, `org:\"FPT Telecom\"` sẽ tìm các thiết bị thuộc sở hữu hoặc vận hành bởi FPT Telecom.",
        "sample_query": "/search org:\"Viettel\" country:VN 12"
    },
    "net": {
        "example": "net:192.168.0.0/16",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị trong một dải IP cụ thể sử dụng ký hiệu CIDR. Ví dụ, `net:192.168.0.0/16` sẽ tìm các thiết bị trong dải từ 192.168.0.0 đến 192.168.255.255.",
        "sample_query": "/search net:203.113.128.0/18 country:VN 7"
    },
    "asn": {
        "example": "asn:AS15169",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị liên kết với một Số Hệ thống Tự trị (ASN) cụ thể. Ví dụ, `asn:AS15169` sẽ tìm các thiết bị trong ASN của Google.",
        "sample_query": "/search asn:AS45899 product:\"Apache\" 10"
    },
    "isp": {
        "example": "isp:\"VNPT\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị liên kết với một Nhà cung cấp dịch vụ Internet (ISP) cụ thể. Ví dụ, `isp:\"VNPT\"` sẽ tìm các thiết bị sử dụng VNPT làm ISP.",
        "sample_query": "/search isp:\"FPT Telecom\" country:VN 15"
    },
    "http.title": {
        "example": "http.title:\"Index of\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có tiêu đề cụ thể trong phản hồi HTTP. Ví dụ, `http.title:\"Index of\"` có thể tìm thấy các máy chủ có chức năng liệt kê thư mục được bật.",
        "sample_query": "/search http.title:\"Welcome to nginx\" 10"
    },
    "http.status": {
        "example": "http.status:200",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị trả về mã trạng thái HTTP cụ thể. Ví dụ, `http.status:200` sẽ tìm các máy chủ web trả về phản hồi thành công.",
        "sample_query": "/search http.status:404 org:\"VNG Corporation\" 8"
    },
    "http.component": {
        "example": "http.component:\"Apache\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị sử dụng một công nghệ hoặc thành phần web cụ thể. Ví dụ, `http.component:\"Apache\"` sẽ tìm các máy chủ web chạy Apache.",
        "sample_query": "/search http.component:\"WordPress\" country:VN 12"
    },
    "ssl": {
        "example": "ssl:\"Google\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có chứng chỉ SSL chứa văn bản cụ thể. Ví dụ, `ssl:\"Google\"` có thể tìm thấy các thiết bị có chứng chỉ SSL do Google cấp.",
        "sample_query": "/search ssl:\"Let's Encrypt\" country:VN 10"
    },
    "product": {
        "example": "product:\"Apache\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị chạy một sản phẩm phần mềm cụ thể. Ví dụ, `product:\"Apache\"` sẽ tìm các thiết bị chạy máy chủ web Apache.",
        "sample_query": "/search product:\"nginx\" os:\"Ubuntu\" 15"
    },
    "version": {
        "example": "version:\"1.6.2\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị chạy một phiên bản phần mềm cụ thể. Ví dụ, `version:\"1.6.2\"` có thể tìm thấy các thiết bị chạy một phiên bản cụ thể của một phần mềm.",
        "sample_query": "/search product:\"OpenSSH\" version:\"7.4\" 10"
    },
    "vuln": {
        "example": "vuln:CVE-2014-0160",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị dễ bị tổn thương với một CVE (Common Vulnerabilities and Exposures) cụ thể. Ví dụ, `vuln:CVE-2014-0160` sẽ tìm các thiết bị có thể bị ảnh hưởng bởi lỗ hổng Heartbleed.",
        "sample_query": "/search vuln:CVE-2014-0160 country:VN 20"
    },
    "brand": {
        "example": "brand:\"Cisco\"",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị của một thương hiệu cụ thể. Ví dụ, `brand:\"Cisco\"` sẽ tìm các thiết bị Cisco.",
        "sample_query": "/search brand:\"Huawei\" country:VN 8"
    },
    "devicetype": {
        "example": "devicetype:\"router\"",
        "explanation": "Bộ lọc này tìm kiếm các loại thiết bị cụ thể. Ví dụ, `devicetype:\"router\"` sẽ tìm các thiết bị được xác định là bộ định tuyến.",
        "sample_query": "/search devicetype:\"webcam\" country:VN 12"
    },
    "before": {
        "example": "before:01/01/2023",
        "explanation": "Bộ lọc này tìm kiếm kết quả từ trước một ngày cụ thể. Ví dụ, `before:01/01/2023` sẽ tìm kết quả được lập chỉ mục trước ngày 1 tháng 1 năm 2023.",
        "sample_query": "/search apache before:01/01/2023 country:VN 10"
    },
    "after": {
        "example": "after:01/01/2022",
        "explanation": "Bộ lọc này tìm kiếm kết quả từ sau một ngày cụ thể. Ví dụ, `after:01/01/2022` sẽ tìm kết quả được lập chỉ mục sau ngày 1 tháng 1 năm 2022.",
        "sample_query": "/search nginx after:01/01/2022 country:VN 15"
    },
    "hash": {
        "example": "hash:-1169765817",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có một mã băm banner cụ thể. Mã băm hữu ích để tìm các thiết bị có banner hoặc đặc điểm giống hệt nhau.",
        "sample_query": "/search hash:-1169765817 10"
    },
    "has_screenshot": {
        "example": "has_screenshot:true",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có ảnh chụp màn hình liên quan trong cơ sở dữ liệu của Shodan. Điều này có thể hữu ích để xác nhận trực quan bản chất của một dịch vụ.",
        "sample_query": "/search has_screenshot:true product:\"webcam\" 8"
    },
    "bitcoin.ip": {
        "example": "bitcoin.ip:any",
        "explanation": "Bộ lọc này tìm kiếm các nút Bitcoin. Sử dụng `bitcoin.ip:any` sẽ tìm bất kỳ thiết bị nào có vẻ là một phần của mạng Bitcoin.",
        "sample_query": "/search bitcoin.ip:any country:VN 10"
    },
    "malware": {
        "example": "malware:wannacry",
        "explanation": "Bộ lọc này tìm kiếm các thiết bị có khả năng bị nhiễm phần mềm độc hại cụ thể. Ví dụ, `malware:wannacry` có thể tìm thấy các thiết bị có dấu hiệu nhiễm ransomware WannaCry.",
        "sample_query": "/search malware:wannacry country:VN 20"
    }
}