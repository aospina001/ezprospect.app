from flask_sqlalchemy import SQLAlchemy
from datetime import date, time, datetime

db = SQLAlchemy()

user_prospects = db.Table('user_prospects',
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("prospect_id", db.Integer, db.ForeignKey("prospects.id"), primary_key=True)
)

prospects_contacts = db.Table('prospects_contacts',
    db.Column("contact_id", db.Integer, db.ForeignKey("contacts.id"), primary_key=True),
    db.Column("prospect_id", db.Integer, db.ForeignKey("prospects.id"), primary_key=True)
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=False, nullable=False)
    first_name = db.Column(db.String(250), unique=False, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    userprospects = db.relationship('Prospects', secondary=user_prospects, backref=db.backref('prospectsuser', lazy='dynamic'))   
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __init__(self,email,password,first_name,last_name,phone_number):
        self.email=email
        self.password=password
        self.first_name=first_name
        self.last_name=last_name
        self.phone_number=phone_number
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "organization_id": self.organization_id
            # do not serialize the password, its a security breach
        }

class Prospects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    industry = db.Column(db.String(250), unique=False, nullable=False)
    address1 = db.Column(db.String(250), unique=False, nullable=False)
    city = db.Column(db.String(250), unique=False, nullable=False)
    state = db.Column(db.String(250), unique=False, nullable=False)
    zipCode = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    account = db.Column(db.String(250), unique=False, nullable=False)
    # background = db.Column(db.String(80), unique=False, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __init__(self,name,industry,address1,city,state,zipCode,phone_number,account):
        self.name=name
        self.industry=industry
        self.address1=address1
        self.city=city
        self.state=state
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.account=account
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<Prospects %r>' % self.account

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "industry": self.industry,
            "address1": self.address1,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone_number": self.phone_number,
            "account": self.account
            # do not serialize the password, its a security breach
        }

class Contacts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(250), unique=True, nullable=False)
    last_name = db.Column(db.String(250), unique=False, nullable=False)
    position = db.Column(db.String(250), unique=False, nullable=False)
    title = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(250), unique=False, nullable=False)
    phone_number = db.Column(db.String(250), unique=False, nullable=False)
    prospectscontacts = db.relationship('Prospects', secondary=prospects_contacts, backref=db.backref('prospectscontacts', lazy='dynamic'))
    created_at = db.Column(db.DateTime(timezone=True), unique=False, nullable=False) 
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)    

    def __init__(self,first_name,last_name,position,title,email,phone_number):
        self.first_name=first_name
        self.last_name=last_name
        self.position=position
        self.title=title
        self.email=email
        self.phone_number=phone_number
        self.created_at = datetime.now()
        self.is_active=True 

    def __repr__(self):
        return '<Contacts %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "position": self.position,
            "title": self.title,
            "email": self.email,
            "phone_number": self.phone_number
        }

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)      
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    # prospect_id = db.Column(Integer, ForeignKey('prospect.prospect_id'))
    # prospect = relationship(Prospects)
    # user_id = db.Column(Integer, ForeignKey('user.user_id'))
    # user = relationship(User)
    # organization_id = db.Column(Integer, ForeignKey('organization.organization_id'))
    # organization = relationship(Organization)
    # product_id = db.Column(Integer, ForeignKey('product.product_id'))
    # product = relationship(Product)

    def __init__(self):
        # self.firstname=firstname
        # self.lastname=lastname
        # self.position=position
        # self.title=title
        # self.email=email
        # self.zipCode=zipCode
        # self.phone_number=phone_number
        self.is_active=True 

    def __repr__(self):
        return '<Clients %r>' % self.id

    def serialize(self):
        return {
            "id": self.id
            # do not serialize the password, its a security breach
        }


class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    status = db.Column(db.Boolean(), unique=False, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))

    def __init__(self,name,description):
        self.name=name
        self.description=description
        self.is_active=True 

    def __repr__(self):
        return '<Products %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
            # do not serialize the password, its a security breach
        }


class Organizations(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address1 = db.Column(db.String(80), unique=False, nullable=False)
    address2 = db.Column(db.String(80), unique=False, nullable=False)
    city = db.Column(db.String(80), unique=False, nullable=False)
    state = db.Column(db.String(80), unique=False, nullable=False)
    zipCode = db.Column(db.Integer, unique=False, nullable=False)
    phone_number = db.Column(db.String(50), unique=False, nullable=False)
    users = db.relationship('User', backref="organizations")
    products = db.relationship('Products', backref="organizations")
    

    def __init__(self,name,address1,address2,city,state,zipCode,phone_number):
        self.name=name
        self.address1=address1
        self.address2=address2
        self.city=city
        self.state=state
        self.zipCode=zipCode
        self.phone_number=phone_number
        self.is_active=True 

    def __repr__(self):
        return '<Organizations %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "address1": self.address1,
            "address2": self.address2,
            "city": self.city,
            "state": self.state,
            "zipCode": self.zipCode,
            "phone_number": self.phone_number,
            "users": list(map(lambda x: x.serialize(), self.users))
            # do not serialize the password, its a security breach
        }

class Financials(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prospect_id = db.Column(db.Integer, unique=False)
    user_id = db.Column(db.Integer)
    statement_date = db.Column(db.Integer)
    quality = db.Column(db.Integer)
    fye_month = db.Column(db.Integer)
    fye_day = db.Column(db.Integer)
    prepared_by = db.Column(db.Integer)
    cash = db.Column(db.Numeric, unique=False, nullable=False)
    accounts_receivable = db.Column(db.Numeric, unique=False, nullable=False)
    raw_materials = db.Column(db.Numeric, unique=False, nullable=False)
    work_in_process = db.Column(db.Numeric, unique=False, nullable=False)
    finished_goods = db.Column(db.Numeric, unique=False, nullable=False)
    total_inventory = db.Column(db.Numeric, unique=False, nullable=False)
    land = db.Column(db.Numeric, unique=False, nullable=False)
    construction_in_progress = db.Column(db.Numeric, unique=False, nullable=False)
    buildings = db.Column(db.Numeric, unique=False, nullable=False)
    machines_and_equipment = db.Column(db.Numeric, unique=False, nullable=False)
    furniture_and_fixtures = db.Column(db.Numeric, unique=False, nullable=False)
    vehicles = db.Column(db.Numeric, unique=False, nullable=False)
    leashold_improvements = db.Column(db.Numeric, unique=False, nullable=False)
    capital_leases = db.Column(db.Numeric, unique=False, nullable=False)
    other_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_gross_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    accumulated_depreciation = db.Column(db.Numeric, unique=False, nullable=False)
    total_net_fixed_assets = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_assets = db.Column(db.Numeric, unique=False, nullable=False)
    goodwill = db.Column(db.Numeric, unique=False, nullable=False)
    other_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    total_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    accumulated_amortization = db.Column(db.Numeric, unique=False, nullable=False)
    net_intangibles = db.Column(db.Numeric, unique=False, nullable=False)
    other_non_operating_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_non_current_assets = db.Column(db.Numeric, unique=False, nullable=False)
    total_assets = db.Column(db.Numeric, unique=False, nullable=False)
    short_term_debt_secured = db.Column(db.Numeric, unique=False, nullable=False)
    short_term_debt_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    cpltd_secured = db.Column(db.Numeric, unique=False, nullable=False)
    cpltd_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    other_notes_payable = db.Column(db.Numeric, unique=False, nullable=False)
    accounts_payable_trade = db.Column(db.Numeric, unique=False, nullable=False)
    other_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    ltd_secured = db.Column(db.Numeric, unique=False, nullable=False)
    ltd_unsecured = db.Column(db.Numeric, unique=False, nullable=False)
    other_lt_notes_payable = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_liaibilities = db.Column(db.Numeric, unique=False, nullable=False)
    other_non_operating_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_non_current_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    total_liabilities = db.Column(db.Numeric, unique=False, nullable=False)
    common_stock = db.Column(db.Numeric, unique=False, nullable=False)
    additional_paid_in_capital = db.Column(db.Numeric, unique=False, nullable=False)
    retained_earnings = db.Column(db.Numeric, unique=False, nullable=False)
    total_equity = db.Column(db.Numeric, unique=False, nullable=False)
    tangible_net_worth = db.Column(db.Numeric, unique=False, nullable=False)
    working_capital = db.Column(db.Numeric, unique=False, nullable=False)
    current_ratio = db.Column(db.Numeric, unique=False, nullable=False)
    quick_ratio = db.Column(db.Numeric, unique=False, nullable=False)
    leverage = db.Column(db.Numeric, unique=False, nullable=False)
    total_revenue = db.Column(db.Numeric, unique=False, nullable=False)
    total_cogs = db.Column(db.Numeric, unique=False, nullable=False)
    gross_profit = db.Column(db.Numeric, unique=False, nullable=False)
    gpm = db.Column(db.Numeric, unique=False, nullable=False)
    sga_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    rent_expense = db.Column(db.Numeric, unique=False, nullable=False)
    depreciation_expense = db.Column(db.Numeric, unique=False, nullable=False)
    amortization_expense = db.Column(db.Numeric, unique=False, nullable=False)
    bad_debt_expense = db.Column(db.Numeric, unique=False, nullable=False)
    other_operating_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    total_operating_expenses = db.Column(db.Numeric, unique=False, nullable=False)
    total_operating_profit = db.Column(db.Numeric, unique=False, nullable=False)
    operating_profit_margin = db.Column(db.Numeric, unique=False, nullable=False)
    interest_expense = db.Column(db.Numeric, unique=False, nullable=False)
    interest_income = db.Column(db.Numeric, unique=False, nullable=False)
    other_non_operating_income_expense = db.Column(db.Numeric, unique=False, nullable=False)
    total_non_operating_income_expense = db.Column(db.Numeric, unique=False, nullable=False)
    total_profit_before_taxes = db.Column(db.Numeric, unique=False, nullable=False)
    tax_provision = db.Column(db.Numeric, unique=False, nullable=False)
    net_income = db.Column(db.Numeric, unique=False, nullable=False)
    distributions = db.Column(db.Numeric, unique=False, nullable=False)
    ebida = db.Column(db.Numeric, unique=False, nullable=False)
    ebitda = db.Column(db.Numeric, unique=False, nullable=False)
    ebitdar = db.Column(db.Numeric, unique=False, nullable=False)
    net_profit_margin = db.Column(db.Numeric, unique=False, nullable=False)
    roa = db.Column(db.Numeric, unique=False, nullable=False)
    roe = db.Column(db.Numeric, unique=False, nullable=False)

    def __init__(self,accounts):
        self.prospect_id = accounts["prospect_id"]
        self.user_id = accounts["user_id"]
        self.statement_date = accounts["statement_date"]
        self.quality = accounts["quality"]
        self.fye_month = accounts["fye_month"]
        self.fye_day = accounts["fye_day"]
        self.prepared_by = accounts["prepared_by"]
        self.cash = accounts["cash"]
        self.accounts_receivable = accounts["accounts_receivable"]
        self.raw_materials = accounts["raw_materials"]
        self.work_in_process = accounts["work_in_process"]
        self.finished_goods = accounts["finished_goods"]
        self.total_inventory = self.calculate_total_inventory(accounts["raw_materials"], accounts["work_in_process"], accounts["finished_goods"])
        self.land = accounts["land"]
        self.construction_in_progress = accounts["construction_in_progress"]
        self.buildings = accounts["buildings"]
        self.machines_and_equipment = accounts["machines_and_equipment"]
        self.furniture_and_fixtures = accounts["furniture_and_fixtures"]
        self.vehicles = accounts["vehicles"]
        self.leasehold_improvements = accounts["leasehold_improvements"]
        self.capital_leases = accounts["capital_leases"]
        self.other_fixed_assets = accounts["other_fixed_assets"]
        self.total_gross_fixed_assets = self.calculate_total_gross_fixed_assets(accounts["land"], accounts["construction_in_progress"], accounts["buildings"], accounts["machines_and_equipment"], accounts["furniture_and_fixtures"], accounts["vehicles"], accounts["leasehold_improvements"], accounts["capital_leases"], accounts["other_fixed_assets"])
        self.accumulated_depreciation = accounts["accumulated_depreciation"]
        self.net_fixed_assets = self.calculate_net_fixed_assets(accounts["total_gross_fixed_assets"], accounts["accumulated_depreciation"])
        self.other_operating_assets = accounts["other_operating_assets"]
        self.goodwill = accounts["goodwill"]
        self.other_intangibles = accounts["other_intangibles"]
        self.total_intangibles = self.calculate_total_intangibles(accounts["goodwill"], accounts["other_intanigbles"])
        self.accumulated_amortization = accounts["accumulated_amortization"]
        self.net_intangibles = self.calculate_net_intangibles(accounts["total_intangibles"], accounts["accumulated_amortization"])
        self.other_non_operating_assets = accounts["other_non_operating_assets"]
        self.total_non_current_assets = self.calculate_total_non_current_assets(accounts["net_fixed_assets"], accounts["other_operating_assets"], accounts["net_intangibles"], accounts["other_non_operating_assets"])
        self.total_assets = self.calculate_total_assets(accounts["total_current_assets"], accounts["total_non_current_assets"])
        self.short_term_debt_secured = accounts["short_term_debt_secured"]
        self.short_term_debt_unsecured = accounts["short_term_debt_unsecured"]
        self.cpltd_secured = accounts["cpltd_secured"]
        self.cpltd_unsecured = accounts["cpltd_unsecured"]
        self.other_notes_payable = accounts["other_notes_payable"]
        self.accounts_payable_trade = accounts["accounts_payable_trade"]
        self.other_current_liabilities = accounts["other_current_liabilities"]
        self.total_current_liaibilities = self.calculate_total_current_liabilities(accounts["short_term_debt_secured"], accounts["short_term_debt_unsecured"], accounts["cpltd_secured"], accounts["cpltd_unsecured"], accounts["other_notes_payable"], accounts["accounts_payable_trade"], accounts["other_current_liabilities"])
        self.ltd_secured = accounts["ltd_secured"]
        self.ltd_unsecured = accounts["ltd_unsecured"]
        self.other_lt_notes_payable = accounts["other_lt_notes_payable"]
        self.other_operating_liaibilities = accounts["other_operating_liabilities"]
        self.other_non_operating_liabilities = accounts["other_non_operating_liabilities"]
        self.total_non_current_liabilities = self.calculate_total_non_current_liabilities(accounts["ltd_secured"], accounts["ltd_unsecured"], accounts["other_lt_notes_payable"])
        self.total_liabilities = self.calculate_total_liabilities(accounts["total_current_liabilities"], accounts["total_non_current_liabilities"])
        self.common_stock = accounts["common_stock"]
        self.additional_paid_in_capital = accounts["additional_paid_in_capital"]
        self.retained_earnings = accounts["retained_earnings"]
        self.total_equity = self.calculate_total_equity(accounts["common_stock"], accounts["additional_paid_in_capital"], accounts["retained_earnings"])
        self.tangible_net_worth = self.calculate_tangible_net_worth(accounts["total_equity"], accounts["net_intangibles"])
        self.working_capital = self.calculate_working_capital(accounts["total_current_assets"], accounts["total_current_liabilities"])
        self.current_ratio = self.calculate_current_ratio(accounts["total_current_assets"], accounts["total_current_liabilities"])
        self.quick_ratio = self.calculate_quick_ratio(accounts["total_current_assets"], accounts["total_inventory"], accounts["total_current_liabilities"])
        self.leverage = self.calculate_leverage(accounts["total_liabilities"], accounts["total_equity"])
        self.total_revenue = accounts["total_revenue"]
        self.total_cogs = accounts["total_cogs"]
        self.gross_profit = self.calculate_gross_profit(accounts["total_revenue"], accounts["total_cogs"])
        self.gpm = self.calculate_gpm(accounts["gross_profit"], accounts["total_revenue"])
        self.sga_expenses = accounts["sga_expenses"]
        self.rent_expense = accounts["rent_expense"]
        self.depreciation_expense = accounts["depreciation_expense"]
        self.amortization_expense = accounts["amortization_expense"]
        self.bad_debt_expense = accounts["bad_debt_expense"]
        self.other_operating_expenses = accounts["other_operating_expenses"]
        self.total_operating_expenses = self.calculate_total_operating_expenses(accounts["sga_expenses"], accounts["rent_expense"], accounts["depreciation_expense"], accounts["amortization_expense"], accounts["bad_debt_expense"], accounts["other_operating_expenses"])
        self.total_operating_profit = self.calculate_total_operating_profit(accounts["gross_profit"], accounts["total_operating_expenses"])
        self.operating_profit_margin = self.calculate_operating_profit_margin(accounts["total_operating_profit"], accounts["total_revenue"])
        self.interest_expense = accounts["interest_expense"]
        self.interest_income = accounts["interest_income"]
        self.other_non_operating_income_expense = accounts["other_non_operating_income_expense"]
        self.total_non_operating_income_expense = self.calculate_total_non_operating_income_expense(accounts["interest_expense"], accounts["interest_income"], accounts["other_non_operating_income_expense"])
        self.total_profit_before_taxes = self.calculate_total_profit_before_taxes(accounts["total_operating_profit"], accounts["total_non_operating_income_expense"])
        self.tax_provision = accounts["tax_provision"]
        self.net_income = self.calculate_net_income(accounts["total_profit_before_taxes"], accounts["tax_provision"])
        self.net_profit_margin = self.calculate_net_profit_margin(accounts["net_income"], accounts["total_revenue"])
        self.distributions = accounts["distributions"]
        self.ebida = self.calculate_ebida(accounts["net_income"], accounts["interest_expense"], accounts["depreciation_expense"], accounts["amortization_expense"])
        self.ebitda = self.calculate_ebitda(accounts["net_income"], accounts["interest_expense"], accounts["tax_provision"], accounts["depreciation_expense"], accounts["amortization_expense"])
        self.ebitdar = self.calculate_ebitdar(accounts["net_income"], accounts["interest_expense"], accounts["tax_provision"], accounts["depreciation_expense"], accounts["amortization_expense"], accounts["rent_expense"])
        self.roa = self.calculate_roa(accounts["net_income"], accounts["total_assets"])
        self.roe = self.calculate_roe(accounts["net_income, total_equity"])

    def calculate_total_inventory (self, raw_materials, work_in_process, finished_goods):
        return raw_materials + work_in_process + finished_goods

    def calculate_total_gross_fixed_assets (self, land, construction_in_progress, buildings, machines_and_equipment, furniture_and_fixtures, vehicles, leasehold_improvements, capital_leases, other_fixed_assets):
        return land + construction_in_progress + buildings + machines_and_equipment + furniture_and_fixtures + vehicles + leasehold_improvements + capital_leases+ other_fixed_assets

    def calculate_net_fixed_assets (self, total_gross_fixed_assets, accumulated_depreciation):
        return total_gross_fixed_assets - accumulated_depreciation

    def calculate_total_intangibles (self, goodwill, other_intanigbles):
        return goodwill + other_intangibles

    def calculate_net_intangibles (self, total_intangibles, accumulated_amortization):
        return total_intangibles - accumulated_amortization

    def calculate_total_non_current_assets (self, net_fixed_assets, other_operating_assets, net_intangibles, other_non_operating_assets):
        return net_fixed_assets + other_operating_assets + net_intangibles + other_non_operating_assets

    def calculate_total_assets (self, total_current_assets, total_non_current_assets):
        return total_current_assets + total_non_current_assets

    def calculate_total_current_liabilities (self, short_term_debt_secured, short_term_debt_unsecured, cpltd_secured, cpltd_unsecured, other_notes_payable, accounts_payable_trade, other_current_liabilities):
        return short_term_debt_secured + short_term_debt_unsecured + cpltd_secured + cpltd_unsecured + other_notes_payable + accounts_payable_trade + other_current_liabilities

    def calculate_total_non_current_liabilities (self, ltd_secured, ltd_unsecured, other_lt_notes_payable):
        return ltd_secured + ltd_unsecured + other_lt_notes_payable
    
    def calculate_total_liabilities (self, total_current_liabilities, total_non_current_liabilities):
        return total_current_liabilities + total_non_current_liabilities

    def calculate_total_equity (self, common_stock, additional_paid_in_capital, retained_earnings):
        return common_stock + additional_paid_in_capital + retained_earnings

    def calculate_tangible_net_worth (self, total_equity, net_intangibles):
        return total_equity - net_intangibles

    def calculate_working_capital (self, total_current_assets, total_current_liabilities):
        return total_current_assets - total_current_liabilities
    
    def calculate_current_ratio (self, total_current_assets, total_current_liabilities):
        return total_current_assets / total_current_liabilities

    def calculate_quick_ratio (self, total_current_assets, total_inventory, total_current_liabilities):
        return (total_current_assets - total_inventory) / total_current_liabilities

    def calculate_leverage (self, total_liabilities, total_equity):
        return total_liabilities / total_equity
    
    def calculate_gross_profit (self, total_revenue,total_cogs):
        return total_revenue - total_cogs
        
    def calculate_gpm (self, gross_profit, total_revenue):
        return gross_profit / total_revenue

    def calculate_total_operating_expenses (self, sga_expenses, rent_expense, depreciation_expense, amortization_expense, bad_debt_expense, other_operating_expenses):
        return sga_expenses + rent_expense + depreciation_expense + amortization_expense + bad_debt_expense + other_operating_expenses

    def calculate_total_operating_profit (self, gross_profit, total_operating_expenses):
        return gross_profit - total_operating_expenses

    def calculate_operating_profit_margin (self, total_operating_profit, total_revenue):
        return total_operating_profit / total_revenue

    def calculate_total_non_operating_income_expense (self, interest_expense, interest_income, other_non_operating_income_expense):
        return interest_expense + interest_income + other_non_operating_income_expense

    def calculate_total_profit_before_taxes (self, total_operating_profit, total_non_operating_income_expense):
        return total_operating_profit - total_non_operating_income_expense

    def calculate_net_income (self, total_profit_before_taxes, tax_provision):
        return total_profit_before_taxes - tax_provision

    def calculate_net_profit_margin (self, net_income, total_revenue):
        return net_income / total_revenue

    def calculate_ebida (self, net_income, interest_expense, depreciation_expense, amortization_expense):
        return net_income + interest_expense + depreciation_expense + amortization_expense

    def calculate_editda (self, net_income, interest_expense, tax_provision, depreciation_expense, amortization_expense):
        return net_income + interest_expense + tax_provision + depreciation_expense + amortization_expense

    def calculate_ebitdar (self, net_income, interest_expense, depreciation_expense, amortization_expense, rent_expense):
        return net_income + interest_expense + tax_provision + depreciation_expense + amortization_expense + rent_expense
    
    def calculate_roa (self, net_income, total_assets):
        return net_income / total_assets

    def calculate_roe (self, net_income, total_equity):
        return net_income / total_equity

    def __repr__(self):
        return '<Financials %r>' % self.id
    
    def serialize(self):
        return {
            # do not serialize the password, its a security breach
            "prospect_id": self.prospect_id,
            "user_id": self.user_id,
            "statement_date": self.statement_date,
            "quality": self.quality,
            "fye_month": self.fye_month,
            "fye_day": self.fye_day,
            "prepared_by": self.prepared_by,
            "cash": self.cash,
            "accounts_receivable": self.accounts_receivable,
            "raw_materials": self.raw_materials,
            "work_in_process": self.work_in_process,
            "finished_goods": self.finished_goods,
            "total_inventory": self.total_inventory,
            "land": self.land,
            "construction_in_progress": self.construction_in_progress,
            "buildings": self.buildings,
            "machines_and_equipment": self.machines_and_equipment,
            "furniture_and_fixtures": self.furniture_and_fixtures,
            "vehicles": self.vehicles,
            "leasehold_improvements": self.leasehold_improvements,
            "capital_leases": self.capital_leases,
            "other_fixed_assets": self.other_fixed_assets,
            "total_gross_fixed_assets": self.total_gross_fixed_assets,
            "accumulated_depreciation": self.accumulated_depreciation,
            "net_fixed_assets": self.net_fixed_assets,
            "other_operating_assets": self.other_operating_assets,
            "goodwill": self.goodwill,
            "other_intangibles": self.other_intangibles,
            "total_intangibles": self.total_intangibles,
            "accumulated_amortization": self.accumulated_amortization,
            "net_intangibles": self.net_intangibles,
            "other_non_operating_assets": self.other_non_operating_assets,
            "total_non_current_assets": self.total_non_current_assets,
            "total_assets": self.total_assets,
            "short_term_debt_secured": self.short_term_debt_secured,
            "short_term_debt_unsecured": self.short_term_debt_unsecured,
            "cpltd_secured": self.cpltd_secured,
            "cpltd_unsecured": self.cpltd_unsecured,
            "other_notes_payable": self.other_notes_payable,
            "accounts_payable_trade": self.accounts_payable_trade,
            "other_current_liabilities": self.other_current_liabilities,
            "total_current_liaibilities": self.total_current_liaibilities,
            "ltd_secured": self.ltd_secured,
            "ltd_unsecured": self.ltd_unsecured,
            "other_lt_notes_payable": self.other_lt_notes_payable,
            "other_operating_liabilities": self.other_operating_liaibilities,
            "other_non_operating_liabilities": self.other_non_operating_liabilities,
            "total_non_current_liabilities": self.total_non_current_liabilities,
            "total_liabilities": self.total_liabilities,
            "common_stock": self.common_stock,
            "additional_paid_in_capital": self.additional_paid_in_capital,
            "retained_earnings": self.retained_earnings,
            "total_equity": self.total_equity,
            "tangible_net_worth": self.tangible_net_worth,
            "working_capital": self.working_capital,
            "current_ratio": self.current_ratio,
            "quick_ratio": self.quick_ratio,
            "leverage": self.leverage,
            "total_revenue": self.total_revenue,
            "total_cogs": self.total_cogs,
            "gross_profit": self.gross_profit,
            "gpm": self.gpm,
            "sga_expenses": self.sga_expenses,
            "rent_expense": self.rent_expense,
            "depreciation_expense": self.depreciation_expense,
            "amortization_expense": self.amortization_expense,
            "bad_debt_expense": self.bad_debt_expense,
            "other_operating_expenses": self.other_operating_expenses,
            "total_operating_expenses": self.total_operating_expenses,
            "total_operating_profit": self.total_operating_profit,
            "operating_profit_margin": self.operating_profit_margin,
            "interest_expense": self.interest_expense,
            "interest_income": self.interest_income,
            "other_non_operating_income_expense": self.other_non_operating_income_expense,
            "total_non_operating_income_expense": self.total_non_operating_income_expense,
            "total_profit_before_taxes": self.total_profit_before_taxes,
            "tax_provision": self.tax_provision,
            "net_income": self.net_income,
            "net_profit_margin": self.net_profit_margin,
            "distributions": self.distributions,
            "ebida": self.ebida,
            "ebitda": self.ebitda,
            "ebitdar": self.ebitdar,
            "roa": self.roa,
            "roe": self.roe
        }