import os

from flask import Flask, abort, send_from_directory
from jinja2.exceptions import TemplateNotFound
import csv
from flaskr.charts import Charts

def read_data(app):
    data_file = os.path.join(app.root_path, 'data', 'cardio_train.csv')
  
    with open(data_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        headers = next(reader)  # Read the first row as headers

        charts = Charts()
        for row in reader:
            datapoint = {}
            for i, header in enumerate(headers):
                datapoint[header] = row[i]
            charts.aggregate(datapoint)

        charts.plot()
        return charts        

def create_app():
    app = Flask(__name__)
    charts = read_data(app)

    @app.route('/charts/')
    def get_chart_list():
        return list(charts.names())
    
    @app.route('/charts/<name>')
    def get_chart(name):
        plot_config = charts.get(name)
        if plot_config is None:
            abort(404)
        return plot_config

    @app.route('/')
    @app.route('/<path>.html')
    def pages(path=None):
        if path is None:
            path = "index"
        try:
            return send_from_directory('pages', path + ".html")
        except TemplateNotFound:
            abort(404)
    return app