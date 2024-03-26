#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd 
import os


# In[2]:


# 获取当前目录下所有的xlsx文件
xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]

# 初始化一个空的DataFrame，用于合并数据
combined_df = pd.DataFrame()

# 遍历所有xlsx文件，读取并合并到combined_df中
for file in xlsx_files:
    df = pd.read_excel(file)
    combined_df = pd.concat([combined_df, df], ignore_index=True)


# In[3]:


combined_df['空调是否开闭'].value_counts(),combined_df['百叶窗是否开闭'].value_counts(),combined_df['喷淋是否开闭'].value_counts()

## 空调存在严重的类别不均衡问题


# In[4]:


import math
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 选择中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False 


# In[9]:


def plot_distribution(dataset,cols=5,width=20,height=15,hspace=0.2,wspace=0.5):
    plt.style.use('seaborn-whitegrid')
    fig = plt.figure(figsize=(width,height))
    fig.subplots_adjust(left=None,bottom=None,right=None,top=None,wspace=wspace,hspace=hspace)
    rows = math.ceil(float(dataset.shape[1]) / cols)

    for i,column in enumerate(dataset.columns.tolist()):
        ax = fig.add_subplot(rows,cols,i+1)

        if dataset.dtypes[column] == np.object:
            g = sns.countplot(y=column,data=dataset)
            plt.title(str(column))
            plt.xticks(rotation=25)
        else:
            g = sns.distplot(dataset[column])
            plt.title(str(column))
            plt.xticks(rotation=25)


# In[8]:


import warnings
warnings.filterwarnings('ignore')
plot_distribution(combined_df.drop(['日期','时间'],axis=1),cols=3,width=20,height=20,hspace=0.45,wspace=0.5)


# In[10]:


# 特征工程
def feature(df):
    # 合并日期和时间为新的时间戳特征
    df['时间戳'] = pd.to_datetime(df['日期'] + ' ' + df['时间'])
    df['时间'] = pd.to_datetime(df['时间'])
    # 提取星期几和月份
    df['星期几'] = df['时间戳'].dt.dayofweek
    # 提取时间特征：早上、中午、晚上、半夜
    df['时段'] = pd.cut(df['时间'].dt.hour, bins=[0, 6, 12, 18, 24], labels=['半夜', '早上', '中午', '晚上'], include_lowest=True)
    # 对时段进行独热编码
    df = pd.get_dummies(df, columns=['时段'], prefix='时段')
    # 计算室内外温湿度差值
    df['温度差'] = df['室内温度'] - df['室外温度']
    df['湿度差'] = df['室内湿度'] - df['室外湿度']
    
    # 创建温度和湿度的滞后特征
    df['室内温度_滞后1'] = df['室内温度'].shift(1)
    df['室内湿度_滞后1'] = df['室内湿度'].shift(1)
    df['室内温度_滞后2'] = df['室内温度'].shift(2)
    df['室内湿度_滞后2'] = df['室内湿度'].shift(2)

    # 创建辐射的滞后特征
    df['室外水平辐射_滞后1'] = df['室外水平辐射'].shift(1)
    df['室内水平辐射_滞后1'] = df['室内水平辐射'].shift(1)
    
    # 添加辐射的统计信息
    df['室外水平辐射_均值'] = df['室外水平辐射'].rolling(window=3).mean()
    df['室内水平辐射_均值'] = df['室内水平辐射'].rolling(window=3).mean()
    df['室内温度_滑动均值'] = df['室内温度'].rolling(window=3).mean()
    df['室内温度_滑动标准差'] = df['室内温度'].rolling(window=3).std()
    
    df['温湿度交互'] = df['室内温度'] * df['室内湿度'] #计算室内温度与湿度的乘积或其他组合，以考虑室内的综合环境。
    df['温度辐射交互'] = df['室内温度'] * df['室内水平辐射'] # 考虑室内温度和水平辐射之间的关系。
    
    return df


# In[11]:


df = feature(combined_df)


# In[12]:


# 删除缺失值
train = df.dropna()
train = train.drop(['日期','时间','时间戳'],axis=1)


# In[13]:


feature_x = ['室外温度', '室外湿度', '室外水平辐射', '室内温度', '室内湿度', '室内水平辐射','星期几', '时段_半夜', '时段_早上', '时段_中午', '时段_晚上', '温度差',
     '湿度差', '室内温度_滞后1', '室内湿度_滞后1', '室内温度_滞后2', '室内湿度_滞后2', '室外水平辐射_滞后1',
     '室内水平辐射_滞后1', '室外水平辐射_均值', '室内水平辐射_均值', '室内温度_滑动均值', '室内温度_滑动标准差',
     '温湿度交互', '温度辐射交互']


# In[14]:


len(feature_x)


# In[15]:


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def train_evaluate_models(X, y):
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6666)

    # 初始化分类器
    rfc = RandomForestClassifier(random_state=6666)
    lgbm = LGBMClassifier(random_state=6666)

    # 训练分类器
    rfc.fit(X_train, y_train)
    lgbm.fit(X_train, y_train)

    # 预测结果
    rfc_pred = rfc.predict(X_test)
    lgbm_pred = lgbm.predict(X_test)

    # 计算评价指标
    rfc_scores = [accuracy_score(y_test, rfc_pred), precision_score(y_test, rfc_pred),
                  recall_score(y_test, rfc_pred), f1_score(y_test, rfc_pred),
                  roc_auc_score(y_test, rfc_pred)]

    lgbm_scores = [accuracy_score(y_test, lgbm_pred), precision_score(y_test, lgbm_pred),
                   recall_score(y_test, lgbm_pred), f1_score(y_test, lgbm_pred),
                   roc_auc_score(y_test, lgbm_pred)]

    # 尝试不同的权重组合
    best_weighted_model = None
    best_weighted_scores = [0, 0, 0, 0, 0]

    for weight in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        # 定义加权模型
        weighted_pred = weight * rfc_pred + (1 - weight) * lgbm_pred

        # 计算加权模型的评价指标
        weighted_scores = [roc_auc_score(y_test, weighted_pred)]

        # 更新最佳权重组合
        if weighted_scores[0] > best_weighted_scores[0]:  # 使用 AUC 作为比较标准
            best_weighted_scores = weighted_scores
            best_weighted_model = f'Weighted({weight} * RFC + {1 - weight} * LGBM)'

    # 构建模型分数的DataFrame
    df_scores = pd.DataFrame({
        'Model': ['RFC', 'LGBM', best_weighted_model],
        'Accuracy': [rfc_scores[0], lgbm_scores[0],'无'],
        'Precision': [rfc_scores[1], lgbm_scores[1],'无'],
        'Recall': [rfc_scores[2], lgbm_scores[2],'无'],
        'F1 Score': [rfc_scores[3], lgbm_scores[3],'无'],
        'AUC': [rfc_scores[4], lgbm_scores[4], best_weighted_scores[0]]
    })

    # 找到最优模型
    best_model = df_scores.loc[df_scores['AUC'].idxmax(), 'Model']

    return best_model, df_scores


# In[ ]:


# 空调

best_model, model_scores = train_evaluate_models(train[feature_x], train['空调是否开闭'])

# 打印最优模型和模型分数
print("Best Model:", best_model)
print("\nModel Scores:")
print(model_scores)

# joblib保存模型
import joblib
joblib.dump(best_model, 'airconditioner.pkl')


# In[ ]:


# 百叶窗
best_model, model_scores = train_evaluate_models(train[feature_x], train['百叶窗是否开闭'])
# 打印
print("Best Model:", best_model)
print("\nModel Scores:")
print(model_scores)
# joblib保存模型
import joblib
joblib.dump(best_model, 'byc.pkl')


# In[16]:


# 喷淋
best_model, model_scores = train_evaluate_models(train[feature_x], train['喷淋是否开闭'])
# 打印
print("Best Model:", best_model)
print("\nModel Scores:")
print(model_scores)
# joblib保存模型
import joblib
joblib.dump(best_model, 'pl.pkl')


# In[19]:


# 空调温度预测
from sklearn.ensemble import RandomForestRegressor
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def train_evaluate_regression_models(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=6666)


    rfr = RandomForestRegressor(random_state=6666)
    lgbmr = LGBMRegressor(random_state=6666)

    rfr.fit(X_train, y_train)
    lgbmr.fit(X_train, y_train)

    rfr_pred = rfr.predict(X_test)
    lgbmr_pred = lgbmr.predict(X_test)

    rfr_scores = [mean_squared_error(y_test, rfr_pred), mean_absolute_error(y_test, rfr_pred), r2_score(y_test, rfr_pred)]
    lgbmr_scores = [mean_squared_error(y_test, lgbmr_pred), mean_absolute_error(y_test, lgbmr_pred), r2_score(y_test, lgbmr_pred)]


    best_weighted_model = None
    best_weighted_scores = [float('inf'), float('inf'), float('-inf')]

    for weight in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
        weighted_pred = weight * rfr_pred + (1 - weight) * lgbmr_pred

        weighted_scores = [mean_squared_error(y_test, weighted_pred), mean_absolute_error(y_test, weighted_pred), r2_score(y_test, weighted_pred)]


        if weighted_scores[0] < best_weighted_scores[0]:  
            best_weighted_scores = weighted_scores
            best_weighted_model = f'Weighted({weight} * RFR + {1 - weight} * LGBMR)'

    df_scores = pd.DataFrame({
        'Model': ['RFR', 'LGBMR', best_weighted_model],
        'Mean Squared Error': [rfr_scores[0], lgbmr_scores[0], best_weighted_scores[0]],
        'Mean Absolute Error': [rfr_scores[1], lgbmr_scores[1], best_weighted_scores[1]],
        'R2 Score': [rfr_scores[2], lgbmr_scores[2], best_weighted_scores[2]]
    })

    best_model = df_scores.loc[df_scores['Mean Squared Error'].idxmin(), 'Model']

    return best_model, df_scores


# In[20]:


# 空调温度预测
tran_new = train[train['空调是否开闭']==1]


best_model, model_scores = train_evaluate_regression_models(tran_new[feature_x], tran_new['空调温度'])
# 打印
print("Best Model:", best_model)
print("\nModel Scores:")
print(model_scores)
# joblib保存模型
import joblib
joblib.dump(best_model, 'wd.pkl')


# In[ ]:




