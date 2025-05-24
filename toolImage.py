import os
import subprocess
from tkinter import Tk, Button, Label, filedialog, messagebox, simpledialog
from PIL import Image, UnidentifiedImageError
from rembg import remove

DEFAULT_OUTPUT_FOLDER = r"D:\app\tool\media\toolImg"

REMOVED_BG_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "removed_bg")
RESIZED_FOLDER = os.path.join(DEFAULT_OUTPUT_FOLDER, "resized")


def openFolder(path):
    if os.path.exists(path):
        subprocess.Popen(f'explorer "{path}"')
    else:
        messagebox.showwarning(
            "⚠️ Thư mục không tồn tại",
            f"Thư mục {path} chưa được tạo hoặc không tồn tại!",
        )

def removeBackgroundGui():
    filePath = filedialog.askopenfilename(
        title="Chọn ảnh để xóa nền",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")],
    )
    if not filePath:
        return

    try:
        image = Image.open(filePath)
        output = remove(image)

        baseName = os.path.splitext(os.path.basename(filePath))[0]
        os.makedirs(REMOVED_BG_FOLDER, exist_ok=True)

        outputPath = os.path.join(REMOVED_BG_FOLDER, f"{baseName}_no_bg.png")
        output.save(outputPath)

        messagebox.showinfo(
            "✅ Thành công", f"Ảnh đã xóa nền và lưu tại:\n{outputPath}"
        )
    except UnidentifiedImageError:
        messagebox.showerror("❌ Lỗi", "File không phải là ảnh hợp lệ.")
    except Exception as e:
        messagebox.showerror("❌ Lỗi", f"Không thể xử lý ảnh:\n{str(e)}")

def resizeImageGui():
    filePath = filedialog.askopenfilename(
        title="Chọn ảnh để resize",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")],
    )
    if not filePath:
        return

    try:
        image = Image.open(filePath)
        baseName = os.path.splitext(os.path.basename(filePath))[0]

        width = int(simpledialog.askstring("Chiều rộng", "Nhập chiều rộng (px):"))
        height = int(simpledialog.askstring("Chiều cao", "Nhập chiều cao (px):"))

        if width <= 0 or height <= 0:
            messagebox.showerror("❌ Lỗi", "Chiều rộng và chiều cao phải lớn hơn 0.")
            return

        resized = image.resize((width, height), resample=Image.LANCZOS)
        os.makedirs(RESIZED_FOLDER, exist_ok=True)

        resizePath = os.path.join(RESIZED_FOLDER, f"{baseName}_{width}x{height}.png")
        resized.save(resizePath)

        messagebox.showinfo("✅ Thành công", f"Ảnh đã resize và lưu tại:\n{resizePath}")

    except ValueError:
        messagebox.showerror("❌ Lỗi", "Chiều rộng hoặc chiều cao không hợp lệ.")
    except UnidentifiedImageError:
        messagebox.showerror("❌ Lỗi", "File không phải là ảnh hợp lệ.")
    except Exception as e:
        messagebox.showerror("❌ Lỗi", f"Không thể resize ảnh:\n{str(e)}")

def createGui():
    root = Tk()
    root.title("🧰 Công Cụ Ảnh - Hồ Trung Developer")
    root.geometry("600x350")
    root.resizable(True, True)

    label = Label(root, text="Chọn chức năng bạn muốn:", font=("Segoe UI", 14))
    label.pack(pady=20)

    btnRemove = Button(
        root,
        text="🪄 Xóa nền ảnh",
        command=removeBackgroundGui,
        font=("Segoe UI", 13),
        bg="#2196F3",
        fg="white",
        padx=15,
        pady=10,
    )
    btnRemove.pack(pady=5)

    btnOpenRemoved = Button(
        root,
        text="📂 Mở thư mục ảnh đã xóa nền",
        command=lambda: openFolder(REMOVED_BG_FOLDER),
        font=("Segoe UI", 11),
        bg="#1976D2",
        fg="white",
        padx=10,
        pady=6,
    )
    btnOpenRemoved.pack(pady=(0, 15))

    btnResize = Button(
        root,
        text="📐 Resize ảnh",
        command=resizeImageGui,
        font=("Segoe UI", 13),
        bg="#FF9800",
        fg="white",
        padx=15,
        pady=10,
    )
    btnResize.pack(pady=5)

    btnOpenResized = Button(
        root,
        text="📂 Mở thư mục ảnh đã resize",
        command=lambda: openFolder(RESIZED_FOLDER),
        font=("Segoe UI", 11),
        bg="#E67E22",
        fg="white",
        padx=10,
        pady=6,
    )
    btnOpenResized.pack(pady=(0, 15))

    root.mainloop()

if __name__ == "__main__":
    createGui()
