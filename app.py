from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Variable to hold the uploaded data temporarily
uploaded_data = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global uploaded_data
    total_value = None
    car_number_plates = []
    selected_plate = None

    if request.method == 'POST':
        # If the clear button is pressed, reset everything
        if 'clear' in request.form:
            uploaded_data = None
            session['file_uploaded'] = False  # Reset the file upload status
            return redirect(url_for('index'))

        # If a file is uploaded, store the data and extract car plates
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename.endswith('.xlsx'):
                try:
                    uploaded_data = pd.read_excel(file)
                    car_number_plates = uploaded_data.iloc[:, 2].unique().tolist()  # Unique plates from column C
                    session['file_uploaded'] = True  # Set file upload status to True
                except Exception as e:
                    return render_template('index.html', error=str(e))

        # If the calculate button is clicked and a plate is selected
        elif 'calculate' in request.form and uploaded_data is not None:
            selected_plate = request.form.get('car_plate')
            if selected_plate:
                # Filter for selected plate and calculate the total transaction value
                selected_data = uploaded_data[uploaded_data.iloc[:, 2] == selected_plate]
                total_value = selected_data.iloc[:, 9].sum()
                car_number_plates = uploaded_data.iloc[:, 2].unique().tolist()  # Reload the dropdown options

    return render_template('index.html', car_number_plates=car_number_plates, total_value=total_value, selected_plate=selected_plate)

if __name__ == '__main__':
    app.run(debug=True)