MAIN_STYLE = """
/* =============/* ================= ROOT ================= */
QMainWindow {
    background-color: #020617;
    font-family: 'Segoe UI', 'Inter', sans-serif;
}

/* ================= SIDEBAR ================= */
#Sidebar {
    background-color: #020617;
    border-right: 1px solid #1e293b;
}

/* ================= CONTROL PANEL ================= */
#ControlPanel {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 16px;
    margin: 12px;
    padding: 16px;
}

/* ================= SECTION CARD ================= */
QFrame#Section {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 14px;
    padding: 14px;
    margin-bottom: 14px;
}

/* ================= SECTION TITLE ================= */
QLabel#SectionTitle {
    color: #38bdf8;
    font-size: 14px;
    font-weight: 700;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* ================= PARAM LABEL ================= */
QLabel {
    color: #94a3b8;
    font-size: 12px;
    font-weight: 500;
    margin-top: 6px;
}

/* ================= VALUE LABEL ================= */
QLabel#Value {
    color: #e2e8f0;
    font-size: 13px;
    font-weight: 600;
}

/* ================= SLIDER ================= */
QSlider {
    margin-top: 4px;
    margin-bottom: 10px;
}

QSlider::groove:horizontal {
    height: 6px;
    background: #0f172a;
    border-radius: 3px;
}

QSlider::sub-page:horizontal {
    background: #38bdf8;
    border-radius: 3px;
}

QSlider::add-page:horizontal {
    background: #020617;
    border-radius: 3px;
}

QSlider::handle:horizontal {
    background: #38bdf8;
    border: 2px solid #7dd3fc;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}

/* ================= PRESSURE DISPLAY ================= */
QLabel#Pressure {
    color: #7dd3fc;
    font-size: 14px;
    font-weight: 700;
    padding: 6px 0;
}

/* ================= BUTTON ================= */
QPushButton {
    background-color: #020617;
    color: #cbd5f5;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 13px;
    font-weight: 600;
}

QPushButton:hover {
    border: 1px solid #38bdf8;
    color: #38bdf8;
}

QPushButton:pressed {
    background-color: #0f172a;
}

/* ================= ACTIVE BUTTON ================= */
QPushButton#Active {
    background-color: #020617;
    color: #38bdf8;
    border: 1px solid #38bdf8;
}
/* ================= SEARCH BOX ================= */
QLineEdit#SearchBox {
    background-color: #0f172a;
    color: #e2e8f0;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 6px 10px;
    font-size: 13px;
}

/* ================= LIST WIDGET ================= */
QListWidget#ReactionList {
    background-color: #020617;
    border: 1px solid #1e293b;
    border-radius: 12px;
    color: #cbd5f5;
    font-size: 13px;
}

/* ================= LIST ITEM HOVER ================= */
QListWidget::item:hover {
    background-color: #1e293b;
    color: #38bdf8;
}

/* ================= LIST ITEM SELECTED ================= */
QListWidget::item:selected {
    background-color: #38bdf8;
    color: #020617;
    border-radius: 8px;
}

/* ================= INFO TEXT ================= */
QTextEdit#ReactionInfo {
    background-color: #0f172a;
    color: #e2e8f0;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 8px;
    font-size: 13px;
}
/* ================= SEARCH BOX ================= */
QLineEdit#SearchBox {
    background-color: #0f172a;
    color: #f1f5f9;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 8px 12px;
    font-size: 13px;
    selection-background-color: #38bdf8;
}

QLineEdit#SearchBox:focus {
    border: 1px solid #38bdf8;
    background-color: #020617;
}

/* ================= LIST WIDGET ================= */
QListWidget#ReactionList {
    background-color: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    color: #94a3b8;
    font-size: 13px;
    outline: none;
    padding: 5px;
}

QListWidget#ReactionList::item {
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 2px;
}

QListWidget#ReactionList::item:hover {
    background-color: #1e293b;
    color: #38bdf8;
}

QListWidget#ReactionList::item:selected {
    background-color: #38bdf8;
    color: #020617;
    font-weight: bold;
}

/* ================= INFO TEXT BOX ================= */
QTextEdit#ReactionInfo {
    background-color: #0f172a;
    color: #e2e8f0;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 12px;
    font-size: 13px;
    line-height: 1.5;
}

/* ================= SCROLLBAR (Thanh cuộn cho List và Info) ================= */
QAbstractScrollArea QScrollBar:vertical {
    background: #020617;
    width: 8px;
    margin: 0px;
}

QAbstractScrollArea QScrollBar::handle:vertical {
    background: #1e293b;
    min-height: 20px;
    border-radius: 4px;
}

QAbstractScrollArea QScrollBar::handle:vertical:hover {
    background: #38bdf8;
}

QAbstractScrollArea QScrollBar::add-line:vertical, 
QAbstractScrollArea QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
