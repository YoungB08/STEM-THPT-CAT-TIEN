import pyvista as pv
import numpy as np
from pyvistaqt import BackgroundPlotter
from PyQt6.QtWidgets import QLabel, QSlider, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt


class NuclearSim:
    def __init__(self, display_layout, param_layout):
        # ===== PLOTTER =====
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.set_background("#020617")
        display_layout.addWidget(self.plotter.interactor)

        # ===== THAM SỐ =====
        self.n_atoms = 500
        self.lambda_val = 0.05
        self.dt = 0.05
        self.time = 0.0

        self.sample_radius = 1.4
        self.gamma_length = 2.5
        self.gamma_ttl = 6
        self.show_gamma = True

        self.point_size = 10

        # ===== INIT =====
        self.init_atoms()

        # ===== UI =====
        self.build_ui(param_layout)

        # ===== LOOP =====
        self.plotter.add_callback(self.update, interval=60)

    # ================= INIT =================

    def init_atoms(self):
        self.time = 0.0
        self.pos = np.random.normal(0, self.sample_radius, (self.n_atoms, 3))
        self.active = np.ones(self.n_atoms, dtype=np.float32)

        self.decay_time = np.random.exponential(
            1 / self.lambda_val, self.n_atoms
        )

        self.mesh = pv.PolyData(self.pos)
        self.mesh["active"] = self.active

        if hasattr(self, "actor"):
            self.plotter.remove_actor(self.actor)

        self.actor = self.plotter.add_mesh(
            self.mesh,
            scalars="active",
            clim=[0, 1],
            cmap="Reds",
            render_points_as_spheres=True,
            point_size=self.point_size,
        )

        self.rays = []

    # ================= UI =================

    def section(self, layout, title):
        frame = QFrame()
        frame.setObjectName("Section")
        v = QVBoxLayout(frame)
        t = QLabel(title)
        t.setObjectName("SectionTitle")
        v.addWidget(t)
        layout.addWidget(frame)
        return v

    def slider(self, layout, text, minv, maxv, val):
        layout.addWidget(QLabel(text))
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(minv, maxv)
        s.setValue(val)
        layout.addWidget(s)
        return s

    def build_ui(self, layout):
        # ===== NUCLEAR =====
        sec = self.section(layout, "PHÂN RÃ HẠT NHÂN")

        self.s_n = self.slider(sec, "SỐ HẠT NHÂN (N)", 100, 1500, self.n_atoms)
        self.s_lambda = self.slider(sec, "HẰNG SỐ PHÂN RÃ (λ)", 1, 100, 20)
        self.s_dt = self.slider(sec, "BƯỚC THỜI GIAN (dt)", 1, 200, 50)

        self.lbl_alive = QLabel("CÒN LẠI: 100%")
        self.lbl_alive.setObjectName("Pressure")
        sec.addWidget(self.lbl_alive)

        # ===== GAMMA =====
        sec = self.section(layout, "TIA GAMMA")

        self.s_gamma_len = self.slider(sec, "ĐỘ DÀI TIA", 10, 60, 25)
        self.s_gamma_ttl = self.slider(sec, "THỜI GIAN TỒN TẠI", 1, 20, self.gamma_ttl)

        # ===== DISPLAY =====
        sec = self.section(layout, "HIỂN THỊ")

        self.s_size = self.slider(sec, "KÍCH THƯỚC HẠT", 4, 20, self.point_size)
        self.s_radius = self.slider(sec, "BÁN KÍNH MẪU", 5, 30, int(self.sample_radius * 10))

    # ================= UPDATE =================

    def update(self):
        # ===== PARAM UPDATE =====
        self.n_atoms = self.s_n.value()
        self.lambda_val = max(self.s_lambda.value() / 400, 0.001)
        self.dt = self.s_dt.value() / 1000
        self.gamma_length = self.s_gamma_len.value() / 10
        self.gamma_ttl = self.s_gamma_ttl.value()
        self.point_size = self.s_size.value()
        self.sample_radius = self.s_radius.value() / 10

        if len(self.active) != self.n_atoms:
            self.init_atoms()
            return

        self.actor.prop.point_size = self.point_size

        self.time += self.dt

        # ===== DECAY =====
        decayed = (self.active > 0) & (self.time >= self.decay_time)

        for idx in np.where(decayed)[0]:
            self.active[idx] = 0.0

            if self.show_gamma:
                start = self.pos[idx]
                direction = np.random.randn(3)
                direction /= np.linalg.norm(direction)
                end = start + direction * self.gamma_length

                ray = pv.Line(start, end)
                actor = self.plotter.add_mesh(
                    ray, color="#38bdf8", line_width=2
                )
                self.rays.append([actor, self.gamma_ttl])

        self.mesh["active"] = self.active

        # ===== GAMMA TTL =====
        alive = []
        for actor, ttl in self.rays:
            if ttl > 0:
                alive.append([actor, ttl - 1])
            else:
                self.plotter.remove_actor(actor)
        self.rays = alive

        # ===== STATS =====
        alive_ratio = np.mean(self.active) * 100
        self.lbl_alive.setText(f"CÒN LẠI: {alive_ratio:.1f}%")

        if not np.any(self.active):
            self.actor.visibility = False
