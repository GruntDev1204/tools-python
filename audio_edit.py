import os
import subprocess
from tkinter import Tk, Button, Label, filedialog, messagebox, simpledialog
from pydub import AudioSegment

BASE_OUTPUT_FOLDER = r"D:\app\tool\audio"


class AudioToolGui:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Audio Tool - Hồ Trung Developer")
        self.root.geometry("1000x500")

        self.audioPath = None
        self.audioSegment = None

        Label(root, text="Chọn chức năng bạn muốn:", font=("Segoe UI", 14)).pack(
            pady=15
        )

        Button(
            root,
            text="📂 Chọn file âm thanh (MP3 hoặc WAV)",
            command=self.loadAudio,
            bg="#4CAF50",
            fg="white",
            font=("Segoe UI", 12),
        ).pack(pady=10)

        self.labelFile = Label(root, text="Chưa chọn file nào", font=("Segoe UI", 11))
        self.labelFile.pack(pady=5)

        Button(
            root,
            text="🎵 Chuyển MP3 -> WAV",
            command=self.convertMp3ToWav,
            font=("Segoe UI", 12),
            bg="#2196F3",
            fg="white",
        ).pack(pady=8)

        Button(
            root,
            text="✂️ Cắt phân đoạn",
            command=self.cutAudioSegment,
            font=("Segoe UI", 12),
            bg="#FF9800",
            fg="white",
        ).pack(pady=8)

        Button(
            root,
            text="🎚️ Tăng/Giảm tone (Pitch)",
            command=self.changePitch,
            font=("Segoe UI", 12),
            bg="#9C27B0",
            fg="white",
        ).pack(pady=8)

        Button(
            root,
            text="⏩ Tăng/Giảm tốc độ (Speed)",
            command=self.changeSpeed,
            font=("Segoe UI", 12),
            bg="#F44336",
            fg="white",
        ).pack(pady=8)

        Button(
            root,
            text="📁 Mở thư mục lưu kết quả",
            command=self.openOutputFolder,
            font=("Segoe UI", 12),
            bg="#607D8B",
            fg="white",
        ).pack(pady=12)

    def loadAudio(self):
        filetypes = [("Audio Files", "*.mp3 *.wav")]
        path = filedialog.askopenfilename(
            title="Chọn file âm thanh", filetypes=filetypes
        )
        if not path:
            return
        try:
            self.audioSegment = AudioSegment.from_file(path)
            self.audioPath = path
            self.labelFile.config(text=f"Đã chọn: {os.path.basename(path)}")
            messagebox.showinfo("✅ Thành công", "File âm thanh đã được tải.")
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể mở file âm thanh:\n{str(e)}")

    def convertMp3ToWav(self):
        if not self.audioPath or not self.audioSegment:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn file âm thanh MP3 trước.")
            return
        ext = os.path.splitext(self.audioPath)[1].lower()
        if ext != ".mp3":
            messagebox.showerror("❌ Lỗi", "File hiện tại không phải MP3.")
            return
        try:
            outputFolder = os.path.join(BASE_OUTPUT_FOLDER, "converted")
            os.makedirs(outputFolder, exist_ok=True)
            baseName = os.path.splitext(os.path.basename(self.audioPath))[0]
            outputPath = os.path.join(outputFolder, f"{baseName}.wav")
            self.audioSegment.export(outputPath, format="wav")
            messagebox.showinfo(
                "✅ Thành công", f"Đã chuyển MP3 sang WAV:\n{outputPath}"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Chuyển đổi thất bại:\n{str(e)}")

    def cutAudioSegment(self):
        if not self.audioSegment:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn file âm thanh trước.")
            return
        try:
            duration_ms = len(self.audioSegment)
            start_sec = simpledialog.askfloat(
                "Thời gian bắt đầu (giây)",
                f"Nhập thời gian bắt đầu (0 - {duration_ms/1000:.2f}):",
            )
            end_sec = simpledialog.askfloat(
                "Thời gian kết thúc (giây)",
                f"Nhập thời gian kết thúc ({start_sec} - {duration_ms/1000:.2f}):",
            )
            if start_sec is None or end_sec is None:
                return
            if not (0 <= start_sec < end_sec <= duration_ms / 1000):
                messagebox.showerror("❌ Lỗi", "Thời gian không hợp lệ.")
                return
            start_ms = int(start_sec * 1000)
            end_ms = int(end_sec * 1000)
            segment = self.audioSegment[start_ms:end_ms]
            outputFolder = os.path.join(BASE_OUTPUT_FOLDER, "cutted")
            os.makedirs(outputFolder, exist_ok=True)
            baseName = os.path.splitext(os.path.basename(self.audioPath))[0]
            ext = os.path.splitext(self.audioPath)[1].lower().replace(".", "")
            outputPath = os.path.join(
                outputFolder, f"{baseName}_cut_{int(start_sec)}-{int(end_sec)}.{ext}"
            )
            segment.export(outputPath, format=ext)
            messagebox.showinfo(
                "✅ Thành công", f"Đã cắt phân đoạn và lưu tại:\n{outputPath}"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Cắt phân đoạn thất bại:\n{str(e)}")

    def changePitch(self):
        if not self.audioSegment:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn file âm thanh trước.")
            return
        try:
            steps = simpledialog.askinteger(
                "Tăng/Giảm tone",
                "Nhập số nửa cung tăng(+) hoặc giảm(-) tone (ví dụ 2 hoặc -2):",
            )
            if steps is None:
                return
            newAudio = self.pitchShift(self.audioSegment, steps)
            outputFolder = os.path.join(BASE_OUTPUT_FOLDER, "changed_tone")
            os.makedirs(outputFolder, exist_ok=True)
            baseName = os.path.splitext(os.path.basename(self.audioPath))[0]
            ext = os.path.splitext(self.audioPath)[1].lower().replace(".", "")
            outputPath = os.path.join(
                outputFolder, f"{baseName}_pitch_{steps:+d}.{ext}"
            )
            newAudio.export(outputPath, format=ext)
            messagebox.showinfo(
                "✅ Thành công", f"Đã thay đổi tone và lưu tại:\n{outputPath}"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Thay đổi tone thất bại:\n{str(e)}")

    def pitchShift(self, audioSegment, semitones):
        newSampleRate = int(audioSegment.frame_rate * (2.0 ** (semitones / 12.0)))
        shifted = audioSegment._spawn(
            audioSegment.raw_data, overrides={"frame_rate": newSampleRate}
        )
        return shifted.set_frame_rate(audioSegment.frame_rate)

    def changeSpeed(self):
        if not self.audioSegment:
            messagebox.showerror("❌ Lỗi", "Vui lòng chọn file âm thanh trước.")
            return
        try:
            speedFactor = simpledialog.askfloat(
                "Tăng/Giảm tốc độ",
                "Nhập hệ số tốc độ (ví dụ 1.5 là nhanh hơn, 0.7 là chậm hơn):",
            )
            if speedFactor is None or speedFactor <= 0:
                messagebox.showerror("❌ Lỗi", "Hệ số tốc độ phải lớn hơn 0.")
                return
            newAudio = self.speedChange(self.audioSegment, speedFactor)
            outputFolder = os.path.join(BASE_OUTPUT_FOLDER, "change_speed")
            os.makedirs(outputFolder, exist_ok=True)
            baseName = os.path.splitext(os.path.basename(self.audioPath))[0]
            ext = os.path.splitext(self.audioPath)[1].lower().replace(".", "")
            outputPath = os.path.join(
                outputFolder, f"{baseName}_speed_{speedFactor:.2f}.{ext}"
            )
            newAudio.export(outputPath, format=ext)
            messagebox.showinfo(
                "✅ Thành công", f"Đã thay đổi tốc độ và lưu tại:\n{outputPath}"
            )
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Thay đổi tốc độ thất bại:\n{str(e)}")

    def speedChange(self, audioSegment, speed=1.0):
        newFrameRate = int(audioSegment.frame_rate * speed)
        spedUp = audioSegment._spawn(
            audioSegment.raw_data, overrides={"frame_rate": newFrameRate}
        )
        return spedUp.set_frame_rate(audioSegment.frame_rate)

    def openOutputFolder(self):
        if not os.path.exists(BASE_OUTPUT_FOLDER):
            messagebox.showwarning(
                "⚠️ Thư mục không tồn tại",
                f"Thư mục {BASE_OUTPUT_FOLDER} chưa được tạo.",
            )
            return
        try:
            subprocess.Popen(f'explorer "{BASE_OUTPUT_FOLDER}"')
        except Exception as e:
            messagebox.showerror("❌ Lỗi", f"Không thể mở thư mục:\n{str(e)}")


def main():
    root = Tk()
    app = AudioToolGui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
