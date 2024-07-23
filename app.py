
#importing necessary libraries
import numpy as np
from PIL import Image,ImageOps
import os,base64
from io import BytesIO #you can use BytedIO also 
from flask import Flask,request,render_template,flash,send_from_directory
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['COMPRESSED_FOLDER'] = 'static/compressed_image'
app.config['SECRET_KEY'] = 'your_secret_key_here'
#if the folder is not there create it
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
#getting the Route
@app.route('/', methods=['GET','POST'])
def compress_image():
    #checking Post method
    if request.method=='POST':
        image_file = request.files['image']
        compression_r= int(request.form['cr'])
        #checking a filename which is not a null
        if image_file.filename !='':
            try:
                temp_image = os.path.join('static/uploads',image_file.filename)
                image_file.save(temp_image)#saving the image in the directory
                original_image_size = os.path.getsize(temp_image)#getting the size of an original image
                imge1 = Image.open(temp_image)
                original_width, original_height = imge1.size
                '''max_size = (800, 600)  # Set maximum dimensions
                imge1.thumbnail(max_size, Image.ANTIALIAS)'''
                new_size = (800, 600)#setting new size
                resized_img = imge1.resize(new_size, Image.LANCZOS)#resizing the image
                resized_img.save('resized_image.jpg')#save it
                image1_gray = ImageOps.grayscale(resized_img)#converting to Grayscale
                image_array = np.array(image1_gray)#getting the matrix of the image
                U,lam,VT = np.linalg.svd(image_array)#performing Single Value Decomposition
                if (compression_r>=10)and(compression_r<30):
                    num_sva_keep = 150
                elif (compression_r>=30) and (compression_r<50):
                    num_sva_keep = 128
                elif (compression_r>=50) and (compression_r<80):
                    num_sva_keep = 64
                elif (compression_r>=80) and (compression_r<=100):
                    num_sva_keep = 32 #calculating the number of lambda values needed using compression rate given
                
                com_img_array = np.dot(U[:,:num_sva_keep],np.dot(np.diag(lam[:num_sva_keep]),VT[:num_sva_keep,:]))#reconstructing the image 
                comr_img = Image.fromarray(com_img_array.astype(np.uint8))#forming the image using reconstructed matrix
                reconstructed_image = comr_img.resize((original_width, original_height), Image.LANCZOS)
                colored_img = ImageOps.colorize(reconstructed_image, black=(60, 40, 0), white=(255, 255, 255))#colorizing it
                #adding a new path to the compressed file
                comp_image_filename = 'compressedimage'+image_file.filename
                comp_image_filepath = os.path.join('static/compressed_image',comp_image_filename)
                colored_img.save(comp_image_filepath)
                with open(comp_image_filepath,'rb') as img_file:#converting the colorized compressed image to base64 for displaying
                    base64_img = base64.b64encode(img_file.read()).decode('utf-8')
                with open('static/uploads/'+image_file.filename,'rb') as im_file:
                    base64_img2 = base64.b64encode(im_file.read()).decode('utf-8')  
                compressed_image_size = os.path.getsize('static/compressed_image/'+comp_image_filename)
                ''''img_buffer = BytesIO()
                comr_img.save(img_buffer, format='JPEG')
                img_buffer.seek(0)'''
                #rendering the template from display.html
                return render_template('display.html', img=base64_img, filename=comp_image_filename,original_size=original_image_size, compressed_size=compressed_image_size,nimag=base64_img2)
            except Exception as e:
                flash(f"An error occurred: {str(e)}", "error")
                return render_template('index.html')
        else:
            flash("No file selected.", "error")
            return render_template('index.html')

    # rendering the template form index.html
    return render_template('index.html')
@app.route('/download/<filename>')
def download_compressed_image(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'],filename,as_attachment = True)

if __name__=='__main__':
    app.run(debug=True)
