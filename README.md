# Mã nguồn poster qLDPC — v10

Poster 75 × 120 cm, nền trắng, chữ đen, tiêu đề mục xanh hội nghị và khung cam đất.
Bản này đã **căn đều hai bên tiêu đề**, có logo ASIANComNet 2026, hai bảng chỉnh sửa được,
sơ đồ native và mục **Conclusion / Scope / Future work** của v8.

## Các file

- `generate_poster.py`: tạo PPTX và tùy chọn xuất PDF/PNG; chỉ dùng thư viện chuẩn Python.
- `poster.json`: nội dung, vị trí và căn chữ của các đối tượng trên poster.
- `src/pptx/`: toàn bộ nguồn Office Open XML của poster, gồm bảng, sơ đồ,
  rich text cho chỉ số dưới, logo và ảnh scatter gốc. Đây là nguồn bố cục;
  script đóng gói các phần này thành PPTX rồi áp dụng cấu hình JSON.
- `fonts/`: DejaVu Sans Regular/Bold và giấy phép để cài trên máy chưa có font.

Gói chạy độc lập, không cần file v3/v4/v8, tài khoản ChatGPT hoặc đường dẫn trên máy đã tạo poster.
Giữ cả thư mục `src/` khi commit; riêng file Python chưa đủ để dựng poster.

## Chạy

Cần **Python 3.9 trở lên**. Không phải cài package bằng pip.

```bash
python generate_poster.py
```

Kết quả: `build/qldpc_poster_v10.pptx`.

Để xuất PDF, cài LibreOffice và cài hai font trong `fonts/` trước:

```bash
python generate_poster.py --pdf
```

Trên Windows, script tự tìm LibreOffice ở thư mục Program Files thông thường.
Nếu cần chỉ định đường dẫn khác:

```powershell
python generate_poster.py --pdf --soffice "C:\Program Files\LibreOffice\program\soffice.exe"
```

Để xuất thêm ảnh xem trước, cài Poppler (`pdftoppm`) và thêm vào PATH:

```bash
python generate_poster.py --pdf --preview
```

Linux (Debian/Ubuntu):

```bash
sudo apt install libreoffice poppler-utils fonts-dejavu-core
python3 generate_poster.py --pdf --preview
```

Trên Windows, mở từng font `.ttf` trong `fonts/`, chọn Install rồi khởi động lại LibreOffice.
Bạn cũng có thể mở PPTX bằng PowerPoint và Export PDF thủ công.
PDF có thể khác chút về font metrics giữa PowerPoint và LibreOffice; kiểm tra trước khi in.

## Chỉnh nội dung và bố cục

Mở `poster.json`. Đối tượng `title` là tiêu đề; `alignment` đã đặt là `distributed`.
Các đối tượng khác có ID cố định và tên để tìm nhanh.

- `text`: nội dung; `\n` tạo dòng mới.
- `position`: `x`, `y`, `width`, `height` theo lưới thiết kế **1500 × 2400**.
  Một đơn vị tương ứng 0,05 cm.
- `alignment`: `left`, `distributed`, `right`, `justify` hoặc `distributed`.
- Có thể thêm `font_size_pt` để đổi cỡ chữ theo **point PowerPoint**.
  Cỡ 19 đơn vị thiết kế tương ứng khoảng 26,93 pt trên poster này.
- Có thể thêm `color`, ví dụ `"0B2A4A"`, để đổi màu chữ.

Ví dụ phần tiêu đề:

```json
"alignment": "distributed"
```

Tiêu đề dùng hai dòng cân độ dài, căn `distributed` để giãn đều hai mép của từng dòng.
Giữ dấu ngắt dòng nếu muốn giữ đúng bố cục bản đã duyệt.
Với công thức có chỉ số dưới và tiêu đề giãn đều, giữ nội dung JSON hiện tại để bảo toàn rich text.
Tiêu đề có khoảng trắng được giãn bằng các run riêng để PDF cũng thẳng hai mép.
Nếu đổi chính tiêu đề, sửa trên PowerPoint hoặc cập nhật các run trong XML rồi kiểm tra lại PDF.
Nếu đổi chính công thức, sửa các run trong `src/pptx/ppt/slides/slide1.xml`
hoặc sửa trên PowerPoint. Thay text công thức bằng chuỗi thường sẽ mất định dạng riêng của từng run.
Bảng nằm trong XML nguồn; cấu hình JSON hiện chỉ hỗ trợ các hộp chữ và vị trí đối tượng.
Mọi chỉnh sửa độ dài chữ/cỡ chữ cần được kiểm tra lại bằng PDF hoặc ảnh xem trước.

## Đưa lên repo

Giải nén gói này vào một thư mục trong repo, rồi chạy thử:

```bash
python generate_poster.py --pdf --preview
git add generate_poster.py poster.json README.md src fonts .gitignore
git commit -m "Add reproducible qLDPC conference poster source"
```

Thư mục `build/` được bỏ qua trong `.gitignore`. Nếu repo cần lưu bản PDF đã duyệt,
copy riêng PDF sang thư mục tài liệu của repo rồi commit file đó.
Gói này không tự commit hoặc push.

## Nguồn tài nguyên

Scatter plot giữ từ poster nghiên cứu gốc; sơ đồ và bảng là đối tượng PowerPoint native.
Logo và màu hội nghị lấy từ flyer/template chính thức ASIANComNet 2026:
https://asiancomnet2026.aconf.org/news/8493.html

Font DejaVu được phân phối kèm theo giấy phép trong `fonts/LICENSE-DejaVu.txt`.
Nội dung khoa học dựa trên bài “A Prospective Rank Test of a Detector-Error-Model Weight Screen
for Circuit-Level qLDPC Decoding”. Đồ thị là ảnh gốc, không có dữ liệu từng điểm để dựng lại scatter.
