import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

from modules.chemistry import PeriodicModule
from modules.ideal_gas import IdealGasSim
from modules.magnetic import MagneticSim
from modules.nuclear import NuclearSim
from modules.puhh import ReactionModule


class AppController(MainWindow):
    def __init__(self):
        super().__init__()
        self.current_sim = None

        # ===== ĐĂNG KÝ MODULE =====
        self.modules = {
            "gas":     ("Khí Lý Tưởng", IdealGasSim),
            "mag":     ("Từ Trường", MagneticSim),
            "nuke":    ("Hạt Nhân", NuclearSim),
            "chem":    ("Bảng tuần hoàn", PeriodicModule),
            "chemsim":  ("Phản ứng hóa học 3D", ReactionModule),
        }

        # ===== CONNECT BUTTON =====
        for key, (label, _) in self.modules.items():
            self.btns[label].clicked.connect(
                lambda _, k=key: self.load_module(k)
            )

    # ================= UTIL =================

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def set_active_button(self, module_key):
        for btn in self.btns.values():
            btn.setObjectName("")
            btn.style().unpolish(btn)
            btn.style().polish(btn)

        label = self.modules[module_key][0]
        btn = self.btns[label]
        btn.setObjectName("Active")
        btn.style().unpolish(btn)
        btn.style().polish(btn)

    # ================= CORE =================

    def load_module(self, key):
        # Đóng sim cũ
        if self.current_sim and hasattr(self.current_sim, "plotter"):
            self.current_sim.plotter.close()
            self.current_sim = None

        # Clear UI
        self.clear_layout(self.display_layout)
        self.clear_layout(self.param_layout)

        # Load sim mới
        _, sim_class = self.modules[key]
        self.current_sim = sim_class(
            self.display_layout,
            self.param_layout
        )

        # Update UI state
        self.set_active_button(key)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppController()
    window.show()
    sys.exit(app.exec())
