from app import app, Data
from flask import request

@app.route('/data', methods=['GET', 'POST'])
def data():
    result = Data.query.all()
    data = []
    for row in result:
        data.append(row.jsonformat())
    # for row in result2:
    #     data.append(row.jsonformat())

    res = {
        "code": 200,
        "msg": "OK",
        "data": data
    }

    return res