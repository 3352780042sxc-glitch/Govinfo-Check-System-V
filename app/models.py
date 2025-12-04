from app import db
from datetime import datetime
from flask_login import UserMixin

# 角色模型
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    users = db.relationship('User', backref='role', lazy=True)
    
    def __repr__(self):
        return f'<Role {self.name}>'

# 用户模型
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        from app import bcrypt
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        from app import bcrypt
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    publish_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(50), default='待审核')
    
    def __repr__(self):
        return f'<Info {self.title}>'

# 采集任务表
class CrawlTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(100), nullable=False)  # 搜索关键词
    pages = db.Column(db.Integer, nullable=False)  # 采集页数
    quantity = db.Column(db.Integer, nullable=False)  # 采集数量
    status = db.Column(db.String(20), default='进行中')  # 任务状态：进行中、已完成、已失败
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    finished_at = db.Column(db.DateTime, nullable=True)  # 完成时间
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # 创建者ID
    
    # 关系
    datas = db.relationship('CrawlData', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<CrawlTask {self.keyword}>'

# 采集数据表
class CrawlData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('crawl_task.id'), nullable=False)  # 所属任务ID
    title = db.Column(db.String(200), nullable=False)  # 标题
    summary = db.Column(db.Text, nullable=True)  # 摘要
    cover = db.Column(db.String(200), nullable=True)  # 封面图片URL
    original_url = db.Column(db.String(200), nullable=False)  # 原始URL
    source = db.Column(db.String(100), nullable=True)  # 来源
    content = db.Column(db.Text, nullable=True)  # 内容（深度采集时获取）
    is_deep_crawled = db.Column(db.Boolean, default=False)  # 是否已深度采集
    deep_crawl_status = db.Column(db.String(20), default='未采集')  # 深度采集状态：未采集、进行中、已完成、已失败
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新时间
    
    def __repr__(self):
        return f'<CrawlData {self.title}>'
