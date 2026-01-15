from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from ui.style import MAIN_STYLE

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("THPT CÁT TIÊN – Physics 3D")
        self.setStyleSheet(MAIN_STYLE)
        self.resize(1280, 720)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # ================= SIDEBAR =================
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(260)

        side = QVBoxLayout(sidebar)
        side.setContentsMargins(18, 18, 18, 18)
        side.setSpacing(16)

        title = QLabel("⚛ THPT CÁT TIÊN\nCLB STEM")
        title.setObjectName("Title")
        side.addWidget(title)

        subtitle = QLabel("THPT CÁT TIÊN\nMô phỏng Vật Lý 12")
        subtitle.setStyleSheet("color:#64748b;")
        side.addWidget(subtitle)

        side.addSpacing(12)

        self.btns = {}
        for name in ["Khí Lý Tưởng", "Từ Trường", "Hạt Nhân", "Bảng tuần hoàn", "Phản ứng hóa học 3D"]:
            btn = QPushButton(f"  {name}")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            side.addWidget(btn)
            self.btns[name] = btn

        side.addStretch()

        author = QLabel(
            "Author\n"
            "Trần Khôi Nguyên\n"
            "Chu Đức Anh Kiệt"
        )
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)
        author.setStyleSheet("color:#475569; font-size:11px;")
        side.addWidget(author)

        root.addWidget(sidebar)

        # ================= DISPLAY =================
        self.display_container = QWidget()
        self.display_layout = QVBoxLayout(self.display_container)
        self.display_layout.setContentsMargins(0, 0, 0, 0)
        root.addWidget(self.display_container, 1)

        # ================= CONTROL PANEL =================
        self.controls = QFrame()
        self.controls.setObjectName("ControlPanel")
        self.controls.setFixedWidth(300)

        self.param_layout = QVBoxLayout(self.controls)
        self.param_layout.setContentsMargins(16, 16, 16, 16)
        self.param_layout.setSpacing(14)

        root.addWidget(self.controls)
