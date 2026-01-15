
Chào bạn, đây là bản README.md được thiết kế chuyên nghiệp, hiện đại và bám sát giao diện Dark Mode/Neon của ứng dụng mà bạn đang phát triển cho CLB STEM Trường THPT Cát Tiên.

🌌 THPT CÁT TIÊN - PHYSICS & CHEMISTRY 3D SIMULATION
Ứng dụng mô phỏng vật lý và hóa học 3D được phát triển bởi CLB STEM Trường THPT Cát Tiên. Công cụ này hỗ trợ học sinh và giáo viên trực quan hóa các khái niệm khoa học phức tạp thông qua môi trường tương tác 3D thời gian thực.

✨ Tính năng nổi bật
Ứng dụng được chia thành các phân hệ chuyên biệt dành cho chương trình Vật Lý và Hóa Học lớp 12:

🔬 Phân hệ Vật Lý 12
Khí Lý Tưởng: Mô phỏng chuyển động của các hạt khí, áp suất và nhiệt độ trong bình kín.

Từ Trường: Trực quan hóa đường sức từ và tương tác của các hạt điện tích.

Hạt Nhân: Mô phỏng cấu trúc hạt nhân và các phản ứng phân rã.

🧪 Phân hệ Hóa Học 3D
Bảng Tuần Hoàn 3D: Tra cứu đầy đủ 118 nguyên tố với thông tin chi tiết (Z, Shells, Orbital, TCVL, TCHH).

Phản Ứng Hóa Học 3D: Thư viện hơn 1000 phản ứng phổ biến với cấu trúc phân tử thực tế.

Toán Học 3D: Vẽ đồ thị hàm số y=f(x) và tương tác với các điểm, đường thẳng trong không gian Oxyz.

🛠 Công nghệ sử dụng
Ứng dụng được xây dựng trên nền tảng Python hiện đại:

PyQt6: Thiết kế giao diện người dùng (GUI) với phong cách Glassmorphism.

PyVista & VTK: Xử lý đồ họa và render mô hình 3D hiệu năng cao.

NumPy: Tính toán tọa độ và xử lý dữ liệu ma trận.

🚀 Cấu trúc dữ liệu Phản ứng
Dữ liệu phản ứng được chuẩn hóa dưới dạng JSON giúp việc mở rộng dễ dàng:

JSON
{
    "equation": "2 H2 + O2 → 2 H2O",
    "type": "Combustion",
    "molecules": {
        "H2O": [[0,0,0], [0.96,0,0], [-0.24,0.92,0]]
    }
}
📦 Cài đặt
Yêu cầu hệ thống: Python 3.9 trở lên.

Cài đặt thư viện:

Bash
pip install PyQt6 pyvistaqt pyvista numpy
Chạy ứng dụng:

Bash
python main.py
🎨 Giao diện người dùng
Giao diện được tối ưu hóa cho trải nghiệm Dark Theme:

Bảng điều khiển (Sidebar): Điều hướng nhanh giữa các chế độ mô phỏng.

Khung hiển thị (Display Area): Tương tác xoay, thu phóng mô hình 3D bằng chuột.

Bảng thông số (Control Panel): Tinh chỉnh các tham số đầu vào (Slider, Input) và xem thông tin chi tiết.

👨‍💻 Phát triển bởi
CLB STEM - Trường THPT Cát Tiên

Dự án: Mô phỏng Vật lý & Hóa học 12.

Tác giả: Trần Khôi Nguyên & Chu Đức Anh Kiệt.

© 2024 THPT Cát Tiên. Mọi quyền được bảo lưu.