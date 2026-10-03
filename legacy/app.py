from flask import Flask, render_template, redirect, url_for, request, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cantiere.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
Path(app.config['UPLOAD_FOLDER']).mkdir(parents=True, exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='user')  # admin, manager, user
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    client_type = db.Column(db.String(20), default='Privato')
    vat_number = db.Column(db.String(50))
    tax_code = db.Column(db.String(50))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    boats = db.relationship('Boat', backref='client', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='client', lazy=True)
    documents = db.relationship('Document', backref='client', lazy=True)

class Boat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    boat_type = db.Column(db.String(100))
    length = db.Column(db.Float)
    registration = db.Column(db.String(100))
    engine = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='boat', lazy=True)

class Warehouse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    location = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('WarehouseItem', backref='warehouse', lazy=True)

class WarehouseItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(db.Integer, db.ForeignKey('warehouse.id'), nullable=False)
    sku = db.Column(db.String(100))
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    location = db.Column(db.String(200))
    unit = db.Column(db.String(20), default='pz')
    quantity = db.Column(db.Float, default=0)
    min_quantity = db.Column(db.Float, default=0)
    cost_price = db.Column(db.Float, default=0)
    sale_price = db.Column(db.Float, default=0)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    movements = db.relationship('Movement', backref='item', lazy=True)

class Movement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('warehouse_item.id'), nullable=False)
    movement_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    movement_type = db.Column(db.String(20), nullable=False)  # Carico, Scarico, Reso
    quantity = db.Column(db.Float, nullable=False)
    unit_cost = db.Column(db.Float, default=0)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    supplier = db.Column(db.String(200))
    note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    boat_id = db.Column(db.Integer, db.ForeignKey('boat.id'), nullable=False)
    title = db.Column(db.String(300), nullable=False)
    status = db.Column(db.String(50), default='Preventivo')
    priority = db.Column(db.String(20), default='Media')
    start_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    budget = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    tax_rate = db.Column(db.Float, default=22)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    jobs = db.relationship('Job', backref='order', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='order', lazy=True)
    attachments = db.relationship('Attachment', backref='order', lazy=True, cascade='all, delete-orphan')
    movements = db.relationship('Movement', backref='order', lazy=True)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), default='Manodopera')
    status = db.Column(db.String(50), default='Da fare')
    quantity = db.Column(db.Float, default=1)
    unit = db.Column(db.String(20), default='pz')
    unit_cost = db.Column(db.Float, default=0)
    unit_price = db.Column(db.Float, default=0)
    assigned_to = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doc_number = db.Column(db.String(50), unique=True, nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)  # Proforma, Fattura, DDT
    doc_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.Date)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String(50), default='Bozza')
    discount = db.Column(db.Float, default=0)
    tax_rate = db.Column(db.Float, default=22)
    notes = db.Column(db.Text)
    xml_generated = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    lines = db.relationship('DocumentLine', backref='document', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='document', lazy=True, cascade='all, delete-orphan')

class DocumentLine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    quantity = db.Column(db.Float, default=1)
    unit_price = db.Column(db.Float, default=0)
    line_order = db.Column(db.Integer, default=0)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    payment_date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Float, nullable=False)
    method = db.Column(db.String(50), default='Bonifico')
    note = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Attachment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    filename = db.Column(db.String(500), nullable=False)
    original_filename = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    description = db.Column(db.String(500))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200))
    company_address = db.Column(db.String(500))
    company_vat = db.Column(db.String(50))
    company_phone = db.Column(db.String(50))
    company_email = db.Column(db.String(120))
    tax_rate = db.Column(db.Float, default=22)
    proforma_prefix = db.Column(db.String(10), default='PF')
    invoice_prefix = db.Column(db.String(10), default='FT')
    ddt_prefix = db.Column(db.String(10), default='DDT')
    proforma_counter = db.Column(db.Integer, default=1)
    invoice_counter = db.Column(db.Integer, default=1)
    ddt_counter = db.Column(db.Integer, default=1)
    order_counter = db.Column(db.Integer, default=1)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def index():
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Credenziali non valide', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_clients': Client.query.count(),
        'total_boats': Boat.query.count(),
        'active_orders': Order.query.filter(Order.status.in_(['Preventivo', 'Approvata', 'In lavorazione'])).count(),
        'low_stock': WarehouseItem.query.filter(WarehouseItem.quantity <= WarehouseItem.min_quantity).count(),
        'open_documents': Document.query.filter(Document.status != 'Annullata').count(),
    }
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    low_stock_items = WarehouseItem.query.filter(WarehouseItem.quantity <= WarehouseItem.min_quantity).limit(10).all()
    
    return render_template('dashboard.html', stats=stats, recent_orders=recent_orders, low_stock_items=low_stock_items)

@app.route('/clients')
@login_required
def clients():
    clients_list = Client.query.order_by(Client.name).all()
    return render_template('clients.html', clients=clients_list)

@app.route('/clients/add', methods=['GET', 'POST'])
@login_required
def add_client():
    if request.method == 'POST':
        client = Client(
            name=request.form['name'],
            client_type=request.form.get('client_type', 'Privato'),
            vat_number=request.form.get('vat_number'),
            tax_code=request.form.get('tax_code'),
            email=request.form.get('email'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            notes=request.form.get('notes')
        )
        db.session.add(client)
        db.session.commit()
        flash('Cliente aggiunto con successo', 'success')
        return redirect(url_for('clients'))
    
    return render_template('client_form.html', client=None)

@app.route('/clients/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_client(id):
    client = Client.query.get_or_404(id)
    
    if request.method == 'POST':
        client.name = request.form['name']
        client.client_type = request.form.get('client_type', 'Privato')
        client.vat_number = request.form.get('vat_number')
        client.tax_code = request.form.get('tax_code')
        client.email = request.form.get('email')
        client.phone = request.form.get('phone')
        client.address = request.form.get('address')
        client.notes = request.form.get('notes')
        
        db.session.commit()
        flash('Cliente aggiornato con successo', 'success')
        return redirect(url_for('clients'))
    
    return render_template('client_form.html', client=client)

@app.route('/clients/<int:id>/delete', methods=['POST'])
@login_required
def delete_client(id):
    client = Client.query.get_or_404(id)
    db.session.delete(client)
    db.session.commit()
    flash('Cliente eliminato', 'success')
    return redirect(url_for('clients'))

@app.route('/boats')
@login_required
def boats():
    boats_list = Boat.query.order_by(Boat.name).all()
    return render_template('boats.html', boats=boats_list)

@app.route('/boats/add', methods=['GET', 'POST'])
@login_required
def add_boat():
    if request.method == 'POST':
        boat = Boat(
            client_id=request.form['client_id'],
            name=request.form['name'],
            boat_type=request.form.get('boat_type'),
            length=request.form.get('length', type=float) or 0,
            registration=request.form.get('registration'),
            engine=request.form.get('engine'),
            notes=request.form.get('notes')
        )
        db.session.add(boat)
        db.session.commit()
        flash('Imbarcazione aggiunta con successo', 'success')
        return redirect(url_for('boats'))
    
    clients_list = Client.query.order_by(Client.name).all()
    return render_template('boat_form.html', boat=None, clients=clients_list)

@app.route('/boats/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_boat(id):
    boat = Boat.query.get_or_404(id)
    
    if request.method == 'POST':
        boat.client_id = request.form['client_id']
        boat.name = request.form['name']
        boat.boat_type = request.form.get('boat_type')
        boat.length = request.form.get('length', type=float) or 0
        boat.registration = request.form.get('registration')
        boat.engine = request.form.get('engine')
        boat.notes = request.form.get('notes')
        
        db.session.commit()
        flash('Imbarcazione aggiornata con successo', 'success')
        return redirect(url_for('boats'))
    
    clients_list = Client.query.order_by(Client.name).all()
    return render_template('boat_form.html', boat=boat, clients=clients_list)

@app.route('/boats/<int:id>/delete', methods=['POST'])
@login_required
def delete_boat(id):
    boat = Boat.query.get_or_404(id)
    db.session.delete(boat)
    db.session.commit()
    flash('Imbarcazione eliminata', 'success')
    return redirect(url_for('boats'))

@app.route('/orders')
@login_required
def orders():
    orders_list = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders_list)

@app.route('/orders/add', methods=['GET', 'POST'])
@login_required
def add_order():
    if request.method == 'POST':
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        
        order_number = f"COM-{datetime.now().year}-{str(settings.order_counter).zfill(3)}"
        settings.order_counter += 1
        
        order = Order(
            order_number=order_number,
            client_id=request.form['client_id'],
            boat_id=request.form['boat_id'],
            title=request.form['title'],
            status=request.form.get('status', 'Preventivo'),
            priority=request.form.get('priority', 'Media'),
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form.get('start_date') else None,
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date() if request.form.get('due_date') else None,
            budget=request.form.get('budget', type=float) or 0,
            discount=request.form.get('discount', type=float) or 0,
            tax_rate=request.form.get('tax_rate', type=float) or 22,
            notes=request.form.get('notes')
        )
        
        db.session.add(order)
        db.session.commit()
        flash('Commessa creata con successo', 'success')
        return redirect(url_for('view_order', id=order.id))
    
    clients_list = Client.query.order_by(Client.name).all()
    boats_list = Boat.query.order_by(Boat.name).all()
    return render_template('order_form.html', order=None, clients=clients_list, boats=boats_list)

@app.route('/orders/<int:id>')
@login_required
def view_order(id):
    order = Order.query.get_or_404(id)
    jobs = Job.query.filter_by(order_id=id).all()
    attachments = Attachment.query.filter_by(order_id=id).all()
    return render_template('order_detail.html', order=order, jobs=jobs, attachments=attachments)

@app.route('/orders/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_order(id):
    order = Order.query.get_or_404(id)
    
    if request.method == 'POST':
        order.client_id = request.form['client_id']
        order.boat_id = request.form['boat_id']
        order.title = request.form['title']
        order.status = request.form.get('status', 'Preventivo')
        order.priority = request.form.get('priority', 'Media')
        order.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form.get('start_date') else None
        order.due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date() if request.form.get('due_date') else None
        order.budget = request.form.get('budget', type=float) or 0
        order.discount = request.form.get('discount', type=float) or 0
        order.tax_rate = request.form.get('tax_rate', type=float) or 22
        order.notes = request.form.get('notes')
        
        db.session.commit()
        flash('Commessa aggiornata con successo', 'success')
        return redirect(url_for('view_order', id=order.id))
    
    clients_list = Client.query.order_by(Client.name).all()
    boats_list = Boat.query.order_by(Boat.name).all()
    return render_template('order_form.html', order=order, clients=clients_list, boats=boats_list)

@app.route('/warehouse')
@login_required
def warehouse():
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return render_template('warehouse.html', warehouses=warehouses)

@app.route('/warehouse/items')
@login_required
def warehouse_items():
    items = WarehouseItem.query.order_by(WarehouseItem.name).all()
    return render_template('warehouse_items.html', items=items)

@app.route('/warehouse/items/add', methods=['GET', 'POST'])
@login_required
def add_warehouse_item():
    if request.method == 'POST':
        item = WarehouseItem(
            warehouse_id=request.form['warehouse_id'],
            sku=request.form.get('sku'),
            name=request.form['name'],
            category=request.form.get('category'),
            location=request.form.get('location'),
            unit=request.form.get('unit', 'pz'),
            quantity=request.form.get('quantity', type=float) or 0,
            min_quantity=request.form.get('min_quantity', type=float) or 0,
            cost_price=request.form.get('cost_price', type=float) or 0,
            sale_price=request.form.get('sale_price', type=float) or 0,
            notes=request.form.get('notes')
        )
        db.session.add(item)
        db.session.commit()
        flash('Articolo aggiunto con successo', 'success')
        return redirect(url_for('warehouse_items'))
    
    warehouses = Warehouse.query.filter_by(is_active=True).all()
    return render_template('warehouse_item_form.html', item=None, warehouses=warehouses)

@app.route('/documents')
@login_required
def documents():
    docs = Document.query.order_by(Document.created_at.desc()).all()
    return render_template('documents.html', documents=docs)

@app.route('/documents/add/<doc_type>', methods=['GET', 'POST'])
@login_required
def add_document(doc_type):
    if request.method == 'POST':
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        
        if doc_type == 'proforma':
            doc_number = f"{settings.proforma_prefix}-{datetime.now().year}-{str(settings.proforma_counter).zfill(3)}"
            settings.proforma_counter += 1
        elif doc_type == 'invoice':
            doc_number = f"{settings.invoice_prefix}-{datetime.now().year}-{str(settings.invoice_counter).zfill(3)}"
            settings.invoice_counter += 1
        elif doc_type == 'ddt':
            doc_number = f"{settings.ddt_prefix}-{datetime.now().year}-{str(settings.ddt_counter).zfill(3)}"
            settings.ddt_counter += 1
        
        doc = Document(
            doc_number=doc_number,
            doc_type=doc_type.capitalize(),
            doc_date=datetime.strptime(request.form['doc_date'], '%Y-%m-%d').date(),
            due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date() if request.form.get('due_date') else None,
            client_id=request.form['client_id'],
            order_id=request.form.get('order_id') or None,
            status=request.form.get('status', 'Bozza'),
            discount=request.form.get('discount', type=float) or 0,
            tax_rate=request.form.get('tax_rate', type=float) or 22,
            notes=request.form.get('notes')
        )
        
        db.session.add(doc)
        db.session.commit()
        flash(f'{doc_type.capitalize()} creato con successo', 'success')
        return redirect(url_for('view_document', id=doc.id))
    
    clients_list = Client.query.order_by(Client.name).all()
    orders_list = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('document_form.html', document=None, doc_type=doc_type, clients=clients_list, orders=orders_list)

@app.route('/documents/<int:id>')
@login_required
def view_document(id):
    doc = Document.query.get_or_404(id)
    lines = DocumentLine.query.filter_by(document_id=id).order_by(DocumentLine.line_order).all()
    payments = Payment.query.filter_by(document_id=id).order_by(Payment.payment_date.desc()).all()
    return render_template('document_detail.html', document=doc, lines=lines, payments=payments)

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    settings = Settings.query.first()
    if not settings:
        settings = Settings()
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        if current_user.role != 'admin':
            flash('Solo gli amministratori possono modificare le impostazioni', 'error')
            return redirect(url_for('settings'))
        
        settings.company_name = request.form.get('company_name')
        settings.company_address = request.form.get('company_address')
        settings.company_vat = request.form.get('company_vat')
        settings.company_phone = request.form.get('company_phone')
        settings.company_email = request.form.get('company_email')
        settings.tax_rate = request.form.get('tax_rate', type=float) or 22
        settings.proforma_prefix = request.form.get('proforma_prefix', 'PF')
        settings.invoice_prefix = request.form.get('invoice_prefix', 'FT')
        settings.ddt_prefix = request.form.get('ddt_prefix', 'DDT')
        
        db.session.commit()
        flash('Impostazioni salvate con successo', 'success')
    
    return render_template('settings.html', settings=settings)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@cantiere.it',
                role='admin'
            )
            admin.set_password('admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: admin/admin")
        
        # Create default settings if not exists
        if not Settings.query.first():
            settings = Settings()
            db.session.add(settings)
            db.session.commit()
        
        # Create default warehouse if not exists
        if not Warehouse.query.first():
            warehouse = Warehouse(name='Magazzino Principale', location='Sede')
            db.session.add(warehouse)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)