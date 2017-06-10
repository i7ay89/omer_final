import sqlite3
from flask import *
from Table import Table
import reservations


conn = sqlite3.connect('db/afeka.db')
cur = conn.cursor()

app = Flask(__name__)


def init_tables(cursor):
    tables = []
    for row in cursor.execute('SELECT * FROM tables'):
        tables.append(Table(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    return tables


@app.route('/', methods=['GET'])
@app.route('/login', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/welcome', methods=['GET'])
def landing_page():
    return render_template('landing.html')


@app.route('/reservations', methods=['GET'])
def reservations_page():
    res_dict = reservations.create_reservations_dict(reservations.filter_reservations(cur,
                                                                                      table_id=request.args.get('table', None),
                                                                                      date=request.args.get('time', None),
                                                                                      name=request.args.get('name', None),
                                                                                      party=request.args.get('party', None)
                                                                                      ))
    return render_template('reservations.html', reservations=res_dict)


@app.route('/delete', methods=['GET'])
def delete_reservation():
    if reservations.delete_reservation(cur, reservation_id=request.args.get('id')):
        conn.commit()
        return redirect('/reservations')
    return 'ERROR!'


@app.route('/edit', methods=['GET'])
def edit_reservation():
    return 'Under Construction'


@app.route('/new_reservation', methods=['GET'])
def make_reservation():
    return render_template('reservation.html')


@app.route('/make_reservation', methods=['GET'])
def create_reservation():
    firstname = request.args.get('firstname', '')
    lastname = request.args.get('lastname', '')
    party = request.args.get('party', None)
    time = request.args.get('date')
    phone = request.args.get('phone', None)

    smoking = request.args.get('smoking', False)
    if smoking == '1' or smoking == 'on':
        smoking = True
    else:
        smoking = False

    bar = request.args.get('bar', False)
    if bar == '1' or bar == 'on':
        bar = True
    else:
        bar = False

    handicapped = request.args.get('handicapped', False)
    if handicapped == '1' or handicapped == 'on':
        handicapped = True
    else:
        handicapped = False

    outside = request.args.get('outside', False)
    if outside == '1' or outside == 'on':
        outside = True
    else:
        outside = False

    matching, alternatives = reservations.check_availability(cur, party_size=party, time=time,
                                                             smoking=smoking,
                                                             bar=bar,
                                                             handicapped=handicapped,
                                                             outside=outside)
    if matching:
        reservations.create_reservation(cur, party, time, matching[0], firstname + ' ' + lastname, phone)
        conn.commit()
        return redirect('/reservations')
    elif alternatives:
        alternatives = reservations.create_alternatives_dict(cur, alternatives, time, firstname, lastname, party, phone)
        return render_template('alternatives.html', alternatives=alternatives)
    else:
        return 'No matching tables'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
