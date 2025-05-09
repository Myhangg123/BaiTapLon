#  Dự án Tự Động Thu Thập Tin Tức từ DanTri

##  Giới thiệu
Chương trình này tự động thu thập tin tức từ chuyên mục **Tài chính** của báo **Dân trí** tại địa chỉ:  
🔗 https://dantri.com.vn/kinh-doanh/tai-chinh.htm

Dữ liệu bao gồm: **tiêu đề**, **mô tả**, **ảnh đại diện**, và **nội dung bài viết**, được lưu lại dưới dạng file Excel. Chương trình được thiết kế chạy **tự động mỗi ngày vào lúc 6h sáng**.

---

##  Các thư viện được sử dụng

- `requests` – Gửi HTTP request đến các trang.
- `beautifulsoup4` – Phân tích và trích xuất HTML.
- `pandas` – Xử lý và lưu dữ liệu dưới dạng bảng.
- `openpyxl` – Ghi dữ liệu ra file Excel (.xlsx).
- `schedule` – Thiết lập lịch chạy tự động.
- `random`, `time`, `datetime`, `urllib.parse` – Thư viện chuẩn.

---

##  Các bước hoạt động của chương trình

1. **Mở trang web Dân trí** chuyên mục Tài chính.
2. **Duyệt qua từng trang tin** (trang 1, trang 2, …) cho đến khi không còn trang.
3. **Lấy tối đa 5 bài viết đầu tiên mỗi trang**, bao gồm:
   - Tiêu đề
   - Mô tả (meta description)
   - Ảnh đại diện (og:image)
   - Nội dung bài báo (tag `<article>`)
4. **Lưu dữ liệu vào file Excel** `dantri_articles.xlsx`.
5. **In thống kê số bài viết mỗi trang**.
6. **Chạy lại tự động vào 6h sáng mỗi ngày.**

---

##  Cài đặt

### 1. Clone project về máy

```bash
git clone https://github.com/yourusername/dantri-news-crawler.git
cd dantri-news-crawler
