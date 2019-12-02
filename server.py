from rsa_crack import rsa_decrypt
from rsa_keygen import rsa_encrypt

from flask import Flask, request, jsonify, render_template, redirect, url_for
from json import dumps
from flask_wtf import Form
from wtforms import TextField

from utils import gcd, serialize, deserialize

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def encrypt_v1():
    err = ""
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
            # print("Content: {} with pkey:{}\n".format(code, key))
            code = serialize(code)
            # print("Content: {} with pkey:{}\n".format(code, key))
            return redirect(url_for('.decrypt_v1', key1=key[0], key2=key[1], encrypted=code))
        except Exception as error:
            print(error)
            err = error
    return render_template('encrypt.html', message=err)


@app.route('/decrypt_v1', methods=['GET', 'POST'])
def decrypt_v1():
    err = ""
    if request.method == 'POST':
        try:
            req = request.form
            print('REQUEST: {}'.format(req))
            key1 = req['key1']
            key2 = req['key2']
            key = [int(key1), int(key2)]
            data = req['data']
            data = deserialize(data)
            # print('Data: {} - key: {}'.format(data, key))
            message, key = rsa_decrypt(key, data)
            print('Data: {} - key: {}'.format(message, key))
            return render_template('result.html', decrypted=message, private=key)
        except Exception as error:
            print(error)
            err = error
            return render_template('decrypt.html', message=err)
    elif request.method == 'GET':
        try:
            req = request.args
            # print('REQUEST: {}'.format(req))
            message = req.get('encrypted')
            key1 = req.get('key1')
            key2 = req.get('key2')
            # print('Render HERE')
            return render_template('decrypt.html', data=message, key1=key1, key2=key2)
        except Exception as error:
            print(error)
            err = error
            return render_template('decrypt.html', message=err)


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
