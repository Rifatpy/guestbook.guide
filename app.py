from flask import Flask, render_template, request, redirect, url_for, session
import json
import schedule
import time
import requests

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'jhu$845hkjd9834g78kjdfoieu5y498ksdbffaisudry98843y5dkadf'

# Replace these values with your actual credentials
CLIENT_ID = "1000.WKQ8NPGW95ZI5W9EABQOVEXXT78B1Q"
CLIENT_SECRET = "c6c815ab7974494acb003856a6899488050584f3b7"
REFRESH_TOKEN = "1000.305b46e4209543ce7202567f685e847d.989ca84ecd257ed0c95475eef2cd69bc"
GRANT_TYPE = "refresh_token"

ACCESS_TOKEN = None

def generate_access_token():
    global ACCESS_TOKEN
    
    # API endpoint to get access token
    token_url = "https://accounts.zoho.eu/oauth/v2/token"

    # API call to generate access token
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": GRANT_TYPE
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        ACCESS_TOKEN = response.json().get("access_token")
        print(f"Access token generated: {ACCESS_TOKEN}")
        return ACCESS_TOKEN
    else:
        print(f"Failed to generate access token. Status Code: {response.status_code}")

# Schedule the function to run every 55 minutes
schedule.every(55).minutes.do(generate_access_token)

# Run the scheduled jobs in a separate thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to get all modules data using the access token
def get_all_modules_data(ACCESS_TOKEN):
    headers = {
        'Authorization': f'Zoho-oauthtoken {ACCESS_TOKEN}'
    }

    response = requests.get('https://www.zohoapis.eu/crm/v2/Guestbook?fields=Email,Guest_Phone,Guest_Check_IN,Guest_Check_OUT,Guest_Email,Guest_Property_Name,Guest_First_Name,Name', headers=headers)
    data = response.json()

    return data


@app.route('/', methods=['GET', 'POST'])
def login():
    # Generate or refresh access token
    """ACCESS_TOKEN = generate_access_token()
    
    # Get all modules data using the access token
    all_data = get_all_modules_data(ACCESS_TOKEN)
    
    # Write the data to the JSON file
    JSON_FILE_PATH = 'response.json'
    with open(JSON_FILE_PATH, 'w') as json_file:
        json.dump(all_data, json_file, indent=4)"""
    
    # Load the JSON data
    with open('response.json') as f:
        all_guest_data = json.load(f)
    
    guest_data = {}  # Initialize guest_data
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        if phone_number:
            # Cleaning the phone number
            cleaned_phone_number = ''.join(filter(str.isdigit, phone_number))[-10:]
    
            all_guest_data = all_guest_data.get("data", [])
            for entry in all_guest_data:
                phone = ''.join(filter(str.isdigit, entry.get('Guest_Phone', '')))[-10:]
    
                if cleaned_phone_number == phone:
                    guest_data = {
                        'Guest_Phone': entry.get('Guest_Phone', None),
                        'Guest_First_Name': entry['Guest_First_Name'],
                        'Guest_Last_Name': entry['Name'],
                        'Guest_Email': entry['Guest_Email'],
                        'Guest_Check_IN': entry['Guest_Check_IN'],
                        'Guest_Check_OUT': entry['Guest_Check_OUT'],
                        'Guest_Property_Name': entry['Guest_Property_Name']
                    }
                    
                    if guest_data['Guest_Property_Name'] == "Highlands":
                        input_number = cleaned_phone_number
                        return redirect(url_for('highland_property', number=input_number))
                    elif guest_data['Guest_Property_Name'] == "Casa al Lago":
                        input_number = cleaned_phone_number
                        return redirect(url_for('casa_al_lago_property', number=input_number))
                    elif guest_data['Guest_Property_Name'] == "Depero":
                        input_number = cleaned_phone_number
                        return redirect(url_for('depero_property', number=input_number))
                    elif guest_data['Guest_Property_Name'] == "Casa Mao":
                        input_number = cleaned_phone_number
                        return redirect(url_for('casa_mao_property', number=input_number))
                    else:
                        return render_template('login.html', error='Invalid phone number. Please try again.')
    
            return render_template('login.html', error='Invalid phone number. Please try again.')
    
    return render_template('login.html')

# Flask route to handle the property page
@app.route('/property/highlands_property/<number>')
def highland_property(number):
  property_name="Highlands"
  # Load the JSON data
  with open('response.json') as f:
      all_guest_data = json.load(f)
  all_guest_data = all_guest_data.get("data", [])
  for entry in all_guest_data:
      phone = ''.join(filter(str.isdigit, entry.get('Guest_Phone', '')))[-10:]

      if number == phone:
          guest_data = {
              'Guest_Phone': entry['Guest_Phone'],
              'Guest_First_Name': entry['Guest_First_Name'],
              'Guest_Last_Name': entry['Name'],
              'Guest_Email': entry['Guest_Email'],
              'Guest_Check_IN': entry['Guest_Check_IN'],
              'Guest_Check_OUT': entry['Guest_Check_OUT'],
              'Guest_Property_Name': entry['Guest_Property_Name']
          }
          try:
            return render_template('highlands_property.html', property_name=property_name, guest_data=guest_data)
          except:
            return render_template('property_not_found.html', property_name=property_name)  

# Flask route to handle the property page
@app.route('/property/casa_al_lago_property/<number>')
def casa_al_lago_property(number):
  property_name="Casa al Lago"
  
  # Load the JSON data
  with open('response.json') as f:
      all_guest_data = json.load(f)
  all_guest_data = all_guest_data.get("data", [])
  for entry in all_guest_data:
      phone = ''.join(filter(str.isdigit, entry.get('Guest_Phone', '')))[-10:]

      if number == phone:
          guest_data = {
              'Guest_Phone': entry['Guest_Phone'],
              'Guest_First_Name': entry['Guest_First_Name'],
              'Guest_Last_Name': entry['Name'],
              'Guest_Email': entry['Guest_Email'],
              'Guest_Check_IN': entry['Guest_Check_IN'],
              'Guest_Check_OUT': entry['Guest_Check_OUT'],
              'Guest_Property_Name': entry['Guest_Property_Name']
          }
  
          return render_template('casa_al_lago_property.html', property_name=property_name, guest_data=guest_data)

# Flask route to handle the property page
@app.route('/property/depero_property/<number>')
def depero_property(number):
  property_name="Depero"

  # Load the JSON data
  with open('response.json') as f:
      all_guest_data = json.load(f)
  all_guest_data = all_guest_data.get("data", [])
  for entry in all_guest_data:
      phone = ''.join(filter(str.isdigit, entry.get('Guest_Phone', '')))[-10:]

      if number == phone:
          guest_data = {
              'Guest_Phone': entry['Guest_Phone'],
              'Guest_First_Name': entry['Guest_First_Name'],
              'Guest_Last_Name': entry['Name'],
              'Guest_Email': entry['Guest_Email'],
              'Guest_Check_IN': entry['Guest_Check_IN'],
              'Guest_Check_OUT': entry['Guest_Check_OUT'],
              'Guest_Property_Name': entry['Guest_Property_Name']
          }
  
          return render_template('depero_property.html', property_name=property_name, guest_data=guest_data)

# Flask route to handle the property page
@app.route('/property/casa_mao_property/<number>')
def casa_mao_property(number):
  property_name="Casa Mao"

  # Load the JSON data
  with open('response.json') as f:
      all_guest_data = json.load(f)
  all_guest_data = all_guest_data.get("data", [])
  for entry in all_guest_data:
      phone = ''.join(filter(str.isdigit, entry.get('Guest_Phone', '')))[-10:]

      if number == phone:
          guest_data = {
              'Guest_Phone': entry['Guest_Phone'],
              'Guest_First_Name': entry['Guest_First_Name'],
              'Guest_Last_Name': entry['Name'],
              'Guest_Email': entry['Guest_Email'],
              'Guest_Check_IN': entry['Guest_Check_IN'],
              'Guest_Check_OUT': entry['Guest_Check_OUT'],
              'Guest_Property_Name': entry['Guest_Property_Name']
          }

          return render_template('casa_mao_property.html', property_name=property_name, guest_data=guest_data)

if __name__ == "__main__":
  # Start the scheduler in a separate thread
  import threading
  scheduler_thread = threading.Thread(target=run_scheduler)
  scheduler_thread.start()
  app.run(host='0.0.0.0', debug=True)
