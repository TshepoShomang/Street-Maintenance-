from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import shutil
from werkzeug.utils import secure_filename
from backend.imageProcessing.validation import is_tar_road
from backend.imageProcessing.pothole_detection import detect_pothole
from backend.database.setData import insert
from backend.database.getData import prevUser, getPassword
from backend.calculations.regModel.pothole_model import get_pothole_model
from backend.calculations.pothole_areas import get_pothole_area
from backend.calculations.regModel.full import getRepairPrice
from backend.calculations.road_area import road_length_in_kilometers
from backend.calculations.road_area import calculate_distance_in_kilometers


app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes


#Global Variables
selected_customization = None
price = None
#End of Global Variables




# Configure upload folder
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENTIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENTIONS



@app.route('/')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/Ssignup', methods=['POST'])
def signHome():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    role = 'client'
    
    if email in prevUser():
        return render_template('login.html', signError = "The email you entered already exists, please login")
    insert(email, username, password)
    return render_template(f'{role}/home.html')

@app.route('/Lsubmit', methods=['POST'])
def Lsubmit():
    email= request.form.get('email')
    password = request.form.get('password')
    
    if email in prevUser():
        if password == getPassword(email):
            return render_template('client/home.html')
        else:
            return render_template('login.html', error = 'You have entered a wrong password, please try again.')
    return render_template('signup.html', error = 'The email does not exist please try signingup')
        

@app.route('/customize', methods=['POST'])
def customize():
    global selected_customization
    selected_customization = request.form.get('customization')
    
    # Optionally, you can log or print the selected customization
    print(f"Selected Customization: {selected_customization}")

    # nothing changes
    return redirect(url_for(upload_file))



#this is the route for uploading / this will take effect after the user uploads the image
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return render_template('client/quote.html', message='This formated is not supported')
    file = request.files['image']
    if file == '':
        return render_template('client/quote.html', message='Please select an image')
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        
        file_data = file.read()
        
        file_location = f'./uploads/{filename}'
        
        try:
            shutil.copy(file_location, './templates/img')
            print("Image successfully copied to ./templates/img")
        except FileNotFoundError:
            print(f"File not found: {file_location}")
        except PermissionError:
            print(f"Permission denied to write to ./templates/img")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        
        if is_tar_road(file_location):  
            front_file_location = f'../uploads/{filename}'
            global price
            price = getRepairPrice(calculate_distance_in_kilometers(file_location),0)
            global selected_customization
            
            
            selected_customization = request.form.get('customization')
            # Map customization to parameters for get_pothole_model
            customization_params = {
                'Cold Asphalt': (0, 0),
                'Hot Asphalt': (1, 0),
                'Infrared Asphalt': (0, 1)
            }

            
            # Check if the selected customization is valid and calculate the price
            if selected_customization in customization_params.keys():
                front_file_location = url_for('static', filename='img/' + filename)
                model_params = customization_params[selected_customization]
                price = 0
                price = sum(get_pothole_model(area, *model_params) for area in get_pothole_area(file_location))
                price = round(price, 2)

                return render_template('client/Quote.html', image_url=front_file_location, price=price, select=selected_customization)
            return render_template('client/Quote.html', image_url=front_file_location, array=customization_params, select=selected_customization, price=price)
                
        else:
            message = """The image does not contain a road, or the image is not clear. 
                        Please Re-take the picture and try again."""
            return render_template('client/quote.html', message=message)
    else:
        return render_template('client/Quote.html', message="File type not allowed"), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)