from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)


# Fetch all available currencies
def fetch_currencies():
    url = "https://open.er-api.com/v6/latest/USD"  # Base currency can be changed if needed
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {code.upper(): code for code in data['rates']}  # Returns uppercase codes
    else:
        return {}


def get_exchange_rate(base_currency_code, target_currency_code):
    url = f"https://open.er-api.com/v6/latest/{base_currency_code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rates = data['rates']
        if target_currency_code in rates:
            return rates[target_currency_code]
        else:
            return None
    else:
        return None


@app.route('/', methods=['GET', 'POST'])
def index():
    converted_amount = None
    currencies = fetch_currencies()  # Fetch currencies dynamically
    amount = None
    base_currency = None
    target_currency = None

    if request.method == 'POST':
        amount = request.form['amount']
        base_currency = request.form['base_currency']
        target_currency = request.form['target_currency']
        rate = get_exchange_rate(base_currency, target_currency)
        if rate:
            converted_amount = round(float(amount) * rate, 2)  # Round to 2 decimal places

    # HTML and CSS
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Currency Converter</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                transition: background-color 0.3s, color 0.3s;
            }
            .container {
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                width: 300px;
                transition: background 0.3s, box-shadow 0.3s;
            }
            h1 {
                margin-bottom: 20px;
            }
            form {
                display: flex;
                flex-direction: column;
            }
            input[type="number"] {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            select {
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 4px;
            }
            button {
                padding: 10px;
                background-color: #28a745;
                color: #fff;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            button:hover {
                background-color: #218838;
            }
            .dark-mode {
                background-color: #333;
                color: #fff;
            }
            .dark-mode .container {
                background: #444;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
            }
            .toggle-icon {
                cursor: pointer;
                margin-bottom: 10px;
            }
        </style>
        <script>
            function toggleMode() {
                document.body.classList.toggle('dark-mode');
            }
        </script>
    </head>
    <body>
        <div class="container">
            <h1>Sabi Rate</h1>
            <span class="toggle-icon" onclick="toggleMode()">🌓</span>
            <form method="POST">
                <input type="number" name="amount" placeholder="Amount" value="{{ amount }}" required>

                <select name="base_currency" required>
                    {% for code in currencies.keys() %}
                        <option value="{{ code }}" {% if base_currency == code %}selected{% endif %}>{{ code }}</option>
                    {% endfor %}
                </select>
                <select name="target_currency" required>
                    {% for code in currencies.keys() %}
                        <option value="{{ code }}" {% if target_currency == code %}selected{% endif %}>{{ code }}</option>
                    {% endfor %}
                </select>
                <button type="submit">Convert</button>
            </form>

            {% if converted_amount is not none %}
                <h4>Amount: {{ converted_amount }}</h4>
            {% endif %}
        </div>
    </body>
    </html>
    '''

    return render_template_string(html_content, converted_amount=converted_amount, currencies=currencies, amount=amount,
                                  base_currency=base_currency, target_currency=target_currency)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

