# PVD Steganography - Pixel Value Differencing

Một thư viện Python implementation của thuật toán **Pixel Value Differencing (PVD)** để ẩn text vào trong hình ảnh một cách bảo mật và không thể phát hiện bằng mắt thường.

## 📋 Mô tả

PVD Steganography sử dụng sự khác biệt giữa các pixel liền kề để ẩn dữ liệu. Thuật toán này:
- Ẩn nhiều hoặc ít bits tùy thuộc vào độ khác biệt pixel (vùng smooth ít bits, vùng edge nhiều bits)
- Duy trì chất lượng hình ảnh cao
- Khó phát hiện bằng các phương pháp phân tích thông thường

## 🚀 Tính năng

- ✅ Embed text vào hình ảnh
- ✅ Extract text từ hình ảnh đã embed
- ✅ Error handling chi tiết
- ✅ Progress tracking khi extract
- ✅ Tự động thêm end marker để phát hiện cuối dữ liệu
- ✅ Hỗ trợ các định dạng hình ảnh phổ biến (PNG, JPG, BMP)

## 📦 Cài đặt

### Yêu cầu hệ thống
- Python
- pip (Python package manager)

### Cài đặt dependencies

```bash
# Cài đặt các package cần thiết (CD vào thư mục implementation, sau đó chạy command sau)
pip install -r requirements.txt
```

## 🛠️ Cấu trúc thư mục

```
PVD Application/
├── .venv
└── implementation/
    └── meth/
        └── pvd.py
    ├── main.py
    ├── steganography.py
    └── requirements.txt
└── README.md
```

## 🔧 Tham số và cấu hình

### Range Table (có thể tùy chỉnh)
```python
# Bảng phạm vi định nghĩa các khoảng sai khác điểm ảnh và số bit có thể lưu trữ:
# Sai khác nhỏ (vùng mượt) lưu ít bit hơn để giữ chất lượng hình ảnh
# Sai khác lớn (vùng biên, cạnh) có thể lưu nhiều bit hơn vì thay đổi ít bị nhận thấy
RANGE_TABLE = ( 
    (0, 7),    # vùng mượt: 3 bit - ảnh hưởng thị giác tối thiểu
    (8, 15),   # vùng hơi có kết cấu: 3 bit - vẫn giữ chất lượng
    (16, 31),  # vùng có nhiều kết cấu: 4 bit - dung lượng trung bình
    (32, 63),  # bắt đầu có cạnh: 5 bit - dung lượng cao hơn
    (64, 127), # cạnh rõ: 6 bit - chứa được nhiều dữ liệu hơn
    (128, 255) # thay đổi mạnh: 7 bit - dung lượng tối đa
)
```
