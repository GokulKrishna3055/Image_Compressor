import numpy as np
from PIL import Image, ImageOps
import os, base64
from io import BytesIO
from flask import Flask, request, render_template, flash, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['COMPRESSED_FOLDER'] = 'static/compressed_image'
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def compress_image():
    if request.method == 'POST':
        image_file = request.files['image']
        compression_r = int(request.form['cr'])

        if image_file.filename != '':
            try:
                temp_image = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
                image_file.save(temp_image)
                original_image_size = os.path.getsize(temp_image)
                
                imge1 = Image.open(temp_image)
                original_width, original_height = imge1.size

                # Resize only if larger than new size
                if original_width > 800 or original_height > 600:
                    new_size = (800, 600)
                    resized_img = imge1.resize(new_size, Image.LANCZOS)
                else:
                    resized_img = imge1

                image1_gray = ImageOps.grayscale(resized_img)
                image_array = np.array(image1_gray)
                
                U, lam, VT = np.linalg.svd(image_array, full_matrices=False)
                num_sva_keep = determine_svd_keep(compression_r, len(lam))
                
                com_img_array = np.dot(U[:, :num_sva_keep], np.dot(np.diag(lam[:num_sva_keep]), VT[:num_sva_keep, :]))
                comr_img = Image.fromarray(com_img_array.astype(np.uint8))
                reconstructed_image = comr_img.resize((original_width, original_height), Image.LANCZOS)
                colored_img = ImageOps.colorize(reconstructed_image, black=(60, 40, 0), white=(255, 255, 255))
                
                comp_image_filename = 'compressedimage_' + image_file.filename
                comp_image_filepath = os.path.join(app.config['COMPRESSED_FOLDER'], comp_image_filename)
                colored_img.save(comp_image_filepath)
                
                base64_img = encode_image_to_base64(comp_image_filepath)
                base64_img2 = encode_image_to_base64(temp_image)
                compressed_image_size = os.path.getsize(comp_image_filepath)
                
                return render_template('display.html', img=base64_img, filename=comp_image_filename, 
                                       original_size=original_image_size, compressed_size=compressed_image_size, nimag=base64_img2)
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('index.html')
        else:
            flash("No file selected.", "error")
            return render_template('index.html')

    return render_template('index.html')

def determine_svd_keep(compression_r, length):
    if 10 <= compression_r < 30:
        return min(150, length)
    elif 30 <= compression_r < 50:
        return min(128, length)
    elif 50 <= compression_r < 80:
        return min(64, length)
    elif 80 <= compression_r <= 100:
        return min(32, length)
    else:
        return min(32, length)

def encode_image_to_base64(filepath):
    with open(filepath, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

@app.route('/download/<filename>')
def download_compressed_image(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
