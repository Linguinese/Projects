from flask import Flask, render_template, request, redirect, url_for
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    provider = None
    if request.method == 'POST':
        last_name = request.form['last_name']
        provider = find_provider(last_name)
    return render_template('index.html', provider=provider)

@app.route('/add_provider', methods=['GET', 'POST'])
def add_provider_view():
    message = None
    if request.method == 'POST':
        provider_data = {
            'Referring Last': request.form['ref_last'],
            'Referring First': request.form['ref_first'],
            'Referring MI': request.form['ref_mi'],
            'Referring Title': request.form['ref_title'],
            'Referring Address': request.form['ref_address'],
            'Referring City': request.form['ref_city'],
            'Referring State': request.form['ref_state'],
            'Referring Zip': request.form['ref_zip'],
            'Referring Clinic': request.form['ref_clinic'],
            'Referring Phone': request.form['ref_phone'],
            'Referring Fax No': request.form['ref_fax']
        }
        message = add_provider(provider_data)
        # Optionally redirect to the find provider page after adding
        return redirect(url_for('index'))
    return render_template('add_provider.html', message=message)

def find_provider(last_name):
    try:
        df = pd.read_csv('Referring Physicians Updated.csv', delimiter=';')
        provider = df[df['Referring Last'].str.lower() == last_name.lower()]
        return provider if not provider.empty else None
    except Exception as e:
        return None

def add_provider(provider_data):
    try:
        df = pd.read_csv('Referring Physicians Updated.csv', delimiter=';')
        new_provider_df = pd.DataFrame([provider_data])
        updated_df = pd.concat([df, new_provider_df], ignore_index=True)
        updated_df.to_csv('Referring Physicians Updated.csv', index=False, sep=';')
        return "Provider added successfully."
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
