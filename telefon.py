import tkinter as tk
import math

# PARAMEETRID

tolerance = 0.95

cx, cy = 310, 310  # keskpunkt
outer_r = 190  # ketta välimine raadius

angle = 0.0  # ketta pöördenurk
dragging = False
returning = False

last_mouse_angle = None
max_angle = 0

selected = None  # hetkel valitud number
number_text = ""  # valitud numbrid

stopper_angle = 45  # stopperi nurk

digit_angles = {
    "1": 330, "2": 300, "3": 270, "4": 240, "5": 210,
    "6": 180, "7": 150, "8": 120, "9": 90, "0": 60
}


# "ABIFUNKTSIOONID"
def mouse_angle(x, y):
    # Hiire nurk keskpunkti suhtes päripäeva

    return (math.degrees(math.atan2(y - cy, x - cx)) + 450) % 360


def angle_change(current, previous):
    # Kahe nurga vahe päripäeva

    diff = current - previous
    if diff > 180:
        diff -= 360
    elif diff < -180:
        diff += 360
    return diff


# TELEFONI VISUAAL

def draw_phone():
    canvas.delete("all")

    # Peamine ketas
    canvas.create_oval(
        cx - outer_r, cy - outer_r,
        cx + outer_r, cy + outer_r,
        fill="#c98a22",
        outline="#5a3d09",
        width=6
    )

    # Stopper
    r = math.radians(stopper_angle)
    canvas.create_line(
        cx + 165 * math.cos(r), cy + 165 * math.sin(r),
        cx + 205 * math.cos(r), cy + 205 * math.sin(r),
        width=10, fill="#111", capstyle=tk.ROUND
    )

    # Sõrmeaugud
    hole_r = 155
    for base in digit_angles.values():
        a = math.radians(base + angle)
        x = cx + hole_r * math.cos(a)
        y = cy + hole_r * math.sin(a)

        canvas.create_oval(
            x - 16, y - 16,
            x + 16, y + 16,
            fill="#f7e6b5",
            outline="#6d4a10",
            width=2
        )

    # Numbrid
    num_r = 155
    visible = 4  # määrab, kui suure nurga ulatuses on number augu all nähtav.

    if not dragging and angle == 0:
        for d, base in digit_angles.items():
            a = math.radians(base)
            canvas.create_text(
                cx + num_r * math.cos(a),
                cy + num_r * math.sin(a),
                text=d, font=("Arial", 12, "bold"), fill="black"
            )

    elif dragging:
        for d, num_base in digit_angles.items():
            for hole_base in digit_angles.values():
                hole_angle = (hole_base + angle) % 360
                diff = (hole_angle - num_base + 180) % 360 - 180

                if -visible <= diff <= visible:
                    a = math.radians(num_base)
                    canvas.create_text(
                        cx + num_r * math.cos(a),
                        cy + num_r * math.sin(a),
                        text=d, font=("Arial", 12, "bold"), fill="black"
                    )
                    break


# HIIR

def mouse_press(event):
    # Käivitatakse siis, kui kasutaja vajutab hiirenuppu ketta peale

    global dragging, selected, angle, max_angle, last_mouse_angle, returning

    dx = event.x - cx
    dy = event.y - cy

    # Ainult õiges ringis tohib keerata
    if not (135 <= math.hypot(dx, dy) <= 175):
        return

    click_angle = (math.degrees(math.atan2(dy, dx)) + 360) % 360

    best = None
    best_diff = 999

    for d, ang in digit_angles.items():
        hole = (ang + angle) % 360
        diff = abs((click_angle - hole + 180) % 360 - 180)
        if diff < best_diff and diff < 18:
            best = d
            best_diff = diff

    if best is None:
        return

    selected = best
    dragging = True
    angle = 0

    # Arvutab pikkust stopperini
    start = digit_angles[best]
    max_angle = (stopper_angle - start) % 360 or 360

    last_mouse_angle = mouse_angle(event.x, event.y)
    returning = False


def mouse_drag(event):
    # Käivitatakse siis, kui kasutaja hoiab hiirt all ja liigutab

    global angle, last_mouse_angle

    if not dragging:
        return

    current = mouse_angle(event.x, event.y)
    diff = angle_change(current, last_mouse_angle)

    # Vastupidi keerata ei saa
    if diff > 0:
        angle = min(max_angle, angle + diff)
        draw_phone()

    last_mouse_angle = current


def mouse_release(event):
    global dragging, selected, number_text

    # Kontroll, kas keerati
    if not dragging:
        return

    # Lõpetab keeramise
    dragging = False

    # Kontroll, et kas keerati lõpuni välja
    if selected and angle >= max_angle * tolerance:
        number_text += selected
        label.config(text=f"Valitud number: {number_text}")

    selected = None
    start_return()


# TAGASIPÖÖRDUMINE

def start_return():
    global returning
    returning = True
    animate_return()


def animate_return():
    global angle, returning

    if not returning:
        return

    # Iga "kaader" jätab alles 80% eelmisest nurgast
    angle *= 0.8
    if angle < 0.5:
        angle = 0
        returning = False
        draw_phone()
        return

    draw_phone()
    root.after(16, animate_return)


# NUPUD

def call():
    label.config(text=f"Helistan: {number_text}" if number_text else "Valitud number:")


def delete_last():
    global number_text
    number_text = number_text[:-1]
    label.config(text=f"Valitud number: {number_text}")


# VORMISTUS AKNAS

root = tk.Tk()
root.title("Telo")
root.geometry("720x720")
root.resizable(False, False)
root.configure(bg="#f2f2f2")

canvas = tk.Canvas(root, width=620, height=620, bg="#f2f2f2", highlightthickness=0)
canvas.pack()

label = tk.Label(root, text="Valitud number:", font=("Arial", 18), bg="#f2f2f2", fg="black")
label.pack(pady=(0, 8))

tk.Button(root, text="Helista", font=("Arial", 16, "bold"), command=call).pack()
tk.Button(root, text="Kustuta", font=("Arial", 12), command=delete_last).pack(pady=(6, 0))

canvas.bind("<Button-1>", mouse_press)
canvas.bind("<B1-Motion>", mouse_drag)
canvas.bind("<ButtonRelease-1>", mouse_release)

draw_phone()
root.mainloop()