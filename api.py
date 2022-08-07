import flask
from flask import request, jsonify
import pandas
import numpy

app = flask.Flask(__name__)
app.config["DEBUG"] = True

df_read = pandas.read_json('data.json',orient='columns',convert_axes=False,convert_dates=False)


@app.route('/', methods=['GET'])
def home():
    return "<h1>API for random walk data</h1>"

@app.route('/api/v1/resources/paths/all', methods=['GET'])
def api_all():
    return jsonify(df_read.T.values.tolist())

@app.route('/api/v1/resources/time', methods=['GET'])
def api_time():
    return jsonify([float(i) for i in df_read.index.tolist()])

@app.route('/api/v1/resources/paths', methods=['GET'])
def api_id():
    
    # return full sequence of the indexed variable and time index
    
    if 'fullsequence_id' in request.args: 
        id = int(request.args['fullsequence_id'])
        seq = df_read.iloc[:,id]
        return jsonify([seq.values.tolist(),[float(i) for i in seq.index.tolist()]])
    
    # return order statistics and corresponding time localization
    
    elif 'order_statistics_id' in request.args:
        id = int(request.args['order_statistics_id'])
        seq = df_read.iloc[:,id].sort_values(ascending=True)
        return jsonify([seq.values.tolist(),[float(i) for i in seq.index.tolist()]])
    
    # return first difference of the indexed variable and time index
    
    elif 'first_delta_id' in request.args:
        id = int(request.args['first_delta_id'])
        seq = df_read.iloc[:,id].diff()
        return jsonify([seq.values.tolist(),[float(i) for i in seq.index.tolist()]])
    
    else:
        return "Error: No id field provided. Please specify an id."

app.run()