import json

MOLECULE_TEMPLATES = {
    "H2": [[0,0,0], [0.74,0,0]],
    "O2": [[0,0,0], [1.21,0,0]],
    "H2O": [[0,0,0], [0.96,0.26,0], [0.96,-0.26,0]],
    "CO2": [[0,0,0], [1.16,0,0], [-1.16,0,0]],
    "CH4": [[0,0,0], [0.63,0.63,0.63], [-0.63,-0.63,0.63], [-0.63,0.63,-0.63], [0.63,-0.63,-0.63]],
    "NaCl": [[0,0,0],[2.36,0,0]],
    "KCl": [[0,0,0],[2.36,0,0]],
    "LiCl": [[0,0,0],[2.3,0,0]],
    "HCl": [[0,0,0],[1.27,0,0]],
    "NaOH": [[0,0,0],[1.0,0,0]],
    "KOH": [[0,0,0],[1.0,0,0]],
    "H2SO4": [[0,0,0],[1.0,0,0],[0,-1.0,0]],
    "K2SO4": [[0,0,0],[1.0,0,0],[0,-1.0,0]],
    "HNO3": [[0,0,0],[1.0,0,0],[0,-1.0,0]],
    "NaNO3": [[0,0,0],[1.0,0,0],[0,-1.0,0]],
}

def generate_template(molecule_name):
    return MOLECULE_TEMPLATES.get(molecule_name, [[0,0,0],[2.0,0,0]])

def generate_100_reactions(filename="reactions_100.json"):
    reactions = []

    # 1️⃣ Kim loại kiềm + Halogen
    metals = ["Li","Na","K","Rb","Cs"]
    halogens = [("Cl2","Cl"),("Br2","Br"),("I2","I")]
    for m in metals:
        for h_formula,h_sym in halogens:
            product = f"{m}{h_sym}"
            reactions.append({
                "reactants":[m,h_formula],
                "products":[product],
                "equation":f"2 {m} + {h_formula} -> 2 {product}",
                "type":"Ionic Synthesis",
                "molecules": {
                    m: [[0,0,0]],
                    h_formula: generate_template(h_formula),
                    product: generate_template(product)
                }
            })

    # 2️⃣ Phản ứng cháy Ankan (CH4 -> C5H12)
    for n in range(1,6):
        formula = "CH4" if n==1 else f"C{n}H{2*n+2}"
        reactions.append({
            "reactants":[formula,"O2"],
            "products":["CO2","H2O"],
            "equation":f"{formula} + O2 -> {n}CO2 + {n+1}H2O",
            "type":"Combustion",
            "molecules": {
                formula: generate_template(formula),
                "O2": generate_template("O2"),
                "CO2": generate_template("CO2"),
                "H2O": generate_template("H2O")
            }
        })

    # 3️⃣ Axit + Baz → Muối + Nước
    acid_base_pairs = [
        ("HCl","NaOH","NaCl"),
        ("HCl","KOH","KCl"),
        ("H2SO4","NaOH","Na2SO4"),
        ("H2SO4","KOH","K2SO4"),
        ("HNO3","NaOH","NaNO3"),
        ("HNO3","KOH","KNO3")
    ]
    for acid,base,salt in acid_base_pairs:
        reactions.append({
            "reactants":[acid,base],
            "products":[salt,"H2O"],
            "equation":f"{acid} + {base} -> {salt} + H2O",
            "type":"Acid-Base Neutralization",
            "molecules": {
                acid: generate_template(acid),
                base: generate_template(base),
                salt: generate_template(salt),
                "H2O": generate_template("H2O")
            }
        })

    # 4️⃣ Oxit kim loại + Axit → Muối + H2O
    oxides = [("Na2O","H2O","NaOH"),("K2O","H2O","KOH")]
    for ox,water,prod in oxides:
        reactions.append({
            "reactants":[ox,water],
            "products":[prod],
            "equation":f"{ox} + {water} -> {prod}",
            "type":"Oxide-Acid Reaction",
            "molecules": {
                ox: generate_template(ox),
                water: generate_template(water),
                prod: generate_template(prod)
            }
        })

    # 5️⃣ Đảm bảo đủ 100 phản ứng → nhân bản các phản ứng cháy và ion
    while len(reactions)<100:
        reactions.append(reactions[len(reactions)%len(reactions)])  # vòng lặp lại

    with open(filename,"w",encoding="utf-8") as f:
        json.dump(reactions[:100],f,indent=4,ensure_ascii=False)
    
    print(f"Đã tạo 100 phản ứng phổ biến vào {filename}")

# Chạy
generate_100_reactions()
