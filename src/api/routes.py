"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_admin.contrib.sqla import ModelView
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
# from datetime import date, time, datetime
from models import db, User, Prospects, Contacts, Organizations, Financials
from flask_jwt_simple import (JWTManager, jwt_required, create_jwt, get_jwt_identity)
from passlib.hash import sha256_crypt


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = "jd"
jwt = JWTManager(app)

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg" : "Missing JSON info request"}),400

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)

    if not email:
        return jsonify({"msg" : "Missing email parameter"}),400

    if not password:
        return jsonify({"msg" : "Missing password parameter"}),400

    specific_user = User.query.filter_by(
        email=email
    ).one_or_none()

    if isinstance(specific_user,User):
        if sha256_crypt.verify(password, specific_user.password):
            response={
                "jwt" : create_jwt(identity=specific_user.id),
                "user_id": specific_user.id
            }
            return jsonify(response),200 
        else:
            return jsonify({"msg" : "Wrong Password"}),400

    else:
        return jsonify({"msg" : "User not found"}),400


@app.route('/signup', methods=['POST'])
def handle_signup():
    
    input_data = request.json

    params = request.get_json()
    email = params.get('email', None)
    password = params.get('password', None)
    first_name = params.get('first_name', None)
    last_name = params.get('last_name', None)
    phone_number = params.get('phone_number', None)
    organization_id = params.get('organization_id', None)

    if not email:
        return jsonify({"msg" : "Missing email"}),400

    if not password:
        return jsonify({"msg" : "Missing password"}),400
    
    if not first_name:
        return jsonify({"msg" : "Missing first name"}),400
    
    if not last_name:
        return jsonify({"msg" : "Missing last name"}),400
    
    if not phone_number:
        return jsonify({"msg" : "Missing phone number"}),400

    

    # if 'email' in input_data and 'password' in input_data and 'first_name' in input_data and 'last_name' in input_data and 'phone_number' in input_data and 'organization_id' in input_data:

    specific_user = User.query.filter_by(
        email=input_data['email']
    ).one_or_none()

    organization = Organizations.query.get(input_data['organization_id'])


    if isinstance(specific_user,User):
        return jsonify({"msg" : "Email already in use"}),400
    else:
        new_user= User(
            email = input_data['email'],
            password = sha256_crypt.encrypt(str(input_data['password'])),
            first_name = input_data['first_name'],
            last_name = input_data['last_name'],
            phone_number = input_data['phone_number']
        )
        organization.users.append(new_user)
        db.session.add(new_user)
        try:
            db.session.commit()
            response={
                "jwt" : create_jwt(identity=new_user.id),
                "user_id": new_user.id
            }
            return jsonify(response),200

        except Exception as error:
            db.session.rollback()
            return jsonify({"msg" : error}),500

@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    specific_user_id = get_jwt_identity()
    specific_user = User.query.filter_by(
        id = specific_user_id
        ).one_or_none()

    if specific_user is None:
        return jsonify({"msg" : "user not found"}),404

    else:
        return jsonify(specific_user.serialize()),200

@app.route('/addProspect', methods=['POST'])
def add_prospect():
    input_data = request.json 
    user_id = input_data['user_id']

    new_prospect= Prospects(
        name = input_data['name'],
        industry = input_data['industry'],
        address1 = input_data['address1'],
        city = input_data['city'],
        state = input_data['state'],
        zipCode = input_data['zipCode'],
        phone_number = input_data['phone_number'],
        account = input_data['account']
    )

    user = User.query.filter_by(
        id=user_id
    ).one_or_none()    

    specific_prospect = Prospects.query.filter_by(
        account=input_data['account']
    ).one_or_none()

    if isinstance(specific_prospect,Prospects):
        prospect_id = specific_prospect.id
        prospects_query = User.query.filter(User.userprospects.any(id=prospect_id)).filter(Prospects.prospectsuser.any(id=user_id)).all()
        prospects_list = list(filter(lambda each: each.id==user_id, prospects_query))
        if not prospects_list:
            specific_prospect.prospectsuser.append(user)
            db.session.commit() 
            return jsonify(input_data),200
        else:
            return jsonify({"msg" : "prospect already created"}),400
    else:   
        db.session.add(new_prospect)
        user.userprospects.append(new_prospect)
        db.session.commit()             
        return jsonify(input_data),200

@app.route('/prospects/<int:user_id>', methods=['GET'])
def get_all_prospects(user_id):
        prospects_query = Prospects.query.filter(Prospects.prospectsuser.any(id=user_id)).all()
        prospects_list = list(map(lambda each: each.serialize(), prospects_query))
        return jsonify(prospects_list), 200


@app.route('/addContact', methods=['POST'])
def addContact():
    input_data = request.json

    prospect_account = Prospects.query.filter_by(
        account=input_data['account']
    ).one_or_none()

    specific_contact = Contacts.query.filter_by(
        first_name=input_data['first_name'],
        last_name=input_data['last_name']
    ).one_or_none()

    if isinstance(specific_contact,Contacts):
        return jsonify({"msg" : "contact already created"}),400
    else:
        new_contact= Contacts(
            first_name = input_data['first_name'],
            last_name = input_data['last_name'],
            position = input_data['position'],
            title = input_data['title'],
            email = input_data['email'],
            phone_number = input_data['phone_number']
        )
        db.session.add(new_contact)
        new_contact.prospectscontacts.append(prospect_account)
        db.session.commit()            
        return jsonify(input_data),200

@app.route('/contacts', methods=['GET'])
def get_all_contacts():
        contacts_query = Contacts.query.all()
        # contacts_query = Contacts.query.filter(Contacts.prospectscontacts.any(id=user_id)).all()
        contacts_list = list(map(lambda each: each.serialize(), contacts_query))
        return jsonify(contacts_list), 200

@app.route('/organizations', methods=['GET'])
def get_all_organizations():
        contacts_query = Organizations.query.all()
        organizations_list = list(map(lambda each: each.serialize(), contacts_query))
        return jsonify(organizations_list), 200

@app.route('/financials', methods=['POST'])
def save_financials():
    input_data = request.json
    input_data['user_id'] = get_jwt_identity()

    if 'cash' not in input_data:
        input_data['cash'] = 0

    if 'accounts_receivable' not in input_data:
        input_data['accounts_receivable'] = 0

    if 'raw_materials' not in input_data:
        input_data['raw_materials'] = 0

    if 'work_in_process' not in input_data:
        input_data['work_in_process'] = 0

    if 'finished_goods' not in input_data:
        input_data['finished_goods'] = 0

    if 'land' not in input_data:
        input_data['land'] = 0
    
    if 'construction_in_progress' not in input_data:
        input_data['construction_in_progress'] = 0

    if 'buildings' not in input_data:
        input_data['buildings'] = 0

    if 'machines_and_equipment' not in input_data:
        input_data['machines_and_equipment'] = 0

    if 'furniture_and_fixtures' not in input_data:
        input_data['furniture_and_fixtures'] = 0
    
    if 'vehicles' not in input_data:
        input_data['vehicles'] = 0

    if 'leasehold_improvements' not in input_data:
        input_data['leasehold_improvements'] = 0

    if 'capital_leases' not in input_data:
        input_data['capital_leases'] = 0

    if 'other_fixed_assets' not in input_data:
        input_data['other_fixed_assets'] = 0
    
    if 'accumulated_depreciation' not in input_data:
        input_data['accumulated_depreciation'] = 0

    if 'other_operating_assets' not in input_data:
        input_data['other_operating_assets'] = 0

    if 'goodwill' not in input_data:
        input_data['goodwill'] = 0

    if 'other_intangibles' not in input_data:
        input_data['other_intangibles'] = 0
    
    if 'accumulated_amortization' not in input_data:
        input_data['accumulated_amortization'] = 0

    if 'other_non_operating_assets' not in input_data:
        input_data['other_non_operating_assets'] = 0
    
    if 'short_term_debt_secured' not in input_data:
        input_data['short_term_debt_secured'] = 0

    if 'short_term_debt_unsecured' not in input_data:
        input_data['short_term_debt_unsecured'] = 0

    if 'cpltd_secured' not in input_data:
        input_data['cpltd_secured'] = 0

    if 'cpltd_unsecured' not in input_data:
        input_data['cpltd_unsecured'] = 0
    
    if 'other_notes_payable' not in input_data:
        input_data['other_notes_payable'] = 0

    if 'accounts_payable_trade' not in input_data:
        input_data['accounts_payable_trade'] = 0 

    if 'other_current_liabilities' not in input_data:
        input_data['other_current_liabilities'] = 0

    if 'ltd_secured' not in input_data:
        input_data['ltd_secured'] = 0

    if 'ltd_unsecured' not in input_data:
        input_data['ltd_unsecured'] = 0

    if 'other_lt_notes_payable' not in input_data:
        input_data['other_lt_notes_payable'] = 0
    
    if 'other_operating_liabilities' not in input_data:
        input_data['other_operating_liabilities'] = 0

    if 'other_non_operating_liabilities' not in input_data:
        input_data['other_non_operating_liabilities'] = 0
    
    if 'common_stock' not in input_data:
        input_data['common_stock'] = 0

    if 'additional_paid_in_capital' not in input_data:
        input_data['additional_paid_in_capital'] = 0

    if 'retained_earnings' not in input_data:
        input_data['retained_earnings'] = 0

    if 'total_revenue' not in input_data:
        input_data['total_revenue'] = 0
    
    if 'total_cogs' not in input_data:
        input_data['total_cogs'] = 0

    if 'sga_expenses' not in input_data:
        input_data['sga_expenses'] = 0 

    if 'rent_expense' not in input_data:
        input_data['rent_expense'] = 0

    if 'depreciation_expense' not in input_data:
        input_data['depreciation_expense'] = 0

    if 'amortization_expense' not in input_data:
        input_data['amortization_expense'] = 0
    
    if 'bad_debt_expense' not in input_data:
        input_data['bad_debt_expense'] = 0

    if 'other_operating_expenses' not in input_data:
        input_data['other_operating_expenses'] = 0 

    if 'interest_expense' not in input_data:
        input_data['interest_expense'] = 0

    if 'interest_income' not in input_data:
        input_data['interest_income'] = 0

    if 'other_non_operating_income_expense' not in input_data:
        input_data['other_non_operating_income_expense'] = 0
    
    if 'tax_provision' not in input_data:
        input_data['tax_provision'] = 0

    if 'distributions' not in input_data:
        input_data['distributions'] = 0

    if 'statement_date' in input_data and 'quality' in input_data and 'fye_month' in input_data and 'fye_day' in input_data and 'prepared_by' in input_data:
        new_financial = Financials( accounts=input_data )
        db.session.add(new_financial)
        # You will have to format the following code accordingly
        try:
            db.session.commit()
            # the response dictionary needs to be worked - maybe serialize the values of new_financial to give the values they want?

            response={
                'financial' : new_financial.serialize()
            }
            return jsonify(response),200

        except Exception as error:
            db.session.rollback()
            # don't forget to set the error value
            return jsonify({"msg" : error}),500
    else:
        return jsonify({"msg" : "information required missing"}),400    
    
    # Do Validation
    # Make sure to check all required columns are set
    # look at line 80
    # And make sure you assign user_id to input_data['user_id']

@app.route('/financials', methods=['GET'])
def getStatements():
    statement_query = Financials.query.all()
    all_statements = list(map(lambda x: x.serialize(), statement_query))
    return jsonify(all_statements), 200


@app.route('/financials/<int:id>', methods=['DELETE'])
def deleteStatement(id):
    statement = Financials.query.get(id)
    if statement is None:
        raise APIException('Statement not found', status_code=404)
    db.session.delete(statement)
    db.session.commit()
    return "ok", 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)