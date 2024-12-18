# Street-Maintenance


## Table of Contents
- Overview 
- Features 
- Installation 
- Screenshots 
- Dependencies 
- Contact


## Overview
The application enables users to upload a photo of the road, which is then analyzed to determine and display the estimated maintenance cost.
### Purpose of the project
The aim of this project is to simplify the process of requesting and managing maintenance work while enhancing transparency and efficiency. By allowing users to easily submit aerial pictures of areas in need of attention, the app streamlines the initial assessment process. Leveraging advanced artificial intelligence algorithms, the app accurately calculates pricing for maintenance tasks, considering various factors like labor costs, transportation expenses, and required materials. This feature ensures that users receive cost estimations, fostering transparency and informed decision-making


## Features
1.	Aerial Picture Submission: Clients can easily upload aerial pictures of the site requiring maintenance directly through the app, providing clear visuals for assessment.
2.	AI-Powered Pricing Calculation: The heart of the app will be its artificial intelligence algorithm, which will analyze the submitted pictures and calculate the pricing for the maintenance work. The algorithm will take into account labor costs, transportation expenses (including gas prices), material costs, and equipment servicing fees.
3.	Real-Time Cost Estimation: Clients will receive instant cost estimations upon submitting the pictures, allowing for transparency and efficient decision-making.
4.	Customizable Services: The app will offer customizable options for clients to specify the type and scope of maintenance required, ensuring flexibility and tailored solutions.
5.	Predictive Maintenance: Utilizing machine learning algorithms, the app can predict potential maintenance needs based on historical data, allowing clients to schedule proactive maintenance and avoid costly repairs in the future.
6.	Route Optimization: For companies dispatching maintenance crews, the app will incorporate route optimization algorithms to minimize travel time and fuel consumption, enhancing operational efficiency.
7.	Scheduling and Reminders: Clients can schedule maintenance appointments through the app and receive reminders, ensuring timely service delivery and enhancing customer satisfaction.


## Installation 

### Prerequisites
To be able to download the required packages, you need to have python version 3.12.3 and above installed on your machine. 
#### To see which version of python you are currently running, use the following comment:
```bash
python --version
```

Before running the application there are a number of packages which should be installed. They reside inside a the requirements.txt file. 

#### To install all packages used, the the command:
```bash
pip install -r requirements.txt

```

## Dependencies 
### Here is a list of all packages used in developing the application
- blinker^1.9.0
- click^8.1.7
- colorama^0.4.6
- Flask^3.1.0
- Flask-Cors^5.0.0
- imageio^2.36.1
- itsdangerous^2.2.0
- Jinja2^3.1.4
- joblib^1.4.2
- lazy_loader^0.4
- MarkupSafe^3.0.2
- networkx^3.4.2
- numpy^2.2.0
- opencv-python^4.10.0.84
- packaging^24.2
- pandas^2.2.3
- pillow^11.0.0
- python-dateutil^2.9.0.post0
- pytz^2024.2
- scikit-image^0.24.0
- scikit-learn^1.6.0
- scipy^1.14.1
- six^1.17.0
- threadpoolctl^3.5.0
- tifffile^2024.9.20
- tzdata^2024.2
- Werkzeug^3.1.3