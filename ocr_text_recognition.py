"""
==========================================================
  Week 4 AI Internship Project: OCR Text Recognition
==========================================================
  This script performs Optical Character Recognition (OCR)
  on a sample image using pytesseract and OpenCV.

  Steps:
    1. Load the input image
    2. Preprocess (grayscale, blur, adaptive threshold)
    3. Extract text using Tesseract OCR
    4. Display results with confidence info
    5. Save the processed image
==========================================================
"""

import cv2               # OpenCV for image processing
import pytesseract        # Python wrapper for Tesseract OCR engine
import os
import sys

# Fix for Windows terminals that don't support UTF-8 by default.
# This ensures emoji and special characters print correctly.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass  # If reconfigure isn't available, continue anyway


# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
# On Windows, set the path to the Tesseract executable if it's not in PATH.
# The installer typically places it in "C:\Program Files\Tesseract-OCR\".
# If you installed Tesseract elsewhere, update this path accordingly.
if sys.platform == "win32":
    tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if os.path.exists(tesseract_path):
        pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Path to the input image (change this to your own image if needed)
INPUT_IMAGE_PATH = "sample_input.png"

# Path where the processed (preprocessed) image will be saved
OUTPUT_IMAGE_PATH = "processed_output.png"


def load_image(image_path):
    """
    Step 1: Load the image from disk.

    Args:
        image_path (str): Path to the image file.

    Returns:
        numpy.ndarray: The loaded image in BGR color format.
    """
    # Check if the file actually exists before trying to load it
    if not os.path.exists(image_path):
        print(f"\n❌ Error: Image file '{image_path}' not found!")
        print("   Please place a sample image named 'sample_input.png' in this folder.")
        print("   You can use any image that contains printed text.")
        sys.exit(1)

    # cv2.imread() loads the image as a NumPy array in BGR format
    image = cv2.imread(image_path)

    if image is None:
        print(f"\n❌ Error: Could not read '{image_path}'. The file may be corrupted.")
        sys.exit(1)

    print(f"✅ Image loaded successfully: {image_path}")
    print(f"   Dimensions: {image.shape[1]}w × {image.shape[0]}h pixels")
    print(f"   Channels:   {image.shape[2]}")
    return image


def preprocess_image(image):
    """
    Step 2: Apply preprocessing to improve OCR accuracy.

    Preprocessing pipeline:
      1. Convert to grayscale   – removes color noise
      2. Gaussian blur          – smooths out small imperfections
      3. Adaptive thresholding  – creates a clean black-and-white image

    Args:
        image (numpy.ndarray): The original BGR image.

    Returns:
        tuple: (grayscale_image, blurred_image, thresholded_image)
    """
    # --- 2a. Grayscale Conversion ---
    # Converting to grayscale simplifies the image from 3 channels (BGR)
    # to a single channel, making processing faster and more reliable.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print("\n🔄 Preprocessing Steps:")
    print("   [1/3] Converted to grayscale")

    # --- 2b. Gaussian Blur ---
    # A slight blur removes small noise and artifacts from the image.
    # The kernel size (5, 5) controls how much blurring is applied.
    # A larger kernel = more blur. We use a small one to keep text sharp.
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    print("   [2/3] Applied Gaussian blur (kernel: 5×5)")

    # --- 2c. Adaptive Thresholding ---
    # Adaptive thresholding converts the image to pure black and white.
    # Unlike simple thresholding, it adapts to different lighting areas
    # in the image, which works much better for scanned documents.
    #
    # Parameters explained:
    #   - 255: Maximum value to assign (white)
    #   - ADAPTIVE_THRESH_GAUSSIAN_C: Uses weighted sum of neighborhood
    #   - THRESH_BINARY: Output is either black (0) or white (255)
    #   - 11: Size of the neighborhood area for threshold calculation
    #   - 2: Constant subtracted from the mean (fine-tunes results)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    print("   [3/3] Applied adaptive thresholding")

    return gray, blurred, thresh


def extract_text(processed_image):
    """
    Step 3: Use Tesseract OCR to extract text from the processed image.

    Args:
        processed_image (numpy.ndarray): The preprocessed (thresholded) image.

    Returns:
        str: The extracted text.
    """
    # pytesseract.image_to_string() sends the image to the Tesseract
    # OCR engine and returns the recognized text as a Python string.
    extracted_text = pytesseract.image_to_string(processed_image)
    return extracted_text


def get_confidence_data(processed_image):
    """
    Step 4: Get word-level confidence scores from Tesseract.

    Tesseract can report how confident it is about each word it recognizes.
    Confidence ranges from 0 (low) to 100 (high).

    Args:
        processed_image (numpy.ndarray): The preprocessed image.

    Returns:
        dict: Word-level OCR data including confidence scores.
    """
    # image_to_data() returns detailed info about each detected word,
    # including bounding boxes, text content, and confidence levels.
    data = pytesseract.image_to_data(
        processed_image,
        output_type=pytesseract.Output.DICT
    )
    return data


def display_results(extracted_text, confidence_data):
    """
    Step 5: Display the extracted text and confidence analysis.

    Args:
        extracted_text (str): The full extracted text string.
        confidence_data (dict): Word-level OCR data with confidence.
    """
    print("\n" + "=" * 60)
    print("  📝  EXTRACTED TEXT")
    print("=" * 60)

    # Clean up the text (remove excess blank lines)
    clean_text = "\n".join(
        line for line in extracted_text.splitlines() if line.strip()
    )

    if clean_text.strip():
        print(clean_text)
    else:
        print("  (No text could be extracted from this image)")

    print("=" * 60)

    # --- Confidence Analysis ---
    # Filter out empty detections (Tesseract returns some blank entries)
    words = []
    confidences = []
    for i in range(len(confidence_data["text"])):
        word = confidence_data["text"][i].strip()
        conf = int(confidence_data["conf"][i])
        if word and conf > 0:  # Only count actual words with valid confidence
            words.append(word)
            confidences.append(conf)

    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
        min_confidence = min(confidences)
        max_confidence = max(confidences)
        word_count = len(words)

        print(f"\n📊 Confidence Analysis:")
        print(f"   Words detected:      {word_count}")
        print(f"   Average confidence:  {avg_confidence:.1f}%")
        print(f"   Highest confidence:  {max_confidence}%")
        print(f"   Lowest confidence:   {min_confidence}%")

        # Provide a human-readable quality rating
        if avg_confidence >= 80:
            rating = "🟢 Excellent – Text was recognized with high confidence."
        elif avg_confidence >= 60:
            rating = "🟡 Good – Most text was recognized reliably."
        elif avg_confidence >= 40:
            rating = "🟠 Fair – Some words may be inaccurate. Try a cleaner image."
        else:
            rating = "🔴 Poor – Consider using a higher-quality image."

        print(f"   Quality rating:      {rating}")

        # Show low-confidence words as warnings
        low_conf_words = [
            (words[i], confidences[i])
            for i in range(len(words))
            if confidences[i] < 50
        ]
        if low_conf_words:
            print(f"\n⚠️  Low-confidence words (< 50%):")
            for word, conf in low_conf_words[:10]:  # Show at most 10
                print(f'      "{word}" → {conf}% confidence')
    else:
        print("\n⚠️  No confidence data available.")


def save_processed_image(thresh, output_path):
    """
    Step 6: Save the preprocessed (thresholded) image to disk.

    This lets you visually inspect what the OCR engine 'sees'
    after preprocessing.

    Args:
        thresh (numpy.ndarray): The thresholded image.
        output_path (str): Path to save the output image.
    """
    cv2.imwrite(output_path, thresh)
    print(f"\n💾 Processed image saved to: {output_path}")


def create_comparison_image(original, gray, blurred, thresh, output_path):
    """
    Bonus: Create a side-by-side comparison showing all preprocessing stages.

    This helps visualize how each step transforms the image.

    Args:
        original (numpy.ndarray): Original BGR image.
        gray (numpy.ndarray): Grayscale image.
        blurred (numpy.ndarray): Blurred image.
        thresh (numpy.ndarray): Thresholded image.
        output_path (str): Base path for saving.
    """
    # Get dimensions – resize all images to same height for comparison
    height = 400
    aspect = original.shape[1] / original.shape[0]
    width = int(height * aspect)

    # Resize all images to the same dimensions
    original_resized = cv2.resize(original, (width, height))
    gray_resized = cv2.resize(gray, (width, height))
    blurred_resized = cv2.resize(blurred, (width, height))
    thresh_resized = cv2.resize(thresh, (width, height))

    # Convert single-channel images to 3-channel so we can stack them
    gray_3ch = cv2.cvtColor(gray_resized, cv2.COLOR_GRAY2BGR)
    blurred_3ch = cv2.cvtColor(blurred_resized, cv2.COLOR_GRAY2BGR)
    thresh_3ch = cv2.cvtColor(thresh_resized, cv2.COLOR_GRAY2BGR)

    # Add labels to each stage
    font = cv2.FONT_HERSHEY_SIMPLEX
    label_color = (0, 200, 0)  # Green text
    cv2.putText(original_resized, "1. Original", (10, 30), font, 0.7, label_color, 2)
    cv2.putText(gray_3ch, "2. Grayscale", (10, 30), font, 0.7, label_color, 2)
    cv2.putText(blurred_3ch, "3. Blurred", (10, 30), font, 0.7, label_color, 2)
    cv2.putText(thresh_3ch, "4. Thresholded", (10, 30), font, 0.7, label_color, 2)

    # Stack images: top row = original + grayscale, bottom row = blurred + threshold
    top_row = cv2.hconcat([original_resized, gray_3ch])
    bottom_row = cv2.hconcat([blurred_3ch, thresh_3ch])
    comparison = cv2.vconcat([top_row, bottom_row])

    comparison_path = os.path.splitext(output_path)[0] + "_comparison.png"
    cv2.imwrite(comparison_path, comparison)
    print(f"📸 Comparison image saved to: {comparison_path}")


# ─────────────────────────────────────────────
# MAIN PROGRAM
# ─────────────────────────────────────────────
def main():
    """Main function that orchestrates the entire OCR pipeline."""

    print("\n" + "=" * 60)
    print("  🔍  OCR TEXT RECOGNITION – Week 4 AI Internship Project")
    print("=" * 60)

    # Step 1: Load the image
    image = load_image(INPUT_IMAGE_PATH)

    # Step 2: Preprocess the image
    gray, blurred, thresh = preprocess_image(image)

    # Step 3: Extract text using Tesseract OCR
    print("\n🔍 Running Tesseract OCR...")
    extracted_text = extract_text(thresh)

    # Step 4: Get confidence data
    confidence_data = get_confidence_data(thresh)

    # Step 5: Display results
    display_results(extracted_text, confidence_data)

    # Step 6: Save the processed image
    save_processed_image(thresh, OUTPUT_IMAGE_PATH)

    # Bonus: Save a comparison image showing all preprocessing stages
    create_comparison_image(image, gray, blurred, thresh, OUTPUT_IMAGE_PATH)

    print("\n✅ OCR processing complete!\n")


# This ensures main() only runs when the script is executed directly
# (not when it's imported as a module)
if __name__ == "__main__":
    main()
