import joblib
import pandas as pd
import re

def predictRes(file_path, data):
#     X_test = pd.DataFrame(data)
    X_test = data
    best_model = joblib.load(file_path+'/model.pkl')
    rfc = joblib.load(file_path+'/rfc')
    lgbm = joblib.load(file_path+'/lgbm')


    # 提取最佳模型
    if best_model == 'RFC':
        model = rfc
        res = model.predict(X_test)
    elif best_model == 'LGBM':
        model = lgbm
        res = model.predict(X_test)
    else:
        # 解析加权模型的权重
        # 提取括号内的内容
        contents = re.search(r'\((.*?)\)', best_model).group(1)

        # 按加号分割
        parts = contents.split('+')

        weights = []
        for part in parts:
            weight = float(re.search(r'\d+\.\d+', part).group())
            weights.append(weight)

        rfc_pred = rfc.predict(X_test)  # 使用训练好的 RFC 模型预测
        # lgbm_pred = lgbm.predict(X_test)  # 使用训练好的 LGBM 模型预测
        # print(weights, rfc_pred)

        # res = weights[0] * rfc_pred + weights[1] * lgbm_pred
        res = rfc_pred

    # 对新数据进行预测
    # your_prediction = model.predict(X_test)
    return res

# 测试函数
if __name__ == "__main__":
    
    X_test = pd.read_excel("pre.xlsx", header=None)
    res = predictRes("./temperature", X_test)
    print(res[0])