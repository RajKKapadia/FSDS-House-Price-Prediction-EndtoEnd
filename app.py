from flask import Flask

app = Flask(import_name='__main__')

@app.route('/')
def home():
    return 'Machine learning project.'

if __name__ == '__main__':
    app.run(
        debug=True
    )