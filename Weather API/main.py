from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv("data_small/stations.txt", skiprows=17)
stations = stations[["STAID", "STANAME                                 "]]


@app.route("/")
def home():
    return render_template("home.html", data=stations.to_html())


@app.route("/api/v1/<station>/<date>")
def about(station, date):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename,
                     skiprows=20,
                     parse_dates=["    DATE"])
    temp = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {
        "station ": station,
        "date": date,
        "temperature": temp
    }


@app.route("/api/v1/<station>")
def by_stat(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    stat = pd.read_csv(filename,
                       skiprows=20,
                       parse_dates=["    DATE"])
    stat = stat[["STAID", "    DATE", "   TG"]]

    return render_template("about.html", data=stat.to_html())
    # result = stat.to_dict(orient="records")
    # return result


@app.route("/api/v1/yearly/<station>/<year>")
def by_stat_year(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    stat = pd.read_csv(filename,
                       skiprows=20)
    stat['    DATE']= stat['    DATE'].astype(str)
    stat_year = stat[stat['    DATE'].str.startswith(str(year))]
    return render_template("about.html", data=stat_year.to_html())


if __name__ == "__main__":
    app.run(debug=True, port=5002)
