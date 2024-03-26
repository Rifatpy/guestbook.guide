from flask import Flask, render_template, request, redirect, url_for, session
from jinja2.exceptions import TemplateNotFound
import json
import schedule
import time
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
  if request.method == 'POST':
    phone_number = request.form['phone_number']
    property_name = 'Highlands_Property'
    return redirect(url_for('highland_property', property_name=property_name))
  return render_template('login.html')

# Flask route to handle the property page
@app.route('/property/<property_name>')
def highland_property(property_name):
  guest_data = {
      "Guest_Property_Name": "Casa al Lago",
      "Guest_First_Name": "Stella",
      "Guest_Last_Name": "Griffin",
      "Guest_Check_OUT": "25-03-2024",
      "Guest_Email": "stellagriffin@gmail.com",
      "Guest_Check_IN": "20-03-2024",
      "id": "628735000000404650",
      "Guest_Phone": "555-9012-3456",
      "Name": "Griffin"
  }
  return render_template('highlands_property.html', property_name=property_name, guest_data=guest_data, entry_data=guest_data)
  

if __name__ == "__main__":
  app.run(host='0.0.0.0', debug=True)
