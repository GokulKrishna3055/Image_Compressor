

---

# Image Compression Platform

## Overview

This project is a web-based platform for compressing images using Singular Value Decomposition (SVD). It allows users to upload images, apply compression, and download the compressed version. The platform is built using Flask for the backend and HTML/CSS for the frontend.

## Features

- **Image Upload**: Upload images for compression.
- **Compression Rate**: Specify the compression rate to determine the degree of compression.
- **Image Preview**: View the original and compressed images.
- **Download**: Download the compressed image.

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML, CSS
- **Image Processing**: PIL (Pillow), NumPy

## Directory Structure

```
/image_compressor
|-- app.py
|-- templates
|   |-- index.html
|   |-- display.html
|-- static
|   |-- uploads
|   |-- compressed_image
```

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/GokulKrishna3055/image_compressor.git
   cd image_compressor
   ```

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

5. **Access the Application**:
   Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage

1. **Upload an Image**: Select an image file from your computer. Supported image types are JPEG, PNG, and BMP. Ensure the image size is within the limit of 5MB.
2. **Specify Compression Rate**: Enter a value between 0 and 100 to set the compression rate.
3. **Submit**: Click the "Submit" button to compress the image.
4. **View Results**: The original and compressed images are displayed along with their sizes.
5. **Download**: Click the "Download Compressed Image" button to download the compressed image.

## Code Explanation

### `app.py`

This is the main Flask application file.

- **Routes**:
  - `/`: Handles the image upload and compression logic.
  - `/download/<filename>`: Serves the compressed image file for download.

- **Functions**:
  - `compress_image()`: Manages image upload, compression, and rendering of results.
  - `download_compressed_image(filename)`: Handles the download request for compressed images.

### `index.html`

The main HTML template for the image upload form.

- **Form**: Allows users to upload an image and specify the compression rate.
- **Messages**: Displays flash messages for errors or information.

### `display.html`

The HTML template for displaying the original and compressed images.

- **Image Previews**: Shows the original and compressed images with their sizes.
- **Download Link**: Provides a link to download the compressed image.

## Dependencies

- Flask
- NumPy
- Pillow

Install dependencies using:
```bash
pip install flask numpy pillow
```

## Contributing

1. **Fork the Repository**: Fork this repository to your own GitHub account.
2. **Create a Branch**: Create a branch for your changes.
   ```bash
   git checkout -b feature-branch
   ```
3. **Commit Your Changes**: Commit your changes with a clear message.
   ```bash
   git commit -m "Add new feature"
   ```
4. **Push to the Branch**: Push your changes to the branch.
   ```bash
   git push origin feature-branch
   ```
5. **Create a Pull Request**: Open a pull request to merge your changes into the main repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

For any questions or suggestions, please contact:

- Name: Gokul Krishna N
- Email: gk9621rf@gmail.com
- GitHub: [GokulKrishna3055](https://github.com/GokulKrishna3055)

---
