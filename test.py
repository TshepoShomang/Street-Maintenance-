from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
import os
import shutil
from werkzeug.utils import secure_filename
from backend.imageProcessing.validation import is_tar_road
from backend.imageProcessing.pothole_detection import detect_pothole
from backend.calculations.regModel.pothole_model import get_pothole_model
from backend.calculations.pothole_areas import get_pothole_area
from backend.calculations.regModel.full import getRepairPrice
from backend.calculations.road_area import road_length_in_kilometers
from backend.database.getData import userNames, getRole, getPassword, prevUser, getUsername
from backend.database.alterData import updateRole
from backend.calculations.road_area import calculate_distance_in_kilometers
from backend.database.setData import setService, insert

app = Flask(__name__)

CORS(app)  # This will enable CORS for all routes


#Global Variables
roles = ['client', 'worker', 'admin']
users = userNames()

selected_customization = None

email = None
username = None
password = None
role = None


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
def lgoin():
    return render_template('login.html')

@app.route('/Lsubmit', methods=['POST'])
def sub_login():
    global email
    email = request.form.get('email')
    
    global password
    password = request.form.get('password')
    
    global username
    username = getUsername(email)
    
    global roal
    role = getRole(email)
    
    if email in prevUser():
        if getPassword(email) == password:
            return render_template(f'{role}/home.html', email=email, password = password, username = username, role = role)
        else:
            return render_template('login.html', error ="The passwod you entered is incorrect", passw=getPassword(email))
    else:
        return render_template('login.html', error = "The email you have entered does not exist in the application, please use another email or signup")
    

@app.route('/Ssignup', methods=["POST"])
def sub_signup():
    global email
    email = request.form.get('email')
    
    if email in prevUser():
        return render_template('signup.html', error = "This email address already exists in the application please login" )
    
    global username
    username = request.form.get('username')
    
    global password 
    password = request.form.get('password')
    
    global role 
    role = 'client'
    
    insert(email, username, password, role)
    return render_template('client/home.html')
    


@app.route('/quote')
def quote():
    return render_template('client/Quote.html')


@app.route('/customize', methods=['POST'])
def customize():
    global selected_customization
    selected_customization = request.form.get('customization')
    
    
    
    # Optionally, you can log or print the selected customization
    print(f"Selected Customization: {selected_customization}")

    # nothing changes
    return redirect(url_for(upload_file))


# Route to assign a role to a user
@app.route('/assign_role', methods=['POST'])
def assign_role():
    user = request.form.get('user')
    role = request.form.get('role')
    updateRole(role, user)
    

    return '', 204




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
            
            global username
            global password
            global email
            global role
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
            return render_template('client/Quote.html', image_url=front_file_location, array=customization_params, select=selected_customization, price=price, email=email, password=password, username=username, role=role)
                
        else:
            message = """The image does not contain a road, or the image is not clear. 
                        Please Re-take the picture and try again."""
            return render_template('client/quote.html', message=message)
    else:
        return render_template('client/Quote.html', message="File type not allowed"), 400

    
@app.route('/upload/customization/service')
def get_services():
    return render_template('client/service.html')

@app.route('/admin')
def admin_dashboard():
    # In a real application, data would come from the database
    return render_template('admin.html')

# Route to handle role changes
@app.route('/change_role', methods=['POST'])
def change_role():
    worker_id = request.form.get('worker_id')
    new_role = request.form.get('new_role')
    print(f"Changing role of worker {worker_id} to {new_role}")
    # Implement role change logic here
    return redirect(url_for('admin_dashboard'))



if __name__ == '__main__':
    app.run(debug=True)