from tkinter import filedialog, Tk, Button, Label, messagebox, StringVar
from pdf2docx import Converter
from docx2pdf import convert
import pytesseract
from PIL import Image
import os
import threading
import subprocess
import sys

pytesseract.pytesseract.tesseract_cmd = r"E:\ProgramFile\OCR\tesseract.exe"
os.environ["TQDM_DISABLE"] = "1"

PDF_TO_WORD_OUTPUT = r"D:\app\tool\document\pdf_to_word"
IMAGE_TO_TEXT_OUTPUT = r"D:\app\tool\document\text_from_photo"
WORD_TO_PDF_OUTPUT = r"D:\app\tool\document\word_to_pdf"

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")


def openFolder(path):
    if os.path.exists(path):
        subprocess.Popen(f'explorer "{path}"')
    else:
        messagebox.showerror("Lỗi ❌", f"Folder không tồn tại:\n{path}")


def setLoading(text):
    loadingVar.set(text)
    root.update_idletasks()


def pdfToWord():
    try:
        pdfPath = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if not pdfPath:
            return
        baseName = os.path.basename(pdfPath).replace(".pdf", ".docx")
        docxPath = os.path.join(PDF_TO_WORD_OUTPUT, baseName)

        def task():
            try:
                setLoading("⏳ Đang chuyển PDF ➜ Word ...")
                cv = Converter(pdfPath)
                cv.convert(docxPath, start=0, end=None)
                cv.close()
                setLoading("")
                messagebox.showinfo("Thành công 🎉", f"✅ PDF ➜ Word: {docxPath}")
            except Exception as e:
                setLoading("")
                messagebox.showerror(
                    "Lỗi ❌", f"Chuyển đổi PDF ➜ Word thất bại:\n{str(e)}"
                )

        threading.Thread(target=task).start()

    except Exception as ex:
        messagebox.showerror("Lỗi ❌", f"Không thể chuyển đổi PDF ➜ Word:\n{str(ex)}")


def imageToText():
    try:
        imgPath = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png;*.jpg;*.jpeg")]
        )
        if not imgPath:
            return
        baseName = os.path.basename(imgPath)
        txtName = os.path.splitext(baseName)[0] + ".txt"
        txtPath = os.path.join(IMAGE_TO_TEXT_OUTPUT, txtName)

        def task():
            try:
                setLoading("⏳ Đang quét ảnh ➜ Text ...")
                img = Image.open(imgPath)
                text = pytesseract.image_to_string(img, lang="eng")
                with open(txtPath, "w", encoding="utf-8") as f:
                    f.write(text)
                setLoading("")
                messagebox.showinfo("Thành công 🎉", f"✅ Ảnh ➜ Text: {txtPath}")
            except Exception as e:
                setLoading("")
                messagebox.showerror("Lỗi ❌", f"Quét ảnh thất bại:\n{str(e)}")

        threading.Thread(target=task).start()

    except Exception as ex:
        messagebox.showerror("Lỗi ❌", f"Không thể quét ảnh:\n{str(ex)}")


def wordToPdf():
    try:
        docxPath = filedialog.askopenfilename(filetypes=[("Word files", "*.docx")])
        if not docxPath:
            return
        baseName = os.path.basename(docxPath).replace(".docx", ".pdf")
        outputPdf = os.path.join(WORD_TO_PDF_OUTPUT, baseName)

        def task():
            try:
                setLoading("⏳ Đang chuyển Word ➜ PDF ...")

                convert(docxPath, outputPdf)
                setLoading("")
                messagebox.showinfo("Thành công 🎉", f"✅ Word ➜ PDF: {outputPdf}")
            except Exception as e:
                setLoading("")
                import traceback

                # messagebox.showerror("Lỗi ❌", f"Chuyển đổi Word ➜ PDF thất bại:\n{str(e)}")
                messagebox.showerror(
                    "Lỗi ❌",
                    f"Chuyển đổi Word ➜ PDF thất bại:\n{traceback.format_exc()}",
                )

        threading.Thread(target=task).start()

    except Exception as ex:
        messagebox.showerror("Lỗi ❌", f"Không thể chuyển đổi Word ➜ PDF:\n{str(ex)}")


root = Tk()
root.title("🛠️ Tool Chuyển Đổi Tài Liệu - Hồ Trung developer")
root.geometry("520x400")

loadingVar = StringVar()
loadingLabel = Label(root, textvariable=loadingVar, font=("Arial", 11), fg="blue")
loadingLabel.pack(pady=10)

Label(root, text="📌 Chọn chức năng:", font=("Arial", 14, "bold")).pack(pady=10)

framePdfWord = Button(
    root,
    text="📄 PDF ➜ Word",
    width=30,
    command=pdfToWord,
    bg="#4caf50",
    fg="white",
    font=("Arial", 12, "bold"),
)
framePdfWord.pack(pady=8)
btnOpenPdfWordFolder = Button(
    root,
    text="📂 Mở thư mục PDF ➜ Word",
    width=30,
    command=lambda: openFolder(PDF_TO_WORD_OUTPUT),
)
btnOpenPdfWordFolder.pack()

btnImageToText = Button(
    root,
    text="🖼️ Ảnh ➜ Text (.txt)",
    width=30,
    command=imageToText,
    bg="#2196f3",
    fg="white",
    font=("Arial", 12, "bold"),
)
btnImageToText.pack(pady=8)
btnOpenImageTextFolder = Button(
    root,
    text="📂 Mở thư mục Ảnh ➜ Text",
    width=30,
    command=lambda: openFolder(IMAGE_TO_TEXT_OUTPUT),
)
btnOpenImageTextFolder.pack()

btnWordToPdf = Button(
    root,
    text="📝 Word ➜ PDF",
    width=30,
    command=wordToPdf,
    bg="#f44336",
    fg="white",
    font=("Arial", 12, "bold"),
)
btnWordToPdf.pack(pady=8)
btnOpenWordPdfFolder = Button(
    root,
    text="📂 Mở thư mục Word ➜ PDF",
    width=30,
    command=lambda: openFolder(WORD_TO_PDF_OUTPUT),
)
btnOpenWordPdfFolder.pack()

root.mainloop()
