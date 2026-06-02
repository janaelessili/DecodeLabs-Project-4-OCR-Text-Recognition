# 🔍 OCR Text Recognition – Week 4 AI Internship Project

A beginner-friendly **Optical Character Recognition (OCR)** project built with Python, OpenCV, and Tesseract. This program loads an image containing text, applies image preprocessing techniques, and extracts machine-readable text from it.

---

## 📋 Table of Contents

- [Description](#-description)
- [How OCR Works](#-how-ocr-works)
- [Preprocessing Explained](#-preprocessing-explained)
- [Libraries Used](#-libraries-used)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [How to Run](#-how-to-run)
- [Sample Input / Output](#-sample-input--output)
- [Project Structure](#-project-structure)
- [Future Improvements](#-future-improvements)
- [License](#-license)

---

## 📖 Description

This project demonstrates the basics of **text recognition from images** using OCR technology. It follows a simple pipeline:

1. **Load** a sample image containing printed text
2. **Preprocess** the image to improve OCR accuracy
3. **Extract** text using the Tesseract OCR engine
4. **Display** the results with confidence analysis
5. **Save** a processed image and a comparison visualization

The code is well-commented and designed for beginners learning about computer vision and AI.

---

## 🧠 How OCR Works

**Optical Character Recognition (OCR)** is a technology that converts different types of documents — such as scanned papers, photos of documents, or images with text — into editable and searchable text data.

Here's a simplified flow:

```
📷 Image → 🔄 Preprocessing → 🔍 Character Detection → 📝 Text Output
```

The OCR engine (Tesseract) works by:
1. **Detecting text regions** in the image
2. **Segmenting** individual characters
3. **Recognizing** each character using trained models
4. **Assembling** characters into words and sentences

---

## 🔄 Preprocessing Explained

Raw images often contain noise, uneven lighting, or low contrast that can confuse the OCR engine. Preprocessing fixes these issues:

### 1. Grayscale Conversion
Converts the color image (3 channels: Blue, Green, Red) into a single-channel grayscale image. This simplifies processing and removes color-related noise.

### 2. Gaussian Blur
Applies a slight blur using a 5×5 kernel to smooth out small imperfections, speckles, and sensor noise. This prevents the OCR engine from misidentifying noise as characters.

### 3. Adaptive Thresholding
Converts the grayscale image to pure black and white. Unlike simple thresholding (which uses one global cutoff value), **adaptive thresholding** calculates different threshold values for different regions of the image. This handles uneven lighting much better — crucial for scanned documents.

---

## 📚 Libraries Used

| Library | Purpose |
|---------|---------|
| **OpenCV** (`cv2`) | Image loading, preprocessing (grayscale, blur, threshold), and saving |
| **pytesseract** | Python wrapper for the Tesseract OCR engine |
| **os / sys** | File path handling and error management |

---

## ✅ Requirements

- **Python** 3.7 or higher
- **Tesseract OCR** engine installed on your system
- Python packages listed in `requirements.txt`

---

## 🛠 Installation

### Step 1: Install Tesseract OCR Engine

Tesseract must be installed **separately** (it's not a Python package — pytesseract is just a wrapper).

**Windows:**
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer (default path: `C:\Program Files\Tesseract-OCR\`)
3. Add Tesseract to your system PATH, or set it in the script:
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install tesseract-ocr
```

### Step 2: Clone the Repository

```bash
git clone https://github.com/your-username/ocr-text-recognition.git
cd ocr-text-recognition
```

### Step 3: (Optional) Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Step 4: Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ How to Run

Make sure you have a sample image named `sample_input.png` in the project folder (one is included), then run:

```bash
python ocr_text_recognition.py
```

To use a **different image**, edit the `INPUT_IMAGE_PATH` variable at the top of the script:

```python
INPUT_IMAGE_PATH = "your_image.png"
```

---

## 📸 Sample Input / Output

### Input Image
A sample image (`sample_input.png`) is included in the project. You can replace it with any image containing printed text (photos of documents, screenshots, book pages, etc.).

### Terminal Output Example
```
============================================================
  🔍  OCR TEXT RECOGNITION – Week 4 AI Internship Project
============================================================
✅ Image loaded successfully: sample_input.png
   Dimensions: 800w × 600h pixels
   Channels:   3

🔄 Preprocessing Steps:
   [1/3] Converted to grayscale
   [2/3] Applied Gaussian blur (kernel: 5×5)
   [3/3] Applied adaptive thresholding

🔍 Running Tesseract OCR...

============================================================
  📝  EXTRACTED TEXT
============================================================
Welcome to OCR Text Recognition.
Optical Character Recognition converts images of text
into machine-readable text.
============================================================

📊 Confidence Analysis:
   Words detected:      15
   Average confidence:  87.3%
   Highest confidence:  96%
   Lowest confidence:   62%
   Quality rating:      🟢 Excellent – Text was recognized with high confidence.

💾 Processed image saved to: processed_output.png
📸 Comparison image saved to: processed_output_comparison.png

✅ OCR processing complete!
```

### Output Files
| File | Description |
|------|-------------|
| `processed_output.png` | The final thresholded image (what the OCR engine sees) |
| `processed_output_comparison.png` | Side-by-side comparison of all 4 preprocessing stages |

---

## 📁 Project Structure

```
ocr-text-recognition/
├── ocr_text_recognition.py    # Main script with OCR pipeline
├── sample_input.png           # Sample image for testing
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

---

## 🚀 Future Improvements

Here are ideas to extend this project:

1. **GUI Interface** – Add a simple GUI using Tkinter or Streamlit for drag-and-drop image upload
2. **Multi-language Support** – Configure Tesseract for other languages (`lang='fra'` for French, etc.)
3. **PDF Support** – Process multi-page PDF documents
4. **Handwriting Recognition** – Train or use models for handwritten text
5. **Batch Processing** – Process multiple images from a folder automatically
6. **Text-to-Speech** – Read extracted text aloud using `pyttsx3`
7. **Cloud Deployment** – Deploy as a web API using Flask or FastAPI
8. **Advanced Preprocessing** – Add deskewing, noise removal, and contrast enhancement
9. **Export Formats** – Save extracted text as `.txt`, `.docx`, or `.csv`
10. **Real-time OCR** – Use a webcam feed for live text recognition

---

## 📄 License

This project is open-source and available under the [MIT License](https://opensource.org/licenses/MIT).

---

> **Built with ❤️ as part of the Week 4 AI Internship Project**
