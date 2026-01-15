import json
import math
import itertools

# ================== HELPER ==================
def create_atom(element, pos):
    return {"element": element, "position": pos}

def create_bond(from_idx, to_idx, bond_type="single"):
    return {"from": from_idx, "to": to_idx, "type": bond_type}

def make_molecule(name, atoms, bonds):
    return {"name": name, "atoms": atoms, "bonds": bonds}

# ================== COORDINATES ==================
def place_atoms_linear(elements):
    coords = [[0,0,0]]
    for i in range(1,len(elements)):
        coords.append([coords[-1][0]+1.0,0,0])  # đơn giản 1D
    return coords

def place_atoms_water():
    return [[0,0,0],[0.96,0.26,0],[0.96,-0.26,0]]

def place_atoms_methane():
    return [[0,0,0],[0.63,0.63,0.63],[-0.63,-0.63,0.63],[-0.63,0.63,-0.63],[0.63,-0.63,-0.63]]

def place_atoms_ammonia():
    return [[0,0,0],[0,0.94,0],[0.81,-0.47,0],[-0.81,-0.47,0]]

# ================== CREATE MOLECULE ==================
def create_standard_molecule(name):
    if name=="H2": elements = ["H","H"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1)]
    elif name=="O2": elements=["O","O"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1,"double")]
    elif name=="H2O": elements=["O","H","H"]; coords=place_atoms_water(); bonds=[create_bond(0,1),create_bond(0,2)]
    elif name=="CO2": elements=["C","O","O"]; coords=[[0,0,0],[1.16,0,0],[-1.16,0,0]]; bonds=[create_bond(0,1,"double"),create_bond(0,2,"double")]
    elif name=="CH4": elements=["C","H","H","H","H"]; coords=place_atoms_methane(); bonds=[create_bond(0,i) for i in range(1,5)]
    elif name=="NH3": elements=["N","H","H","H"]; coords=place_atoms_ammonia(); bonds=[create_bond(0,i) for i in range(1,4)]
    elif name=="HCl": elements=["H","Cl"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1)]
    elif name=="NaCl": elements=["Na","Cl"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1)]
    elif name=="LiCl": elements=["Li","Cl"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1)]
    elif name=="KCl": elements=["K","Cl"]; coords=place_atoms_linear(elements); bonds=[create_bond(0,1)]
    elif name=="NH4Cl": elements=["N","H","H","H","H","Cl"]; coords=[[0,0,0],[0.9,0,0],[-0.9,0,0],[0,0.9,0],[0,-0.9,0],[2.3,0,0]]; bonds=[create_bond(0,i) for i in range(1,5)]+[create_bond(0,5)]
    else: elements=[c for c in name if c.isalpha()]; coords=place_atoms_linear(elements); bonds=[create_bond(i,i+1) for i in range(len(elements)-1)]
    atoms=[create_atom(el,pos) for el,pos in zip(elements,coords)]
    return make_molecule(name,atoms,bonds)

# ================== CREATE MOLECULE DICTIONARY ==================
MOLECULES={}
for name in ["H2","O2","H2O","CO2","CH4","NH3","HCl","NaCl","LiCl","KCl","NH4Cl","C2H6","C3H8","C4H10"]:
    MOLECULES[name]=create_standard_molecule(name)

# Thêm nguyên tử đơn nếu chưa có
for element in ["Li","Na","K","Cl2"]:
    if element not in MOLECULES:
        if element=="Cl2": MOLECULES[element]=create_standard_molecule("Cl2")
        else: MOLECULES[element]=make_molecule(element,[create_atom(element,[0,0,0])],[])

# ================== GENERATE UNIQUE REACTIONS ==================
reactions=[]
reaction_hash=set()

# Combustion
alkanes=["CH4","C2H6","C3H8","C4H10"]
for alkane in alkanes:
    reactants=[MOLECULES[alkane], MOLECULES["O2"]]
    products=[MOLECULES["CO2"], MOLECULES["H2O"]]
    key=(alkane,"O2","CO2","H2O")
    if key not in reaction_hash:
        reactions.append({"reactants":reactants,"products":products,"equation":f"{alkane}+O2->CO2+H2O","type":"Combustion"})
        reaction_hash.add(key)

# Ionic Synthesis
metals=["Li","Na","K"]; halogens=["Cl2"]
for m,h in itertools.product(metals,halogens):
    prod_name=m+"Cl"
    reactants=[MOLECULES[m],MOLECULES[h]]
    products=[MOLECULES[prod_name]]
    key=(m,h,prod_name)
    if key not in reaction_hash:
        reactions.append({"reactants":reactants,"products":products,"equation":f"{m}+{h}->{prod_name}","type":"Ionic Synthesis"})
        reaction_hash.add(key)

# Acid-Base
reactants=[MOLECULES["NH3"],MOLECULES["HCl"]]
products=[MOLECULES["NH4Cl"]]
key=("NH3","HCl","NH4Cl")
if key not in reaction_hash:
    reactions.append({"reactants":reactants,"products":products,"equation":"NH3+HCl->NH4Cl","type":"Acid-Base"})
    reaction_hash.add(key)

# Halogenation fill-up 100
for i in range(100-len(reactions)):
    reactants=[MOLECULES["H2"],MOLECULES["Cl2"]]
    products=[MOLECULES["HCl"]]
    key=("H2","Cl2","HCl")
    if key not in reaction_hash:
        reactions.append({"reactants":reactants,"products":products,"equation":f"H2+Cl2->2HCl({len(reactions)})","type":"Halogenation"})
        reaction_hash.add(key)

# ================== SAVE JSON ==================
with open("reactions_3d.json","w",encoding="utf-8") as f:
    json.dump(reactions,f,indent=4,ensure_ascii=False)

print(f"✅ Đã tạo xong {len(reactions)} phản ứng 3D hợp lý vào file reactions_3d.json")
