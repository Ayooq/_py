from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify

from api import token, home
import funcs as f


app = Flask(__name__)
sslify = SSLify(app)


@app.route('/' + token, methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        response = request.get_json()
        try:
            chat_id = response['message']['chat']['id']
            message = response['message']['text']
        except KeyError:
            chat_id = response['edited_message']['chat']['id']
            message = response['edited_message']['text']
        finally:
            currency = f.parse_text(message)
            f.send_message(
                chat_id, f.get_price(currency)
            ) if currency else f.send_message(chat_id)
            return jsonify(response)
    else:
        return '<h1>Hello, world!</h1>'


if __name__ == '__main__':
    # f.set_webhook(home + token)
    # f.delete_webhook(home + token)
    app.run()
