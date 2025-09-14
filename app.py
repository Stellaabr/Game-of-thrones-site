from flask import Flask, render_template, request, make_response, session
import pandas as pd
import base64
from io import BytesIO
import battle_analysis as ba
import character_analysis as ca

app = Flask(__name__)
app.secret_key = "4d6f45a5fc12445dbac2f59c3b6c7cb1"

#Dataset
battles_df = pd.read_excel('data\\battles.xlsx')
king_stats = ba.analyze_battle_data_numpy(pd.read_excel('data\\battles.xlsx'))
char_df = pd.read_excel('data\\character-deaths.xlsx')

@app.route('/toggle_theme')
def toggle_theme():
    # Переключаем тему между 'light' и 'dark'
    session['theme'] = 'light' if session.get('theme') == 'dark' else 'dark'
    return '', 204

@app.route('/', methods=['GET', 'POST'])
def home():
    slider_value = request.form.get('slider_value', '298') if request.method == 'POST' else '298'

    return render_template('index.html',
                           slider_value=slider_value,
                           battles=ba.choice(slider_value, battles_df),
                           year=slider_value,
                           king_stats=king_stats,
                           theme=session.get('theme', 'dark'))

@app.route("/tables", methods=['POST', 'GET'])
def tables():
    slider_value = request.form.get('slider_value', '1') if request.method == 'POST' else '1'


    if slider_value == '1':
        fig = ca.plot_deaths_by_year(char_df)
    elif slider_value == '2':
        fig = ca.plot_top_allegiances(char_df)
    elif slider_value == '3':
        fig = ca.plot_gender_nobility_death(char_df)
    elif slider_value == '4':
        fig = ca.plot_deaths_by_book_pie(char_df)


    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    plot_url = base64.b64encode(buf.getvalue()).decode('utf-8')

    return render_template('page2.html',
                           plot_url=plot_url,
                           slider_value=slider_value,
                           char_df=char_df,
                           theme=session.get('theme', 'dark'))


@app.route("/export_csv")
def export_csv():
    csv = char_df.to_csv(index=False)


    response = make_response(csv)
    response.headers["Content-Disposition"] = "attachment; filename=characters_deaths.csv"
    response.headers["Content-type"] = "text/csv"

    return response


if __name__ == '__main__':
    app.run(debug=True)
