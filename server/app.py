from flask import Flask,g
from flask import jsonify
from flask_cors import CORS
from main import run_df_csv
import logging as logger
from neo4j import GraphDatabase, basic_auth
from neo4j.exceptions import Neo4jError
import neo4j.time
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# DATABASE_USERNAME = env('MOVIE_DATABASE_USERNAME')
# DATABASE_PASSWORD = env('MOVIE_DATABASE_PASSWORD')
# DATABASE_URL = env('MOVIE_DATABASE_URL')

DATABASE_URL = 'bolt://localhost:7687'
DATABASE_USERNAME = 'neo4j'
DATABASE_PASSWORD = 'yugijimoh'
driver = GraphDatabase.driver(DATABASE_URL, auth=basic_auth(DATABASE_USERNAME, str(DATABASE_PASSWORD)))

def get_db():
    if not hasattr(g, 'neo4j_db'):
        g.neo4j_db = driver.session()
    return g.neo4j_db
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'neo4j_db'):
        g.neo4j_db.close()


def buildNodes(nodeRecord):  # 构建web显示节点
    data = {"id": nodeRecord._id, "label": list(nodeRecord._labels)[0]}  # 将集合元素变为list，然后取出值
    data.update(dict(nodeRecord._properties))

    #return {"data": data}
    return data


def buildEdges(relationRecord):  # 构建web显示边
    data = {"source": relationRecord.start_node._id,
            "target": relationRecord.end_node._id,
            "relationship": relationRecord.type}
    #return {"data": data}
    return data


@app.route('/graph')
def get_graph():
    # nodes = list(map(buildNodes, graph.run('MATCH (n) RETURN n').data()))
    #
    # edges = list(map(buildEdges, graph.run('MATCH ()-[r]->() RETURN r').data()))
    # elements = {"nodes": nodes, "edges": edges}

    with driver.session() as session:
        results = session.run(
            'MATCH (p1{name:"Laurence Fishburne"})-[r1:ACTED_IN]->(m)<-[r2:DIRECTED]-(p2)  RETURN p1,m,p2,r1,r2').values()
        nodeList = []
        edgeList = []
        categoryList = []
        for result in results:
            nodeList.append(result[0])
            nodeList.append(result[1])
            nodeList.append(result[2])
            nodeList = list(set(nodeList))
            edgeList.append(result[3])
            edgeList.append(result[4])

        nodes = list(map(buildNodes, nodeList))
        edges = list(map(buildEdges, edgeList))
        categoryList=[{"label":"Movie"},{"label":"Person"}]
        logger.warning(categoryList)
    return jsonify(elements={"nodes": nodes, "edges": edges, "categories":categoryList})

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/getMsg', methods=['GET', 'POST'])
def home():
    response = {
        'msg': 'Hello, Python !'
    }
    return jsonify(response)

@app.route('/loadCsv', methods=['GET', 'POST'])
def load_csv():
    data = run_df_csv()
    data = data.to_json()
    response = {
        'msg': 'Hello, Python !',
        'data': data
    }
    logger.warning("#########################")
    logger.warning(data)
    return response


# start run
if __name__ == '__main__':
    app.run(debug = True)   # start up localhost:5000
   # app.run(host='your_ip_address') # set host public IP and run