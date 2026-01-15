import pyvista as pv
import numpy as np
from pyvistaqt import BackgroundPlotter
from PyQt6.QtWidgets import QLabel, QSlider
from PyQt6.QtCore import Qt, QTimer


class MagneticSim:
    def __init__(self, display_layout, param_layout):
        # ===== PLOTTER =====
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.set_background("#05070d")
        display_layout.addWidget(self.plotter.interactor)

        # ===== PARAMETERS =====
        self.B = 10
        self.grid_n = 25
        self.stream_count = 120
        self.tube_radius = 0.025
        self.opacity = 0.75
        self.magnet_len = 0.9
        self.gap = 0.05

        # ===== DEBOUNCE TIMER =====
        self.update_timer = QTimer()
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self.update_field)

        # ===== UI =====
        self.make_slider(param_layout, "CƯỜNG ĐỘ NAM CHÂM", 1, 30, self.B, self.set_B)
        self.make_slider(param_layout, "MẬT ĐỘ LƯỚI", 10, 40, self.grid_n, self.set_grid)
        self.make_slider(param_layout, "SỐ ĐƯỜNG SỨC", 30, 300, self.stream_count, self.set_stream)
        self.make_slider(param_layout, "ĐỘ DÀY ĐƯỜNG", 1, 50, int(self.tube_radius * 1000), self.set_radius)
        self.make_slider(param_layout, "ĐỘ TRONG", 10, 100, int(self.opacity * 100), self.set_opacity)
        self.make_slider(param_layout, "CHIỀU DÀI NAM CHÂM", 5, 20, int(self.magnet_len * 10), self.set_length)
        self.make_slider(param_layout, "KHE HỞ N–S", 1, 20, int(self.gap * 100), self.set_gap)

        # ===== INIT =====
        self.stream_actor = None
        self.draw_magnet()
        self.update_field()

    # ================= UI =================

    def make_slider(self, layout, text, a, b, val, func):
        layout.addWidget(QLabel(text))
        s = QSlider(Qt.Orientation.Horizontal)
        s.setRange(a, b)
        s.setValue(val)
        s.valueChanged.connect(func)
        layout.addWidget(s)

    def request_update(self):
        # debounce 200ms
        self.update_timer.start(200)

    # ================= MAGNET =================

    def draw_magnet(self):
        self.plotter.clear_actors()

        L = self.magnet_len
        g = self.gap

        self.magnet_n = pv.Box(bounds=(-0.3, 0.3, g, g + L, -0.3, 0.3))
        self.magnet_s = pv.Box(bounds=(-0.3, 0.3, -g - L, -g, -0.3, 0.3))

        self.plotter.add_mesh(self.magnet_n, color="#ff3b3b", metallic=0.7)
        self.plotter.add_mesh(self.magnet_s, color="#3b6cff", metallic=0.7)

    # ================= PHYSICS =================

    def dipole_field(self, r, m):
        r_mag = np.linalg.norm(r, axis=1)[:, None] + 1e-4
        r_hat = r / r_mag
        dot = np.sum(m * r_hat, axis=1)[:, None]
        return (3 * dot * r_hat - m) / (r_mag ** 3)

    # ================= UPDATE (NẶNG) =================

    def update_field(self):
        self.draw_magnet()

        self.grid = pv.ImageData(
            dimensions=(self.grid_n,) * 3,
            spacing=(0.35, 0.35, 0.35),
            origin=(-5, -5, -5)
        )

        pts = self.grid.points
        m = np.array([0, self.B, 0])

        self.grid["B"] = self.dipole_field(pts, m)

        if self.stream_actor:
            self.plotter.remove_actor(self.stream_actor)

        stream = self.grid.streamlines(
            vectors="B",
            n_points=self.stream_count,
            max_steps=300,
            terminal_speed=5e-2,
            initial_step_length=0.3
        )

        self.stream_actor = self.plotter.add_mesh(
            stream.tube(radius=self.tube_radius),
            color="#00f7ff",
            opacity=self.opacity,
            smooth_shading=True
        )

    # ================= SETTERS =================
    # ---- NẶNG → debounce ----

    def set_B(self, v):
        self.B = v
        self.request_update()

    def set_grid(self, v):
        self.grid_n = v
        self.request_update()

    def set_stream(self, v):
        self.stream_count = v
        self.request_update()

    def set_length(self, v):
        self.magnet_len = v / 10
        self.request_update()

    def set_gap(self, v):
        self.gap = v / 100
        self.request_update()

    # ---- NHẸ → realtime ----

    def set_radius(self, v):
        self.tube_radius = v / 1000
        if self.stream_actor:
            self.stream_actor.mapper.SetScalarRange(0, 1)
            self.stream_actor.GetMapper().GetInput().GetPointData()
            self.stream_actor = self.plotter.add_mesh(
                self.stream_actor.mapper.GetInput().tube(radius=self.tube_radius),
                color="#00f7ff",
                opacity=self.opacity,
                smooth_shading=True
            )

    def set_opacity(self, v):
        self.opacity = v / 100
        if self.stream_actor:
            self.stream_actor.GetProperty().SetOpacity(self.opacity)
