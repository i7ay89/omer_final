from datetime import timedelta, datetime


def bool_to_str(value):
    if value:
        return 1
    return 0


def check_availability(cursor, party_size, time, smoking=False, outside=False, bar=False, handicapped=False):
    cursor.execute('''SELECT ID FROM tables WHERE smoking={} AND outdoor={} AND
                      bar={} AND handicapped={} AND capacity<={} + 2 AND capacity >= {}'''.format(bool_to_str(smoking),
                                                                                                  bool_to_str(outside),
                                                                                                  bool_to_str(bar),
                                                                                                  bool_to_str(handicapped),
                                                                                                  party_size,
                                                                                                  party_size))
    matching_tables = [tup[0] for tup in cursor.fetchall()]

    cursor.execute('''SELECT ID FROM tables WHERE capacity<={0} + 2 AND capacity >= {0}'''.format(party_size,
                                                                                                  party_size))
    alternatives = [tup[0] for tup in cursor.fetchall()]
    alternatives = [table for table in alternatives if table not in matching_tables]

    cursor.execute("""SELECT table_id FROM reservations WHERE from_time<='{}' AND until_time>'{}'""".format(time,
                                                                                                             time))
    occupied_tables = [tup[0] for tup in cursor.fetchall()]

    matching_tables = [table for table in matching_tables if table not in occupied_tables]
    alternatives = [table for table in alternatives if table not in occupied_tables]

    return matching_tables, alternatives


def filter_reservations(cursor, table_id=None, date=None, party=None, name=None, from_time=None, until_time=None):
    query = """SELECT * FROM reservations WHERE 1=1 """
    if table_id:
        query += """AND table_id={} """.format(table_id)
    if date:
        if from_time and until_time:
            from_time = date + ' ' + from_time
            until_time = date + ' ' + until_time
        else:
            from_time = date + ' 00:00:00'
            until_time = date + '23:59:59'
        query += """AND from_time<='{}' AND until_time>='{}' """.format(from_time, until_time)
    if name:
        query += """AND name='{}' """.format(name)
    if party:
        query += """AND party={} """.format(party)

    cursor.execute(query)
    reservations = cursor.fetchall()
    return reservations


def create_reservations_dict(reservations):
    reservations_dict = []
    for reservation in reservations:
        reservations_dict.append({'reservation_id': reservation[5],
                                  'table_id': reservation[0],
                                  'time': reservation[1],
                                  'name': reservation[3],
                                  'party': reservation[4],
                                  'phone': reservation[6]})
    return reservations_dict


def delete_reservation(cursor, reservation_id):
    try:
        cursor.execute("""DELETE FROM reservations WHERE reservation_id={}""".format(reservation_id))
    except:
        return False
    return True


def create_reservation(cursor, party_size, time, table_id, name, phone):
    time = time.replace('T', ' ')
    from_time = time
    until_time = str(datetime.strptime(time, "%Y-%m-%d %H:%M") + timedelta(hours=2))
    try:
        cursor.execute("""INSERT INTO reservations (table_id, from_time, until_time, name, party, phone) VALUES ({}, '{}', '{}', '{}', {}, {})""".format(table_id, from_time,
                                                                                           until_time, name,
                                                                                           party_size, phone))
        return True
    except:
        return False


def create_alternatives_dict(cursor, alternatives, time, firstname, lastname, party, phone):
    alternatives_dict = []
    for alternative in alternatives:
        alternative_table = cursor.execute("""SELECT * FROM tables WHERE ID={}""".format(alternative)).fetchone()
        alternatives_dict.append(
        {'table_id': alternative,
         'firstname': firstname,
         'lastname': lastname,
         'time': time,
         'party': party,
         'phone': phone,
         'capacity': alternative_table[1],
         'smoking': alternative_table[2],
         'outside': alternative_table[3],
         'bar': alternative_table[4],
         'handicapped': alternative_table[6]
         })

    return alternatives_dict
