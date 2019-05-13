from flask import Flask, render_template, request,redirect, url_for
import pickle

import nltk
import re
#nltk.download('stopwords');
#nltk.download('punkt');
import spacy
nlp = spacy.load('en_core_web_sm');

KW_dict = pickle.load(open("Keyword.pkl", "rb"))
Topic_dict = pickle.load(open("Topic.pkl", "rb"))

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['the','i','you','a','c','slu','them','she','he','company'])
stopwords.extend(KW_dict.keys())

def get_recommendation(user_prf, KW_dict):
    def stopword_RMV(sent):
        res = []
        for word in sent.split():
            if word.lower() not in stopwords:
                res.append(word)
        return ' '.join(res)

    doc0 = nlp(stopword_RMV(user_prf))
    score_dict = {}
    for k, v in KW_dict.items():
        temp_doc = nlp(v)
        score_dict[k] = doc0.similarity(temp_doc)

    sorted_score = sorted(score_dict.items(), key=lambda kv: kv[1], reverse=True)

    rcm_company = []
    for i in range(5):
        rcm_company.append('#' + str(i + 1) + ': ' + str(sorted_score[i][0]))

    return rcm_company

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        target_company = request.form['target_company']
        company = target_company
        return render_template('graph.html', company=company)
    if request.method == 'GET':
        user_input = request.args.get('user_input')
        return rcm(user_input)
        #return redirect(url_for('rcm', sent = user_input))
    return render_template('login.html')

@app.route('/graph')
def graph():

    return render_template('graph.html')

@app.route('/rcm')
def rcm(sent,KW_dict = KW_dict):
    #print(KW_dict['google'])
    rcm_company=get_recommendation(user_prf=sent, KW_dict=KW_dict)
    c0 = rcm_company[0].split(':')[-1]
    c1 = rcm_company[1].split(':')[-1]
    c2 = rcm_company[2].split(':')[-1]
    c3 = rcm_company[3].split(':')[-1]
    c4 = rcm_company[4].split(':')[-1]
    return render_template('rcm.html',sent=sent,c0=c0,c1=c1,c2=c2,c3=c3,c4=c4)


if __name__ == '__main__':
    app.run(debug=True)