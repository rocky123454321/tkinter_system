import tkinter as tk
from tkinter import ttk
from pathlib import Path

from PIL import Image, ImageTk
from  controllers.room_controller import RoomController


def create_user_map(parent, on_back=None):
    """Temporary floor map UI.

    - Shows a floor image (1st/2nd/3rd)
    - Buttons can be extended later to fully utilize room inventory data
    """

    container = tk.Frame(parent, bg="#f5f5f7")
    container.pack(fill="both", expand=True)

    header = tk.Frame(container, bg="#f5f5f7")
    header.pack(fill="x", padx=10, pady=(0, 10))

    tk.Label(
        header,
        text="Hotel Map",
        font=("SF Pro Display", 22, "bold"),
        bg="#f5f5f7",
        fg="#1d1d1f",
    ).pack(side="left")



    rooms = RoomController.handle_list_rooms()
    floors = sorted({int(r.get("floor")) for r in rooms if r.get("floor") is not None})

    floor_order = [1, 2, 3]


    project_root = Path(__file__).resolve().parents[3]
    assets_dir = project_root / "assets"

    img_paths = {
        1: assets_dir / "floor1_image.png",
        2: assets_dir / "floor2_image.png",
        3: assets_dir / "floor3_image.png",
        4: assets_dir / "floor4_image.png",
    }



    controls = tk.Frame(container, bg="#f5f5f7")
    controls.pack(fill="x", padx=20, pady=(0, 10))

    tk.Label(controls, text="Select Floor:", font=("Segoe UI", 10, "bold"), bg="#f5f5f7", fg="#1d1d1f").pack(
        side="left"
    )

    selected_floor = {"v": 1}

    status_lbl = tk.Label(controls, text="", font=("Segoe UI", 9), bg="#f5f5f7", fg="#86868b")
    status_lbl.pack(side="right")


    img_holder = tk.Frame(container, bg="#ffffff", highlightthickness=1, highlightbackground="#d2d2d7")
    img_holder.pack(fill="both", expand=True, padx=20, pady=10)

    img_label = tk.Label(img_holder, bg="#ffffff")
    img_label.pack(fill="both", expand=True)


    photo_cache = {1: None, 2: None, 3: None}

    def set_floor(floor_no: int):
        selected_floor["v"] = floor_no


        floor_rooms = [r for r in rooms if int(r.get("floor")) == floor_no]
        avail_count = sum(1 for r in floor_rooms if r.get("status") == "Available")
        occ_count = sum(1 for r in floor_rooms if r.get("status") == "Occupied")
        maint_count = sum(1 for r in floor_rooms if r.get("status") == "Maintenance")

        status_lbl.config(
            text=f"Floor {floor_no} | Available: {avail_count} • Occupied: {occ_count} • Maintenance: {maint_count}"
        )

        img_path = img_paths.get(floor_no)
        if not img_path or not img_path.exists():
            img_label.config(text=f"Missing image: {img_path}", image="")
            return


        raw = Image.open(str(img_path))

        def redraw(*_):
            w = max(img_label.winfo_width(), 3800)
            h = max(img_label.winfo_height(), 3600)

            resized = raw.copy()
            resized.thumbnail((w, h))
            photo = ImageTk.PhotoImage(resized)
            photo_cache[floor_no] = photo
            img_label.config(image=photo)

        redraw()

    def make_btn(floor_no: int, label: str):
        btn = tk.Button(
            controls,
            text=label,
            bg="#ffffff",
            fg="#1d1d1f",
            relief="flat",
            cursor="hand2",
            highlightthickness=1,
            highlightbackground="#e1e1e1",
            padx=15,
            pady=8,
            command=lambda: set_floor(floor_no),
        )
        btn.pack(side="left", padx=8)


    make_btn(1, "1st Floor")
    make_btn(2, "2nd Floor")
    make_btn(3, "3rd Floor")
    make_btn(4, "4th Floor")



    set_floor(1)

    return container

