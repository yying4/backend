#encoding：utf-8
from flask import Flask,request
from flask_cors import CORS, cross_origin
config = {
  'ORIGINS': [
    'http://localhost:8080',  # React
    'http://127.0.0.1:8080',  # React
  ],

  'SECRET_KEY': '...'
}
app = Flask(__name__)
#CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)# cors = CORS(app)

CORS(app, supports_credentials=True)
#resources={ r'/*': {'origins': config['ORIGINS']}},
@app.route('/')
def hi():
    return 'hi~'

@app.route('/output/',methods=['GET'])
def output():
    request.args.get("key")
    id = request.get_data(as_text=True)
    return id

@app.route('/login/',methods=['POST'])
def login():
    if request.method == 'POST':
        web=request.values.get('website')
        #web='success'
    #web=request.form.get('website')
    return web

if __name__=='__main__':
    app.run(port=5000,host='127.0.0.1',debug=True)


# website = request.get_data(as_text=True)
