from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, current_user, logout_user, login_required
from app import app, db
from app.models import Info, User, Role
from app.forms import InfoForm, LoginForm, RegisterForm, CrawlerForm
from app.crawler import baidu_news_crawler

# 登录路由
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('登录失败，请检查用户名和密码', 'danger')
    return render_template('login.html', form=form, title='用户登录')

# 退出路由
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# 首页路由
@app.route('/')
@login_required
def index(): 
    info_count = Info.query.count()
    processed_count = Info.query.filter_by(status='已处理').count()
    return render_template('index.html', info_count=info_count, processed_count=processed_count)

@app.route('/info/list')
@login_required
def info_list():
    infos = Info.query.all()
    return render_template('info_list.html', infos=infos)

@app.route('/info/<int:info_id>')
@login_required
def info_detail(info_id):
    info = Info.query.get_or_404(info_id)
    return render_template('info_detail.html', info=info)

@app.route('/info/add', methods=['GET', 'POST'])
@login_required
def info_add():
    form = InfoForm()
    if form.validate_on_submit():
        info = Info(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            status=form.status.data
        )
        db.session.add(info)
        db.session.commit()
        flash('信息添加成功！', 'success')
        return redirect(url_for('info_list'))
    return render_template('info_add.html', form=form)

@app.route('/info/<int:info_id>/edit', methods=['GET', 'POST'])
@login_required
def info_edit(info_id):
    info = Info.query.get_or_404(info_id)
    form = InfoForm()
    if form.validate_on_submit():
        info.title = form.title.data
        info.content = form.content.data
        info.category = form.category.data
        info.status = form.status.data
        db.session.commit()
        flash('信息编辑成功！', 'success')
        return redirect(url_for('info_detail', info_id=info.id))
    elif request.method == 'GET':
        form.title.data = info.title
        form.content.data = info.content
        form.category.data = info.category
        form.status.data = info.status
    return render_template('info_edit.html', form=form, info=info)

@app.route('/info/<int:info_id>/delete')
@login_required
def info_delete(info_id):
    info = Info.query.get_or_404(info_id)
    db.session.delete(info)
    db.session.commit()
    flash('信息删除成功！', 'success')
    return redirect(url_for('info_list'))

# 角色管理路由
@app.route('/admin/roles')
@login_required
def role_list():
    # 只有管理员可以访问
    if current_user.role.name != '管理员':
        flash('没有权限访问该页面', 'danger')
        return redirect(url_for('index'))
    roles = Role.query.all()
    return render_template('admin/role_list.html', roles=roles)

# 用户管理路由
@app.route('/admin/users')
@login_required
def user_list():
    # 只有管理员可以访问
    if current_user.role.name != '管理员':
        flash('没有权限访问该页面', 'danger')
        return redirect(url_for('index'))
    users = User.query.all()
    return render_template('admin/user_list.html', users=users)

# 添加用户路由
@app.route('/admin/user/add', methods=['GET', 'POST'])
@login_required
def user_add():
    # 只有管理员可以访问
    if current_user.role.name != '管理员':
        flash('没有权限访问该页面', 'danger')
        return redirect(url_for('index'))
    form = RegisterForm()
    form.role_id.choices = [(role.id, role.name) for role in Role.query.all()]
    if form.validate_on_submit():
        user = User(username=form.username.data, role_id=form.role_id.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('用户添加成功！', 'success')
        return redirect(url_for('user_list'))
    return render_template('admin/user_add.html', form=form)

# 系统设置路由
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def settings():
    # 只有管理员可以访问
    if current_user.role.name != '管理员':
        flash('没有权限访问该页面', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        app_name = request.form.get('app_name')
        # 这里可以添加更多系统设置
        flash('系统设置已更新！', 'success')
        return redirect(url_for('settings'))
    return render_template('admin/settings.html')

# 数据抓取路由
@app.route('/crawler', methods=['GET', 'POST'])
@login_required
def crawler():
    form = CrawlerForm()
    results = []
    keyword = None
    
    if form.validate_on_submit():
        keyword = form.keyword.data
        pages = form.pages.data
        quantity = form.quantity.data
        flash(f'正在抓取关于"{keyword}"的新闻数据...', 'info')
        
        # 调用爬虫函数
        results = baidu_news_crawler(keyword, pages=pages, quantity=quantity)
        
        if results:
            flash(f'抓取完成，共找到 {len(results)} 条新闻！', 'success')
        else:
            flash(f'没有找到关于"{keyword}"的新闻数据', 'warning')
    
    return render_template('crawler.html', form=form, results=results, keyword=keyword)
