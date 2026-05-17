
PAGE_PADX  = 40       
PAGE_PADY  = 20      
CARD_PADX  = 20      
CARD_PADY  = 20       
TITLE_PADY = (0, 20)  

COLORS = {
    "bg":        "#f5f5f7",
    "card":      "#ffffff",
    "text_main": "#1d1d1f",
    "text_sub":  "#86868b",
    "border":    "#d2d2d7",
    "accent":    "#0071e3",
    "accent_2":  "#005bb5",
    "danger":    "#ff3b30",
    "success":   "#1db954",
}

BG_PAGE   = COLORS["bg"]
BG_CARD   = COLORS["card"]
TEXT_MAIN = COLORS["text_main"]
TEXT_SUB  = COLORS["text_sub"]
BORDER    = COLORS["border"]
ACCENT     = COLORS["accent"]
DANGER     = COLORS["danger"]
SUCCESS    = COLORS["success"]


PAGE_TITLE_FONT = ("SF Pro Display", 18, "bold")
PAGE_TITLE_FG   = TEXT_MAIN

SECTION_TITLE_FONT = ("SF Pro Display", 16, "bold")
SECTION_TITLE_FG   = TEXT_MAIN

BODY_FONT    = ("SF Pro Text", 11)
BODY_FG      = TEXT_MAIN

LABEL_FONT   = ("SF Pro Text", 7, "bold") 
LABEL_FG     = TEXT_SUB

SUBTEXT_FONT = ("SF Pro Text", 9)
SUBTEXT_FG   = TEXT_SUB

PRIMARY_FONT = ("SF Pro Text", 11, "bold")



PRIMARY_BUTTON_STYLE = {
    "bg": ACCENT,
    "fg": "white",
    "relief": "flat",
    "cursor": "hand2",
    "borderwidth": 0,
    "font": PRIMARY_FONT,
}

DANGER_BUTTON_STYLE = {
    "bg": DANGER,
    "fg": "white",
    "relief": "flat",
    "cursor": "hand2",
    "borderwidth": 0,
    "font": PRIMARY_FONT,
}

LIGHT_BUTTON_STYLE = {
    "bg": BG_PAGE,
    "fg": TEXT_MAIN,
    "relief": "flat",
    "cursor": "hand2",
    "borderwidth": 0,
    "font": ("Helvetica", 10),
}

LINK_BUTTON_STYLE = {
    "bg": "transparent",
    "fg": ACCENT,
    "relief": "flat",
    "cursor": "hand2",
    "borderwidth": 0,
    "font": ("SF Pro Text", 11, "bold"),
}

ENTRY_STYLE = {
    "font": ("SF Pro Text", 11),
    "bg": BG_PAGE,
    "relief": "flat",
    "highlightthickness": 1,
    "highlightbackground": BORDER,
    "highlightcolor": ACCENT,
}


PAGE_TITLE_BG = BG_PAGE
TITLE_BG = BG_PAGE
CARD_BG = BG_CARD

