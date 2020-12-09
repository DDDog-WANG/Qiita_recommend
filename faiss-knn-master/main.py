from flask import Flask, jsonify, request
import json
import sys
import importlib

import faiss_knn

app = Flask(__name__)

@app.route('/knn')
def knn():
    id_list = request.args.get('id').split(',')
    print(id_list)
    count = int(request.args.get('count'))
    result = faiss_knn.search_knn(id_list, count)
    return json.dumps(result)

@app.route('/restart')
def restart():
    try:
        importlib.reload(faiss_knn)
    except:
        return jsonify({'message': 'error'}), 500
    else:
        return jsonify({'message': 'success'}), 200

host = sys.argv[1]
port = int(sys.argv[2])

app.run(host=host, port=port, debug=False)
