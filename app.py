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
def home():
  # Generate or refresh access token
  ACCESS_TOKEN = generate_access_token()

  # Get all modules data using the access token
  all_data = get_all_modules_data(ACCESS_TOKEN)

  # Write the data to the JSON file
  JSON_FILE_PATH = 'response.json'
  with open(JSON_FILE_PATH, 'w') as json_file:
      json.dump(all_data, json_file, indent=4)

  # Load the JSON data
  with open(JSON_FILE_PATH) as f:
      all_guest_data = json.load(f)

  guest_data = {}  # Initialize guest_data
  if request.method == 'POST':
      phone_number = request.form['phone_number']
      # Removing (-) from the number
      try:
          phone_number = phone_number.replace("-", "")
      except:
          pass
      # Revoming (+) sign from the number if there is
      try:
          phone_number = phone_number.replace("+", "")
      except:
          pass

      try:
          phone_number = phone_number[-10:]
      except:
          pass

      all_guest_data = all_guest_data["data"]
      for entry in all_guest_data:
          phone = entry['Guest_Phone']
          # Removing (-) from the number
          try:
              phone = phone.replace("-", "")
          except:
              pass
          # Revoming (+) sign from the number if there is
          try:
              phone = phone.replace("+", "")
          except:
              pass

          # Taking last 10 digits
          try:
              phone = phone[-10:]
          except:
              pass

          if phone_number == phone:
              guest_data = {
                  'Guest_Phone': phone,
                  'Guest_First_Name': entry['Guest_First_Name'],
                  'Guest_Last_Name': entry['Name'],
                  'Guest_Email': entry['Guest_Email'],
                  'Guest_Check_IN': entry['Guest_Check_IN'],
                  'Guest_Check_OUT': entry['Guest_Check_OUT'],
                  'Guest_Property_Name': entry['Guest_Property_Name']
              }
              if guest_data['Guest_Property_Name'] == "Highlands":
                session['guest_data'] = guest_data  # Store guest data in session
                session['entry_data'] = entry  # Store entry data in session
                return redirect(url_for('highland_property', guest_data=guest_data))
              elif guest_data['Guest_Property_Name'] == "Casa al Lago":
                session['guest_data'] = guest_data  # Store guest data in session
                session['entry_data'] = entry  # Store entry data in session
                return redirect(url_for('casa_al_lago_property', guest_data=guest_data))
              elif guest_data['Guest_Property_Name'] == "Depero":
                session['guest_data'] = guest_data  # Store guest data in session
                session['entry_data'] = entry  # Store entry data in session
                return redirect(url_for('depero_property', guest_data=guest_data))
              else:
                pass
          else:
              return render_template('login-page.html', error='Invalid phone number. Please try again.')

# Flask route to handle the property page
@app.route('/property/highlands_property')
def highland_property(guest_data):
  property_name="highlands"
  
  # Retrieve guest data and entry data from session
  guest_data = session.get('guest_data', {})
  entry_data = session.get('entry_data', None)

  try:
    return render_template('highlands_property.html', property_name=property_name, guest_data=guest_data, entry_data=guest_data)
  except TemplateNotFound:
    return render_template('property_not_found.html', property_name=property_name)
  
  

# Flask route to handle the property page
@app.route('/property/casa_al_lago_property')
def casa_al_lago_property(guest_data):
  property_name="Casa al Lago"
  
  # Retrieve guest data and entry data from session
  guest_data = session.get('guest_data', {})
  entry_data = session.get('entry_data', None)
  
  return render_template('casa_al_lago_property.html', property_name=property_name, guest_data=guest_data, entry_data=guest_data)

# Flask route to handle the property page
@app.route('/property/casa_al_lago_property')
def depero_property(guest_data):
  property_name="Depero"

  # Retrieve guest data and entry data from session
  guest_data = session.get('guest_data', {})
  entry_data = session.get('entry_data', None)
  
  return render_template('casa_al_lago_property.html', property_name=property_name, guest_data=guest_data, entry_data=guest_data)

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
