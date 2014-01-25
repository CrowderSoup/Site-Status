# Imports
import sys, getopt, datetime, pymongo, smtplib, requests, bcrypt, pprint

from pymongo import MongoClient, ASCENDING, DESCENDING
from email.mime.text import MIMEText
from bson.objectid import ObjectId
from ConfigParser import SafeConfigParser

def insert_site(sites):
    name = raw_input('Site Name: ')
    url = raw_input('Site Url: ')

    site_id = sites.insert({
        'name': name,
        'url': url
        })

    return site_id

def insert_user(users):
    name = raw_input('Username: ')
    email = raw_input('Email address: ')
    password = raw_input('Password: ')
    password2 = raw_input('Again: ')

    if password != password2:
        print "Passwords did not match, aborting."
        print password
        print password2
        return 0;

    user_id = users.insert({
        'name': name,
        'email': email,
        'password': bcrypt.hashpw(password, bcrypt.gensalt())
        })

    return user_id

def check(sites, status, users, email):
    stats = []

    for site in sites.find():
        try:
            r = requests.get(site['url'])

            headers = {}
            for header in r.headers:
                headers[header] = r.headers[header]

            stat = {
                'site': site,
                'code': r.status_code,
                'headers': headers,
                'time': datetime.datetime.now().isoformat()
            }
        except:
            print "There was an error, assuming {0} is down".format(site.name)
        finally:
            stats.append(stat)

    for stat in stats:
        if(stat['code'] is not 200):
            email_users(users, stat, email)
    return status.insert(stats)

def last_check(sites, status):
    for stat in status.find().sort("_id", DESCENDING).limit(sites.count()):
        pprint.pprint(stat)

def email_users(users, stat, email):
    for user in users.find():
        message = "{0} is down!".format(stat['site']['name'])
        msg = MIMEText(message)
        msg['Subject'] = message

        msg['From'] = 'aaron@aaroncrowder.com'
        msg['To'] = user['email']

        # Send the message via SMTP Mail server
        server = smtplib.SMTP_SSL(email['server'], email['port'])
        server.login(email['user'], email['password'])
        server.sendmail(email['user'], user['email'], msg.as_string())
        server.quit()

def main(argv):
    # Get everything we need
    parser = SafeConfigParser()
    parser.read('settings.ini')

    # Mongo Settings
    mongo_server = parser.get('mongo_settings', 'server')
    mongo_user = parser.get('mongo_settings', 'user')
    mongo_password = parser.get('mongo_settings', 'password')
    mongo_source = parser.get('mongo_settings', 'source')

    # Email Settings
    email = {}
    email['user'] = parser.get('email_settings', 'user')
    email['password'] = parser.get('email_settings', 'password')
    email['server'] = parser.get('email_settings', 'server')
    email['port'] = parser.get('email_settings', 'port')

    client = MongoClient(mongo_server)
    authenticated = client.status_check.authenticate(
            mongo_user, mongo_password, source=mongo_source)

    if authenticated:
        db = client.status_check
        sites = db.sites
        status = db.status
        users = db.users

        if argv and argv[0] == 'insert' and argv[1] == '-s':
            site_id = insert_site(sites)
            print "You just inserted a new site, it's Id is", site_id
        elif argv and argv[0] == 'insert' and argv[1] == '-u':
            user_id = insert_user(users)
            print "You just inserted a new user, it's Id is", user_id
        elif argv and argv[0] == 'check':
            print "Checking sites..."
            check(sites, status, users, email)
            print "Finished checking sites!"
        else:
            last_check(sites, status)
    else:
        print "Could not authenticate."

if __name__ == "__main__":
    main(sys.argv[1:])
