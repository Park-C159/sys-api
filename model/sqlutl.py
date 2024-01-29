import pymysql
def sqlGet(conn, sql):
    conn.ping(reconnect=True)
    cursor = conn.cursor()

    cursor.execute(sql)
    result = cursor.fetchall()
    # for data in result:
    #     print(data)

    fields = cursor.description
    # print(fields)

    cursor.close()
    conn.close()

    column_list = []
    for i in fields:
        column_list.append(i[0])
    # print(column_list)

    res = []
    for row in result:
        data = {}
        for i in range(len(column_list)):
            data[column_list[i]] = row[i]
        res.append(data)
    return res

# values 是一个()元组类型
def sqlInsert(conn, sql, values):
    conn.ping(reconnect=True)
    cs1 = conn.cursor()
    # 执行sql语句
    res = 0
    res = cs1.execute(sql, values)

    # 提交之前的操作，如果之前已经执行多次的execute，那么就都进行提交
    conn.commit()

    # 关闭cursor对象
    cs1.close()
    # 关闭connection对象
    # conn.close()

    return res

# print(jsonData)


# d = ((1, 'CityOfSky', '544423', 'https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fb-ssl.duitang.com%2Fuploads%2Fitem%2F201410%2F03%2F20141003163119_XQxzi.thumb.700_0.jpeg&refer=http%3A%2F%2Fb-ssl.duitang.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1651471678&t=8f49c366f7029cbf3b3ab983f603776a', '15212371894', 1, datetime.date(2002, 4, 14), '1596770371@qq.com'), (2, 'root', '544423', None, None, 1, None, None), (3, 'root1', '544423', None, None, 1, None, None))
# d = dict(d)
# print(d)
# r = json.dumps(d)
# # r = json.dumps(r)
# print(r)