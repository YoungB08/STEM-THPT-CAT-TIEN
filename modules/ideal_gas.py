import pyvista as pv
import numpy as np
from pyvistaqt import BackgroundPlotter
from PyQt6.QtWidgets import QLabel, QSlider, QVBoxLayout
from PyQt6.QtCore import Qt


class IdealGasSim:
    def __init__(self, display_layout, param_layout):
        # ===== Plotter =====
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.set_background("#020205")
        display_layout.addWidget(self.plotter.interactor)

        # ===== Tham số mặc định =====
        self.n = 150
        self.mass = 1.0
        self.radius = 0.04
        self.e = 1.0
        self.dt = 0.02
        self.v_scale = 1.0

        self.init_particles()

        # ===== Box =====
        self.box = pv.Box(bounds=(-1, 1, -1, 1, -1, 1))
        self.box_actor = self.plotter.add_mesh(
            self.box, style="wireframe", color="#3b82f6"
        )

        # ===== UI =====
        self.build_ui(param_layout)

        # ===== Update loop =====
        self.plotter.add_callback(self.update, interval=16)

    # ================= INIT =================

    def init_particles(self):
        self.pos = np.random.uniform(-self.v_scale, self.v_scale, (self.n, 3))
        self.vel = np.random.normal(0, 0.6, (self.n, 3))

        self.particles = pv.PolyData(self.pos)
        self.particles["speed"] = np.linalg.norm(self.vel, axis=1)

        if hasattr(self, "actor"):
            self.plotter.remove_actor(self.actor)

        self.actor = self.plotter.add_mesh(
            self.particles,
            scalars="speed",
            cmap="coolwarm",
            render_points_as_spheres=True,
            point_size=10,
        )

    # ================= UI =================

    def slider(self, text, minv, maxv, val):
        lbl = QLabel(text)
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(minv, maxv)
        s.setValue(val)
        return lbl, s

    def build_ui(self, layout: QVBoxLayout):
        # ---- GAS ----
        layout.addWidget(QLabel("TRẠNG THÁI KHÍ"))

        _, self.s_v = self.slider("V", 6, 30, 10)
        _, self.s_t = self.slider("T", 10, 300, 100)
        _, self.s_n = self.slider("N", 50, 400, self.n)

        layout.addWidget(QLabel("THỂ TÍCH (V)"))
        layout.addWidget(self.s_v)
        layout.addWidget(QLabel("NHIỆT ĐỘ (T)"))
        layout.addWidget(self.s_t)
        layout.addWidget(QLabel("SỐ PHÂN TỬ (N)"))
        layout.addWidget(self.s_n)

        self.lbl_p = QLabel("ÁP SUẤT (P): 0.0")
        layout.addWidget(self.lbl_p)

        # ---- PARTICLE ----
        layout.addWidget(QLabel("PHÂN TỬ"))

        _, self.s_m = self.slider("m", 1, 500, 100)
        _, self.s_r = self.slider("r", 1, 100, 40)
        _, self.s_e = self.slider("e", 50, 100, 100)

        layout.addWidget(QLabel("KHỐI LƯỢNG (m)"))
        layout.addWidget(self.s_m)
        layout.addWidget(QLabel("BÁN KÍNH (r)"))
        layout.addWidget(self.s_r)
        layout.addWidget(QLabel("ĐÀN HỒI (e)"))
        layout.addWidget(self.s_e)

        # ---- SIM ----
        layout.addWidget(QLabel("MÔ PHỎNG"))

        _, self.s_dt = self.slider("dt", 1, 100, 20)
        layout.addWidget(QLabel("BƯỚC THỜI GIAN (dt)"))
        layout.addWidget(self.s_dt)

    # ================= PHYSICS =================

    def apply_temperature(self):
        T = self.s_t.value()
        target = np.sqrt(T / 100)
        rms = np.sqrt(np.mean(np.sum(self.vel**2, axis=1)))
        self.vel *= target / (rms + 1e-6)

    def wall_collisions(self):
        for i in range(3):
            hit = np.abs(self.pos[:, i]) > self.v_scale
            self.vel[hit, i] *= -self.e
            self.pos[hit, i] = np.sign(self.pos[hit, i]) * self.v_scale

    def particle_collisions(self):
        for i in range(self.n):
            for j in range(i + 1, self.n):
                r = self.pos[i] - self.pos[j]
                dist = np.linalg.norm(r)
                if dist < 2 * self.radius:
                    n = r / (dist + 1e-8)
                    dv = self.vel[i] - self.vel[j]
                    vn = np.dot(dv, n)
                    if vn < 0:
                        J = -(1 + self.e) * vn / 2
                        self.vel[i] += J * n
                        self.vel[j] -= J * n

    def compute_pressure(self):
        V = (2 * self.v_scale) ** 3
        return np.sum(self.mass * np.sum(self.vel**2, axis=1)) / (3 * V)

    # ================= UPDATE =================

    def update(self):
        # Volume
        self.v_scale = self.s_v.value() / 10
        box = pv.Box(bounds=(
            -self.v_scale, self.v_scale,
            -self.v_scale, self.v_scale,
            -self.v_scale, self.v_scale
        ))
        self.box_actor.mapper.dataset.deep_copy(box)

        # Params
        self.mass = self.s_m.value() / 100
        self.radius = self.s_r.value() / 1000
        self.e = self.s_e.value() / 100
        self.dt = self.s_dt.value() / 1000

        # N change
        if self.s_n.value() != self.n:
            self.n = self.s_n.value()
            self.init_particles()

        # Physics
        self.apply_temperature()
        self.pos += self.vel * self.dt
        self.wall_collisions()
        self.particle_collisions()

        # Update mesh
        self.particles.points = self.pos
        self.particles["speed"] = np.linalg.norm(self.vel, axis=1)

        # Pressure
        P = self.compute_pressure()
        self.lbl_p.setText(f"ÁP SUẤT (P): {P:.3f}")
