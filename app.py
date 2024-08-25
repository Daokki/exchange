from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['GET'])
def convert():
    from_currency = request.args.get('from')
    to_currency = request.args.get('to')
    amount = request.args.get('amount', type=float)

    if not from_currency or not to_currency or amount is None:
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        response = requests.get(f'https://api.exchangerate-api.com/v4/latest/{from_currency}')
        data = response.json()
        rate = data['rates'][to_currency]
        converted_amount = round(amount * rate, 2)
        return jsonify({'converted_amount': converted_amount})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
