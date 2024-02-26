SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1:3307/sysplus' # 默认数据库（主数据库）
UPLOAD_FOLDER = 'uploads'

# 需要绑定的多个数据库
SQLALCHEMY_BINDS = {
    'param': 'mysql://root:Qianfankeji!234@59.110.6.63:20011/wlwtext',
    'db2': 'mysql://ln:ln123456!@rm-2zex4b7196b1g6fyzco.mysql.rds.aliyuncs.com:3306/fittingdata',
}
