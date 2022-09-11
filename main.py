from flask import Flask, render_template, request, redirect, json

from hh_requests import hh_search

app = Flask(__name__, template_folder='templates', static_folder='static')
# app = Flask(__name__)

@app.route("/", methods=['GET'])
def main():
    return render_template('main_page.html')

@app.route("/main_page/", methods=['GET', 'POST'])
def main1():
    return render_template('main_page.html')

@app.route("/contacts/", methods=['GET', 'POST'])
def contacts():
    return render_template('contacts.html')
#

@app.route('/results/')
def results():
    with open('request_result.json', "r", encoding="utf-8") as f:
        data = json.load(f)
    # print(data)
    return render_template('results.html', data=data)


@app.route('/result/')
def result0():
    return redirect("/main_page/")


@app.route('/result/result/')
def result1():
    return redirect("/result/")


@app.route('/result/query_form/', methods=['GET'])
def result2():
    return redirect("/query_form/")


@app.route('/result/main_page/')
def result3():
    return redirect("/main_page/")


@app.route('/query_form/', methods=['POST'])
def query_form_post():
    data = request.form['query_string']
    request_result = hh_search(data)
    print(request_result)
    # return render_template('query_form.html', data=request_result)
    return render_template('result.html', data=request_result)


@app.route('/query_form/', methods=['GET'])
def query_form_get():
    print('GET')
    return render_template('query_form.html')


@app.route('/query_form/result/')
def query_form1():
    return redirect("/result/")

@app.route('/query_form/query_form/')
def query_form2():
    return redirect("/query_form/")

@app.route('/query_form/main_page/')
def query_form3():
    return redirect("/main_page/")


if __name__ == "__main__":
    app.run(debug=True)


