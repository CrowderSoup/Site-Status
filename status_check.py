# Imports
import requests
import smtplib

from email.mime.text import MIMEText

# Get our variables ready
COMMASPACE = ', '
me = 'FROM-ADDRESS/USERNAME'
password = 'USER-PASSWORD'

with open("emails.txt","U") as e_file, open("sites.txt","U") as s_file:
    sites = e_file.read().split('\n')
    emails = s_file.read().split('\n')

# Loop over the sites
for site in sites:
    print 'Checking to make sure %s is still up... ' % (site)
    
    r = requests.get(site)
    
    if(r.status_code != requests.codes.ok):
        print 'Site is not Ok!'
        
        msg = MIMEText('The site %s is down!' % (site))
        msg['Subject'] = 'Site is down!'
        
        msg['From'] = me
        msg['To'] = COMMASPACE.join(emails)
        
        # Send the message via GMail
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()  
        server.login(me, password)
        server.sendmail(me, emails, msg.as_string())
        server.quit()
    else:
        print 'Site is Ok!'
    #end if
#end for