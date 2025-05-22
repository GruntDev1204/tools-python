import os
import subprocess
from tkinter import Tk, Button, Label, filedialog, messagebox, Toplevel, ttk
from PIL import Image
from moviepy.editor import VideoFileClip
import pillow_heif

DEFAULT_OUTPUT_FOLDER = r"D:\app\tool\media\toolConvert"
pillow_heif.register_heif_opener()


def openFolder(path):
    if os.path.exists(path):
        if os.name == "nt":
            os.startfile(path)
        elif os.name == "posix":
            subprocess.run(["open" if sys.platform == "darwin" else "xdg-open", path])
    else:
        messagebox.showerror("❌ Lỗi", f"Thư mục không tồn tại:\n{path}")


def convertHeicToPngOrJpg():
    filePath = filedialog.askopenfilename(
        title="Chọn file HEIC để chuyển sang PNG/JPG",
        filetypes=[("HEIC Files", "*.heic")],
    )
    if not filePath:
        return

    try:
        image = Image.open(filePath)
        baseName = os.path.splitext(os.path.basename(filePath))[0]
        output_folder = os.path.join(DEFAULT_OUTPUT_FOLDER, "images")
        outputPath = os.path.join(output_folder, f"{baseName}.png")

        os.makedirs(output_folder, exist_ok=True)
        image.save(outputPath, "PNG")

        if messagebox.askyesno(
            "✅ Thành công",
            f"Ảnh đã chuyển sang PNG và lưu tại:\n{outputPath}\n\nBạn có muốn mở thư mục chứa file không?",
        ):
            openFolder(output_folder)
    except Exception as e:
        messagebox.showerror("❌ Lỗi", f"Không thể chuyển đổi ảnh:\n{str(e)}")


def convertVideoToMp4():
    filePath = filedialog.askopenfilename(
        title="Chọn file video để chuyển sang MP4",
        filetypes=[
            ("Video Files", "*.mov *.mp4 *.mkv *.hevc"),
            ("MOV Files", "*.mov"),
            ("MP4 Files", "*.mp4"),
            ("MKV Files", "*.mkv"),
            ("HEVC Files", "*.hevc"),
        ],
    )
    if not filePath:
        return

    loading_popup = Toplevel()
    loading_popup.title("⏳ Đang chuyển đổi video...")
    loading_popup.geometry("300x100")
    Label(loading_popup, text="Đang xử lý video, vui lòng chờ...").pack(pady=10)
    pb = ttk.Progressbar(loading_popup, mode="indeterminate")
    pb.pack(fill="x", padx=20, pady=5)
    pb.start()

    loading_popup.update()

    try:
        video = VideoFileClip(filePath)
        baseName = os.path.splitext(os.path.basename(filePath))[0]
        output_folder = os.path.join(DEFAULT_OUTPUT_FOLDER, "mp4_converter")
        outputPath = os.path.join(output_folder, f"{baseName}.mp4")

        os.makedirs(output_folder, exist_ok=True)
        video.write_videofile(outputPath, codec="libx264")
        video.close()

        loading_popup.destroy()

        if messagebox.askyesno(
            "✅ Thành công",
            f"Video đã chuyển sang MP4 và lưu tại:\n{outputPath}\n\nBạn có muốn mở thư mục chứa file không?",
        ):
            openFolder(output_folder)
    except Exception as e:
        loading_popup.destroy()
        messagebox.showerror("❌ Lỗi", f"Không thể chuyển đổi video:\n{str(e)}")


def extractAudioFromMp4():
    filePath = filedialog.askopenfilename(
        title="Chọn file video MP4 để tách audio", filetypes=[("MP4 Files", "*.mp4")]
    )
    if not filePath:
        return

    loading_popup = Toplevel()
    loading_popup.title("⏳ Đang tách audio từ video...")
    loading_popup.geometry("300x100")
    Label(loading_popup, text="Đang xử lý audio, vui lòng chờ...").pack(pady=10)
    pb = ttk.Progressbar(loading_popup, mode="indeterminate")
    pb.pack(fill="x", padx=20, pady=5)
    pb.start()

    loading_popup.update()

    try:
        video = VideoFileClip(filePath)
        baseName = os.path.splitext(os.path.basename(filePath))[0]
        output_folder = os.path.join(DEFAULT_OUTPUT_FOLDER, "mp3_got_from_video")
        outputPath = os.path.join(output_folder, f"{baseName}.mp3")

        os.makedirs(output_folder, exist_ok=True)
        video.audio.write_audiofile(outputPath)
        video.close()

        loading_popup.destroy()

        if messagebox.askyesno(
            "✅ Thành công",
            f"Audio đã được tách và lưu tại:\n{outputPath}\n\nBạn có muốn mở thư mục chứa file không?",
        ):
            openFolder(output_folder)
    except Exception as e:
        loading_popup.destroy()
        messagebox.showerror("❌ Lỗi", f"Không thể tách audio:\n{str(e)}")


def muteVideoMp4():
    filePath = filedialog.askopenfilename(
        title="Chọn file video MP4 để tắt tiếng", filetypes=[("MP4 Files", "*.mp4")]
    )
    if not filePath:
        return

    loading_popup = Toplevel()
    loading_popup.title("⏳ Đang tắt tiếng video...")
    loading_popup.geometry("300x100")
    Label(loading_popup, text="Đang xử lý video, vui lòng chờ...").pack(pady=10)
    pb = ttk.Progressbar(loading_popup, mode="indeterminate")
    pb.pack(fill="x", padx=20, pady=5)
    pb.start()

    loading_popup.update()

    try:
        video = VideoFileClip(filePath)
        baseName = os.path.splitext(os.path.basename(filePath))[0]
        output_folder = os.path.join(DEFAULT_OUTPUT_FOLDER, "muted_video")
        outputPath = os.path.join(output_folder, f"{baseName}_muted.mp4")

        os.makedirs(output_folder, exist_ok=True)

        video_without_audio = video.without_audio()
        video_without_audio.write_videofile(outputPath, codec="libx264")
        video.close()

        loading_popup.destroy()

        if messagebox.askyesno(
            "✅ Thành công",
            f"Đã tắt tiếng video và lưu tại:\n{outputPath}\n\nBạn có muốn mở thư mục chứa file không?",
        ):
            openFolder(output_folder)
    except Exception as e:
        loading_popup.destroy()
        messagebox.showerror("❌ Lỗi", f"Không thể tắt tiếng video:\n{str(e)}")


def createConverterGui():
    root = Tk()
    root.title("🎥🎞️ Video & Ảnh Converter - Hồ Trung Developer")
    root.geometry("1000x500")
    root.resizable(True, True)

    label = Label(root, text="Chọn công cụ bạn muốn sử dụng:", font=("Segoe UI", 14))
    label.pack(pady=20)

    btnVideo = Button(
        root,
        text="🎬 Chuyển Video (MOV/HEVC/MP4/MKV) → MP4",
        command=convertVideoToMp4,
        font=("Segoe UI", 13),
        bg="#2196F3",
        fg="white",
        padx=15,
        pady=10,
    )
    btnVideo.pack(pady=10)

    btnExtractAudio = Button(
        root,
        text="🎧 Tách Audio từ Video MP4",
        command=extractAudioFromMp4,
        font=("Segoe UI", 13),
        bg="#4CAF50",
        fg="white",
        padx=15,
        pady=10,
    )
    btnExtractAudio.pack(pady=10)

    btnMuteVideo = Button(
        root,
        text="🔇 Tắt tiếng Video MP4",
        command=muteVideoMp4,
        font=("Segoe UI", 13),
        bg="#9E9E9E",
        fg="white",
        padx=15,
        pady=10,
    )
    btnMuteVideo.pack(pady=10)

    btnHeic = Button(
        root,
        text="🖼️ Chuyển HEIC → PNG",
        command=convertHeicToPngOrJpg,
        font=("Segoe UI", 13),
        bg="#FF5722",
        fg="white",
        padx=15,
        pady=10,
    )
    btnHeic.pack(pady=10)

    def openDfaultFolder():
        openFolder(DEFAULT_OUTPUT_FOLDER)

    btnOpenFolder = Button(
        root,
        text="📁 Mở thư mục lưu file chung",
        command=openDfaultFolder,
        font=("Segoe UI", 12),
        bg="#607D8B",
        fg="white",
        padx=10,
        pady=8,
    )
    btnOpenFolder.pack(side="bottom", pady=15)

    root.mainloop()


if __name__ == "__main__":
    createConverterGui()
