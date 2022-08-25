import requests
from flask import Flask, request, render_template

NB_USERS = 322896
selected_id = 0
REC_TYPE = ['Content-Based', 'Collaborative Filtering']
REC_TYPE_API = {'Content-Based': 'cb', 'Collaborative Filtering': 'cf'}
selected_type = REC_TYPE[0]

app = Flask(__name__)

# Endpoint
@app.route('/', methods=["GET","POST"])
def index():

    global selected_id
    if request.form.get('user'):
        selected_id = int(request.form.get('user'))

    selected_id = selected_id if selected_id <= NB_USERS else NB_USERS
    selected_id = selected_id if selected_id >= 0 else 0

    global selected_type
    if request.form.get('rec'):
        selected_type = str(request.form.get('rec'))

    return render_template('index.html', sended=False, rec_type=REC_TYPE, selected_id=selected_id, selected_type=selected_type)

# Endpoint pour recommander les articles du user sélectionné
@app.route('/recommend/', methods=["GET","POST"])
def recommendArticles():

    params = {"id": selected_id, "type": REC_TYPE_API[selected_type]}

    # Appel vers Azure function pour la recommandation d'articles
    r = requests.get('https://ocp9-function.azurewebsites.net/api/recommend-article', json=params, verify=True)

    content = r.content.decode("utf-8")

    remove ='[ ]'
    for charac in remove:
        content = content.replace(charac, '')

    content = content.split(',')

    return render_template('index.html', sended=True, rec_type=REC_TYPE, selected_id=selected_id, selected_type=selected_type, result=content)

if __name__ == "__main__":
    app.run()