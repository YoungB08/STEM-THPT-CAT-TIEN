from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from pyvistaqt import BackgroundPlotter
import pyvista as pv
import numpy as np

from data.elements import ELEMENTS_DATA

# ===================== MODULE =====================
class PeriodicModule:
    def __init__(self, display_layout, param_layout):
        self.display_layout = display_layout
        self.param_layout = param_layout

        self.build_table()
        self.build_info()
        self.build_3d()

    # ================== TABLE ==================
    def build_table(self):
        table = QWidget()
        grid = QGridLayout(table)
        grid.setSpacing(4)

        for period, group, sym, *_ in ELEMENTS_DATA:
            btn = QPushButton(sym)
            btn.setFixedSize(48,48)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, s=sym: self.load_element(s))
            grid.addWidget(btn, period-1, group-1)

        self.display_layout.addWidget(table)

    # ================== INFO ==================
    def build_info(self):
        self.info = QTextEdit()
        self.info.setReadOnly(True)
        self.info.setMinimumHeight(220)
        self.param_layout.addWidget(self.info)

    # ================== 3D ==================
    def build_3d(self):
        self.plotter = BackgroundPlotter(show=False)
        self.display_layout.addWidget(self.plotter.interactor, 1)

    # ================== LOAD ELEMENT ==================
    def load_element(self, symbol):
        element = None
        for e in ELEMENTS_DATA:
            if e[2] == symbol:
                element = e
                break
        if element is None:
            return

        _, _, sym, name, Z, shells, tcvl, tchh, orbital = element

        self.info.setText(
            f"Nguyên tố: {name} ({sym})\n"
            f"Số hiệu nguyên tử (Z): {Z}\n\n"
            f"TCVL:\n{tcvl}\n\n"
            f"TCHH:\n{tchh}\n\n"
            f"Loại orbital: {orbital}"
        )

        # vẽ mô hình orbital
        self.draw_orbital_model({"orbital": orbital, "shells": shells})

    # ================== ATOM MODEL ==================
    def draw_orbital_model(self, element):
        self.plotter.clear()
        self.electrons = []
        self.time = 0.0

        # CAMERA & LIGHT
        self.plotter.set_background("#020617")
        self.plotter.enable_eye_dome_lighting()
        self.plotter.camera.position = (0, -8, 4)
        self.plotter.camera.focal_point = (0, 0, 0)
        self.plotter.camera.up = (0,0,1)

        orbital_type = element["orbital"]
        shells = element.get("shells", [1])

        # NUCLEUS
        nucleus = pv.Sphere(radius=0.45, theta_resolution=64, phi_resolution=64)
        self.plotter.add_mesh(nucleus, color="#ef4444",
                              smooth_shading=True, specular=0.6, specular_power=30)

        # SHELLS + ELECTRONS
        base_r = 1.4
        for shell_idx, e_count in enumerate(shells):
            r = base_r + shell_idx * 1.1
            # Orbit
            orbit = pv.Circle(radius=r, resolution=240)
            self.plotter.add_mesh(orbit, color="#64748b", line_width=3, opacity=0.35)

            for i in range(e_count):
                phase = 2*np.pi*i/e_count
                electron = pv.Sphere(radius=0.12, theta_resolution=32, phi_resolution=32)
                actor = self.plotter.add_mesh(electron, color="#38bdf8", smooth_shading=True,
                                              specular=1.0, specular_power=50)
                self.electrons.append({"actor": actor, "r": r, "phase": phase, "speed": 0.8 + 0.2*shell_idx})

        # VẼ ORBITAL THỰC
        if orbital_type == "s":
            self.draw_s_orbital()
        elif orbital_type == "p":
            self.draw_s_orbital(0.8)
            self.draw_p_orbital("x")
            self.draw_p_orbital("y")
            self.draw_p_orbital("z")
        elif orbital_type == "d":
            self.draw_s_orbital(0.7)
            self.draw_p_orbital("x")
            self.draw_d_orbital()

        # ANIMATION
        self.plotter.add_callback(self.animate_electrons, interval=16)

    def animate_electrons(self):
        self.time += 0.02
        for e in self.electrons:
            angle = e["phase"] + self.time*e["speed"]
            x = e["r"]*np.cos(angle)
            y = e["r"]*np.sin(angle)
            z = 0.15*np.sin(angle*2)
            e["actor"].SetPosition(x,y,z)

    # ================== ORBITAL SHAPES ==================
    def draw_s_orbital(self, radius=1.2):
        cloud = pv.Sphere(radius=radius, theta_resolution=64, phi_resolution=64)
        self.plotter.add_mesh(cloud, color="#38bdf8", opacity=0.25, smooth_shading=True)

    def draw_p_orbital(self, axis="x"):
        offset = 0.9
        r = 0.6
        centers = {
            "x": [( offset, 0,0), (-offset,0,0)],
            "y": [(0, offset,0), (0,-offset,0)],
            "z": [(0,0, offset), (0,0,-offset)],
        }
        for c in centers[axis]:
            lobe = pv.Sphere(center=c, radius=r, theta_resolution=48, phi_resolution=48)
            self.plotter.add_mesh(lobe, color="#22c55e", opacity=0.35, smooth_shading=True)

    def draw_d_orbital(self):
        r = 0.45
        offset = 0.9
        positions = [
            ( offset,  offset,0),
            (-offset,  offset,0),
            (-offset, -offset,0),
            ( offset, -offset,0)
        ]
        for p in positions:
            lobe = pv.Sphere(center=p, radius=r, theta_resolution=48, phi_resolution=48)
            self.plotter.add_mesh(lobe, color="#a855f7", opacity=0.35, smooth_shading=True)
