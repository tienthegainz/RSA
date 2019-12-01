from rsa_crack import rsa_decrypt
from rsa_keygen import rsa_encrypt

from flask import Flask, request, jsonify
from json import dumps

from utils import gcd

app = Flask(__name__)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    if request.method == 'POST':
        try:
            req = request.form
            data = req['data']
            if 'e' in req and 'n' in req:
                e = int(req['e'])
                n = int(req['n'])

                key, code = rsa_encrypt(data, e=e, n=n)
            elif 'q' in req and 'p' in req:
                q = int(req['q'])
                p = int(req['p'])
                key, code = rsa_encrypt(data, p=p, q=q)
            else:
                key, code = rsa_encrypt(data)
            return jsonify({'success': True, 'public': key, 'encrypted': code})
        except Exception as err:
            print(err)
            return jsonify({'success': False, 'error': err})
    else:
        return jsonify({'success': False})


@app.route('/decrypt', methods=['POST'])
def decrypt():
    if request.method == 'POST':
        try:
            req = request.get_json()
            key = req['public']
            data = req['encrypted']
            key = list(key)
            data = list(data)
            # print((key), '---', (data))
            # print(type(key), '---', type(data))

            message, key = rsa_decrypt(key, data)
            return jsonify({'success': True, 'decrypted': message, 'private': key})
        except Exception as err:
            print(err)
            return jsonify({'success': False, 'error': err})
    else:
        return jsonify({'success': False})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
