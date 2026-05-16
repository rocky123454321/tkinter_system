# Shared UI constants for consistent styling across all user-facing pages.

# ---------------------------------------------------------------------------
# Page Titles  (e.g. "Your Bookings", "Hotel Map", "Settings")
# ---------------------------------------------------------------------------
PAGE_TITLE_FONT = ("SF Pro Display", 18, "bold")
PAGE_TITLE_FG   = "#1d1d1f"
PAGE_TITLE_BG   = "#f5f5f7"

# ---------------------------------------------------------------------------
# Section Sub-headers  (e.g. "Profile", "Password" inside Settings)
# ---------------------------------------------------------------------------
SECTION_TITLE_FONT = ("SF Pro Display", 16, "bold")
SECTION_TITLE_FG   = "#1d1d1f"

# ---------------------------------------------------------------------------
# Body / Label text
# ---------------------------------------------------------------------------
BODY_FONT      = ("SF Pro Text", 11)
BODY_FG        = "#1d1d1f"

LABEL_FONT     = ("SF Pro Text", 7, "bold")   # small caps field labels
LABEL_FG       = "#86868b"

SUBTEXT_FONT   = ("SF Pro Text", 9)
SUBTEXT_FG     = "#86868b"

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
COLORS = {
    "bg":        "#f5f5f7",
    "card":      "#ffffff",
    "text_main": "#1d1d1f",
    "text_sub":  "#86868b",
    "border":    "#d2d2d7",
    "accent":    "#0071e3",
    "success":   "#1db954",
}

# ---------------------------------------------------------------------------
# Spacing  (padx / pady values used consistently across pages)
# ---------------------------------------------------------------------------
PAGE_PADX  = 40       # outer horizontal padding of content area
PAGE_PADY  = 20       # outer vertical padding of content area
CARD_PADX  = 20       # padding inside a card/panel
CARD_PADY  = 20       # padding inside a card/panel
TITLE_PADY = (0, 20)  # below every page title