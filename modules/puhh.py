import json
import numpy as np
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt, QTimer
from pyvistaqt import BackgroundPlotter
import pyvista as pv

# ================== LOAD DATA ==================
def load_reactions_from_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

REACTIONS_DATA = load_reactions_from_json("data/reactions_detailed.json")

# ================== ATOM COLORS ==================
ATOM_COLORS = {
    "H": "#ffffff",
    "C": "#000000",
    "O": "#ff0000",
    "N": "#0000ff",
    "Cl": "#00ff00",
    "Li": "#facc15",
    "Na": "#f0f8ff"
}

BOND_COLORS = {
    "single": "#aaaaaa",
    "double": "#888888",
    "triple": "#555555"
}

# ================== Reaction Module ==================
class ReactionModule:
    def __init__(self, display_layout, param_layout):
        self.display_layout = display_layout
        self.param_layout = param_layout
        self.current_reaction = None
        self.actors = []

        # UI
        self.build_search_box()
        self.build_reaction_list()
        self.build_info()
        self.build_3d()

    # ================== SEARCH BOX ==================
    def build_search_box(self):
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Tìm kiếm phản ứng...")
        self.search_box.textChanged.connect(self.filter_reactions)
        self.param_layout.addWidget(QLabel("Tìm kiếm:"))
        self.param_layout.addWidget(self.search_box)

    def filter_reactions(self, text):
        text = text.lower()
        self.list_widget.clear()
        for reaction in REACTIONS_DATA:
            if text in reaction["equation"].lower():
                self.list_widget.addItem(reaction["equation"])

    # ================== REACTION LIST ==================
    def build_reaction_list(self):
        self.list_widget = QListWidget()
        for reaction in REACTIONS_DATA:
            self.list_widget.addItem(reaction["equation"])
        self.list_widget.itemClicked.connect(self.load_reaction)
        self.param_layout.addWidget(QLabel("Chọn phản ứng:"))
        self.param_layout.addWidget(self.list_widget)

    # ================== INFO BOX ==================
    def build_info(self):
        self.info = QTextEdit()
        self.info.setReadOnly(True)
        self.info.setMinimumHeight(150)
        self.param_layout.addWidget(QLabel("Thông tin phản ứng:"))
        self.param_layout.addWidget(self.info)

    # ================== 3D ==================
    def build_3d(self):
        self.plotter = BackgroundPlotter(show=False)
        self.plotter.set_background("#020617")
        self.plotter.enable_eye_dome_lighting()
        self.plotter.camera.position = (8, -8, 6)
        self.plotter.camera.focal_point = (0,0,0)
        self.plotter.camera.up = (0,0,1)
        self.display_layout.addWidget(self.plotter.interactor)

        # Animation timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    # ================== LOAD REACTION ==================
    def load_reaction(self, item):
        eq = item.text()
        reaction = next((r for r in REACTIONS_DATA if r["equation"] == eq), None)
        if not reaction:
            return
        self.current_reaction = reaction

        self.info.setText(
            f"Phản ứng: {reaction['equation']}\n"
            f"Loại: {reaction['type']}\n"
            f"Chất tham gia: {', '.join([m.get('name','Mol') for m in reaction['reactants']])}\n"
            f"Sản phẩm: {', '.join([m.get('name','Mol') for m in reaction['products']])}"
        )

        self.draw_reaction(reaction)

    # ================== DRAW REACTION ==================
    def draw_reaction(self, reaction):
        self.plotter.clear()
        self.actors.clear()

        for phase in ["reactants", "products"]:
            x_offset = -3 if phase=="reactants" else 3
            for mol in reaction[phase]:
                self.draw_molecule(mol, x_offset)

    # ================== DRAW MOLECULE ==================
    def draw_molecule(self, molecule, x_offset=0):
        for i, atom in enumerate(molecule["atoms"]):
            pos = np.array(atom["position"]) + np.array([x_offset,0,0])
            sphere = pv.Sphere(center=pos, radius=0.25)
            actor = self.plotter.add_mesh(sphere, color=ATOM_COLORS.get(atom["element"], "#ffffff"), smooth_shading=True)
            self.actors.append({"actor":actor, "target":pos})

        for bond in molecule.get("bonds", []):
            idx1, idx2 = bond["from"], bond["to"]
            pos1 = np.array(molecule["atoms"][idx1]["position"]) + np.array([x_offset,0,0])
            pos2 = np.array(molecule["atoms"][idx2]["position"]) + np.array([x_offset,0,0])
            vec = pos2 - pos1
            center = (pos1 + pos2)/2
            cyl = pv.Cylinder(center=center, direction=vec, radius=0.07, height=np.linalg.norm(vec))
            actor = self.plotter.add_mesh(cyl, color=BOND_COLORS.get(bond["type"], "#aaaaaa"), smooth_shading=True)
            self.actors.append({"actor":actor, "target":center})

    # ================== ANIMATION ==================
    def animate(self):
        # PyVista Qt animation workaround: tạm thời không di chuyển, giữ vị trí cố định
        # Nếu muốn di chuyển, cần dùng `set_position` từ add_mesh với tên
        pass
