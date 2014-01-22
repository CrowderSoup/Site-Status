# Imports
import sys, getopt, datetime, pymongo, smtplib, requests, pprint

from pymongo import MongoClient, ASCENDING, DESCENDING
from email.mime.text import MIMEText
from bson.objectid import ObjectId

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

    user_id = users.insert({
        'name': name,
        'email': email
        })

    return user_id

def check(sites, status, users):
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
            email_users(users, stat)
    return status.insert(stats)

def last_check(sites, status):
    for stat in status.find().sort("_id", DESCENDING).limit(sites.count()):
        pprint.pprint(stat)

def email_users(users, stat):
    email = {}
    email['user'] = "aaron@aaroncrowder.com"
    email['password'] = "Dumbl#d0re"
    email['server'] = "smtp.crowderfam.org"
    email['port'] = "465"

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
    client = MongoClient()
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
        check(sites, status, users)
        print "Finished checking sites!"
    else:
        last_check(sites, status)

if __name__ == "__main__":
    main(sys.argv[1:])