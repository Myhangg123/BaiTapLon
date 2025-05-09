import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from urllib.parse import urljoin
from datetime import datetime
import schedule

def fetch_all_pages():
    # Bước 1: Vào website đã chọn (chọn mục "Kinh doanh - Tài chính" trên báo Dân trí)
    base_url = "https://dantri.com.vn/kinh-doanh/tai-chinh.htm"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    data = []
    seen_titles = set()
    page_num = 1
    page_stats = {}

    while True:
        # Bước 2: Click chọn một mục tin tức bất kỳ (ở đây là phân trang từng mục tin)
        url = base_url if page_num == 1 else base_url.replace('.htm', f'/trang-{page_num}.htm')
        print(f" Đang xử lý trang {page_num}: {url}")

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 404:
                print(f" Trang {page_num} không tồn tại. Đã quét xong toàn bộ.")
                break
            response.raise_for_status()
        except Exception as e:
            print(f" Lỗi truy cập {url}, lý do: {e}")
            break

        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.find_all('h3', class_='article-title')

        page_stats[page_num] = len(articles)

        if not articles:
            print(f" Trang {page_num} không có bài viết (trang trắng).")
            break

        count = 0
        for article in articles:
            if count >= 5:
                break

            a_tag = article.find('a')
            if not a_tag:
                continue

            title = a_tag.get_text(strip=True)
            if title in seen_titles:
                continue
            seen_titles.add(title)

            link = urljoin(base_url, a_tag['href'])

            try:
                # Bước 4: Lấy tất cả dữ liệu hiển thị trong bài viết (Tiêu đề, Mô tả, Hình ảnh, Nội dung)
                article_page = requests.get(link, headers=headers)
                article_page.raise_for_status()
                article_soup = BeautifulSoup(article_page.text, 'html.parser')

                description_tag = article_soup.find('meta', {'name': 'description'})
                description = description_tag['content'] if description_tag else 'Không có mô tả'

                image_tag = article_soup.find('meta', {'property': 'og:image'})
                image = image_tag['content'] if image_tag else 'Không có hình ảnh'

                article_tag = article_soup.find('article')
                content = article_tag.get_text(separator='\n', strip=True) if article_tag else 'Không có nội dung'

                data.append([title, description, image, content])
                count += 1

            except Exception as e:
                print(f" Lỗi khi lấy bài: {title} | Lý do: {e}")
                continue

        # Bước 5: Lấy tất cả dữ liệu của các trang (duyệt lần lượt từng trang)
        page_num += 1
        time.sleep(random.uniform(1, 2))

    # Bước 6: Lưu dữ liệu đã lấy được vào file Excel (có thể thay bằng CSV nếu muốn)
    file_excel = f'dantri_articles.xlsx'
    if data:
        try:
            df = pd.DataFrame(data, columns=['Tiêu đề', 'Mô tả', 'Hình ảnh', 'Nội dung'])
            df.to_excel(file_excel, index=False, engine='openpyxl')
            print(f"\n  Đã lưu {len(data)} bài viết vào {file_excel}")
        except PermissionError:
            print(f"\n Không thể ghi file '{file_excel}'. Vui lòng đóng file Excel nếu đang mở.")
    else:
        print("\n Không có dữ liệu để lưu.")

    print("\n Thống kê số bài viết trên từng trang:")
    for page, count in page_stats.items():
        print(f"- Trang {page}: {count} bài viết")

# Bước 7: Set lịch chạy tự động lúc 6h sáng mỗi ngày (thay 12:58 bằng 06:00 khi chạy thực tế)
schedule.every().day.at("06:00").do(fetch_all_pages)

# Vòng lặp giữ chương trình chạy để thực thi theo lịch
if __name__ == "__main__":
    print(" Đang chờ đến 6h sáng mỗi ngày để bắt đầu thu thập tin tức Dantri...")
    while True:
        schedule.run_pending()
        time.sleep(60)
