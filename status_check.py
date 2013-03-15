# Imports
import requests
import smtplib
import MySQLdb as mdb
import sys

from email.mime.text import MIMEText

# Define our functions
def sendErrorMessages(emails, sitesDown, user, password):
    msg = MIMEText('These sites are down:\n %s' % ('\n'.join(sitesDown)))
    msg['Subject'] = 'Sites are down!'
    
    msg['From'] = user
    msg['To'] = ', '.join(emails[0])
    
    # Send the message via GMail
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()  
    server.login(user, password)
    server.sendmail(user, emails, msg.as_string())
    server.quit()
#end sendErrorMessages

def createConnection(server, username, password, database):
    con = None
    
    try:
        con = mdb.connect(server, username, password, database)
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)
    #end try/except
    
    return con
#end createConnection

def closeConnection(con):
    if(con):
        con.close()
    #end if
#end closeConnection

def queryDatabase(con, query):
    cur = con.cursor()
    cur.execute(query)
    
    return cur.fetchall()
#end queryDatabase

# Create connection to MySQL Server
con = createConnection('localhost', 'DBUSER', 'DBPASSWORD', 'DB')
if not(con):
    sys.exit(1)
#end if

# Get our variables ready
user = queryDatabase(con, 
    """
    SELECT 
        settingValue 
    FROM 
        siteSettings 
    WHERE 
        settingName = 'email_user'
    """)[0][0]
password = queryDatabase(con, 
    """
    SELECT 
        settingValue 
    FROM 
        siteSettings 
    WHERE 
        settingName = 'email_password'
    """)[0][0]

sitesDown = []
sites = queryDatabase(con, "SELECT * FROM websites")
emails = queryDatabase(con, "SELECT email FROM users WHERE fk_roleid = 1")

# Loop over the sites
for site in sites:
    print 'Checking %s ... ' % (site[1])
    status = 0
    try:
        r = requests.get(site[2])
        
        if(r.status_code != requests.codes.ok):
            sitesDown.append(site[1])
        else:
            status = 1
        #end if
    except:
        print 'There was an error, assuming site is down.'
        sitesDown.append(site[1])
    finally:
        if(status):
            print 'Site is ok!'
        else:
            print 'Site is not ok!'
        #end if
        
        queryDatabase(con, 
            """
            INSERT
            INTO websitesChecked(fkid_website, status)
            VALUES(%d, %d)
            """ % (int(site[0]), status))
        
        con.commit()
    #end try/except
#end for

if(len(sitesDown) > 0):
    sendErrorMessages(emails, sitesDown, user, password)
else:
    print 'All sites where up! Good work!'
#end if

# Close connection to MySQL Server
closeConnection(con)