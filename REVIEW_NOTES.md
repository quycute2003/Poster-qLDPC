# Ghi chú rà soát poster qLDPC v10

**Trạng thái:** PDF cuối đã qua kiểm tra kỹ thuật và kiểm tra hình ảnh. Chưa
chốt đối chiếu với đúng file bài báo được chỉ định: không tìm thấy
`final_paper_1232964_japluxhwcn2mph76_v2(2).pdf`. File hiện có là
`E:\QUY\Slide-NCKH\final_paper_1232964_japluxhwcn2mph76_v2.pdf`; đã đọc đủ
5 trang và đối chiếu tạm, nhưng chưa xác nhận hai tên là cùng một bản.
Không sử dụng poster phiên bản cũ và không tự upload website.

## Thay đổi

- Giữ thiết kế v10, tiêu đề nguyên văn hai dòng căn distributed, logo,
  Presentation ID 88, tác giả, đơn vị, email và toàn bộ đối tượng gốc.
- Sửa 5 run chỉ số dưới: `upper`, `DEM`, `cert`; sửa kích thước/baseline
  để PowerPoint hiển thị đúng. Hạ hai ký hiệu trong sơ đồ để tách khỏi nhãn.
- Mục Future work ghi “Benchmark unproven cost savings.”, làm rõ tiết kiệm
  chi phí chưa được chứng minh; giữ nguyên các kết quả khoa học.
- Bổ sung xuất PDF trực tiếp bằng PowerPoint ở print intent. Bước cuối đặt
  page box chính xác và phục hồi nguyên pixel/alpha của logo nguồn vì
  PowerPoint thay đổi màu ở các pixel bán trong suốt. Không rasterize trang.

## Đối chiếu nội dung

Các mục dưới khớp checklist người dùng và file `v2.pdf` hiện có:

| Nội dung | Kết quả | Vị trí trong v2.pdf |
|---|---|---|
| Ngân hàng, development, confirmatory | 32; BB72/90/144/288; 28 | Trang 2, Table I |
| Điểm vận hành | p=0.003; 6 rounds; X-basis; SI1000 | Trang 2, Table I |
| Schedule, decoder, budget | EdgeColoringXZ/smallest-last; product-sum BP 32 iterations; OSD-CS order 10; 20,000 × 32=640,000 shots; no early stop | Trang 2–3 |
| Screen | Cận trên đã kiểm chứng; đếm cơ chế lỗi DEM; không phải exact code/DEM distance | Trang 3, II.B |
| Coverage | 24/32; 22/28; 6/28 confirmatory không có hạng | Trang 2, 4 |
| Cặp so sánh | 231 có thể; 226 ordered; 5 unordered | Trang 4, Table II |
| Đồng thuận/hòa/nghịch | 148/45/33; 65.5%/19.9%/14.6% | Trang 4, Table II |
| Điểm C | (148+0.5×45)/226=0.7544; mốc 0.5 | Trang 3–4 |
| Khoảng ổn định | 95% code-resampling stability interval [0.6262,0.8382]; không phải shot-noise hoặc superpopulation confidence interval | Trang 3–4 |
| Hình 2 | Chiều thuận, trục, các điểm và Wilson bars khớp hình bài báo; không dựng lại dữ liệu | Trang 4, Fig. 2 |
| Kết luận/phạm vi | Xếp hạng thô; BP+OSD-dependent; một điểm; triage tiềm năng; chưa chứng minh tiết kiệm chi phí; không dự đoán LER tuyệt đối | Trang 4–5 |

C không có nghĩa “75% số cặp đúng thứ tự”; hòa nhận nửa điểm. Các phần trăm
148/45/33 dùng mẫu số 226, không dùng 231.

## Kiểm tra PDF cuối

- Một trang, MediaBox/CropBox 75 × 120 cm, chiều dọc, PDF 1.7, RGB; không
  áp dụng PDF/X, CMYK hoặc nén mạnh. Dung lượng 203,930 byte, khoảng 199 KiB.
- Cả 4 font resources đều nhúng subset DejaVu Sans Regular/Bold; không có
  font thay thế. Chữ tìm kiếm/sao chép được, dấu mũ không còn ký tự điều khiển.
- 3,596 ký tự văn bản; đường, khung, bảng và sơ đồ vẫn là vector. PPTX giữ
  hai bảng native và đúng tập shape ID của v10.
- Render chính PDF cuối ở preview 3,000 px; kiểm tra toàn trang và crop 150 dpi
  ở tiêu đề, ký hiệu/chỉ số dưới, mũi tên, FREEZE BOUNDARY, đồ thị/chú thích,
  khung kết quả, mục 5 và chân trang. Không phát hiện chồng/cắt chữ sau sửa.
- Biểu đồ 3568 × 2416 px: 274.63 dpi hiệu dụng; logo 254 × 108 px: 86.02 dpi.
  Hai ảnh trong PDF khớp nguyên từng pixel RGBA với PNG nguồn; không giảm
  kích thước, không dùng JPEG. Preview không được dùng để tạo PDF.

## Giới hạn còn lại

Logo xanh vẫn có độ phân giải thấp. Đã kiểm tra flyer và slide template
chính thức: flyer chứa đúng bản xanh 254 × 108 px; template chỉ có bản trắng
365 × 153 px. Chưa tìm thấy bản xanh vector/chất lượng cao hơn giữ đúng
nhận diện đã duyệt. Không phóng lớn, vẽ lại hoặc dùng AI để tạo logo.

Nguồn chính thức đã kiểm tra:
[hướng dẫn và template](https://asiancomnet2026.aconf.org/news/8493.html),
[flyer](https://file.aconf.org/conf/hk/2026/01/229273/files/ASIANComNet%202026%20Flyer_0928.pdf).

PPTX cần DejaVu Sans trên máy chỉnh sửa; font và giấy phép đi kèm source.
PDF đã nhúng font và không cần cài font trên máy xem/upload.
