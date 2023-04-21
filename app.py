from flask import render_template, jsonify
from graph import loadData, random_graph, random_connected_graph, graph_to_dict, d3_format, export_json
# import datatime
import numpy as np
from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class FlaskJSONEncoder(_JSONEncoder):
    """重载flask的json encoder, 确保jsonfy()能解析numpy的json"""

    def default(self, obj):
        if isinstance(obj, (np.integer, np.floating, np.bool_)):
            return obj.item()
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        # elif isinstance(obj, (datetime.datetime, datetime.timedelta)):
        #     return obj.__str__()
        else:
            return super(FlaskJSONEncoder, self).default(obj)


class Flask(_Flask):
    """重载flask的jsonencoder, 确保能解析numpy的json"""
    json_encoder = FlaskJSONEncoder


app = Flask(__name__)



def create_random_d3_graph_dict():
    """
    Creates a random NetworkX graph and returns a dictionary 
    representation of the graph formatted for visualization in d3
    """
    G = random_connected_graph(15)
    graph_dict = graph_to_dict(G)
    d3_graph_dict = d3_format(graph_dict)
    return d3_graph_dict


@app.route('/forcetree')
def get_force_tree():
    # create a random graph and export to static file
    d3_graph_dict = create_random_d3_graph_dict()
    export_json(d3_graph_dict) #保存成json文件
    # client will load graph from static file
    return render_template("force-tree.html")


@app.route('/forcezoompan')
def get_force_zoom_pan():
    # create a random graph and export to static file
    d3_graph_dict = create_random_d3_graph_dict()
    export_json(d3_graph_dict)
    # client will load graph from static file
    return render_template("force-zoom-pan.html")


@app.route('/forcezoompan2')
def get_force_zoom_pan_2():
    # client will ask for graph data from /data route
    return render_template("force-zoom-pan-2.html")


@app.route('/data')
def get_data():
    # 这里需要实现自己提供数据
    G = loadData("clubs.mtx", "clubs.attr")
    # G = loadData("Caltech36.mtx", "Caltech36.attr")
    # print(G)
    graph_dict = graph_to_dict(G)
    # print("graph_dict", graph_dict)
    d3_graph_dict = d3_format(graph_dict)
    # create a random graph and return json via flask
    # d3_graph_dict = create_random_d3_graph_dict()
    # print("d3_graph_dict", d3_graph_dict)
    return jsonify(dict(data=d3_graph_dict))
    # return jsonify({'data':d3_graph_dict})


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    host_name = 'localhost'
    port_num = 5000
    app.run(debug=True, host=host_name, port=port_num)
