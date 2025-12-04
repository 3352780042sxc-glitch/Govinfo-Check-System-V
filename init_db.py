from app import app, db
from app.models import User, Role
from app import bcrypt

with app.app_context():
    # 创建角色
    admin_role = Role(name='管理员', description='具有所有功能的权限')
    user_role = Role(name='普通用户', description='登录后可以看到数据报表和最新的报告')
    
    # 检查角色是否已存在
    if not Role.query.filter_by(name='管理员').first():
        db.session.add(admin_role)
    
    if not Role.query.filter_by(name='普通用户').first():
        db.session.add(user_role)
    
    db.session.commit()
    
    # 创建管理员用户
    admin_user = User.query.filter_by(username='admin').first()
    if not admin_user:
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin_user = User(username='admin', password_hash=hashed_password, role_id=admin_role.id)
        db.session.add(admin_user)
        db.session.commit()
        print('管理员用户创建成功，用户名：admin，密码：admin123')
    else:
        print('管理员用户已存在')
    
    print('数据库初始化完成')
