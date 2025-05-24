Hướng dẫn sửa===========================
📌 HƯỚNG DẪN CÀI ĐẶT - TIẾNG VIỆT
===========================

✅ Yêu cầu:
- Cài Python 3.10+ từ https://www.python.org/
  (Chọn "Add Python to PATH" khi cài)
- Clone repo này về

2. Cài thư viện:
   pip install -r requirements.txt

3. (Nếu chưa cài) Cài thêm PyInstaller:
   pip install pyinstaller

4. Build file exe:
   pyinstaller --noconsole --onefile ....py

5. File EXE sẽ nằm ở:
   dist/document_tool.exe

👉 Nếu có dùng Tesseract OCR:
- Tải ở: https://github.com/UB-Mannheim/tesseract/wiki
- Đặt đường dẫn vào file Python:
  pytesseract.pytesseract.tesseract_cmd = r"D:\duong\dan\tesseract.exe"

================================
📌 INSTALL GUIDE - ENGLISH
================================

✅ Requirements:
- Install Python 3.10+ from https://www.python.org/
  (Tick "Add Python to PATH" during installation)
- Clone this repo

2. Install required packages:
   pip install -r requirements.txt

3. (If not installed) Install PyInstaller:
   pip install pyinstaller

4. Build the executable:
   pyinstaller --noconsole --onefile ....py

5. The EXE file will be in:
   dist/document_tool.exe

👉 If your app uses Tesseract OCR:
- Download it here: https://github.com/UB-Mannheim/tesseract/wiki
- Set the path in your Python script:
  pytesseract.pytesseract.tesseract_cmd = r"D:\path\to\tesseract.exe"
