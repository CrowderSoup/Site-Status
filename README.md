# Site Status

This simple script checks to make sure that all the sites you have listed in
your database are returning 200, 'ok' messages. If one isn't, you will be 
emailed at the addresses listed for users that are set to the 'admin' role.

The database being used for this application is actually in production, which
is why I have a users and roles table in the first place. You can modify how
this script works any way you like, but to get you going I have included the
create statements you'll need below:

```sql
CREATE TABLE IF NOT EXISTS `roles` (
  `pk_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(55) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`pk_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

CREATE TABLE IF NOT EXISTS `siteSettings` (
  `settingName` varchar(255) NOT NULL,
  `settingValue` varchar(255) NOT NULL,
  UNIQUE KEY `settingName` (`settingName`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `users` (
  `pkid` int(11) NOT NULL AUTO_INCREMENT,
  `fName` varchar(55) NOT NULL DEFAULT '',
  `lName` varchar(55) NOT NULL DEFAULT '',
  `uName` varchar(55) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `salt` varchar(255) NOT NULL,
  `jsonSettings` text,
  `fk_roleid` int(11) NOT NULL DEFAULT '5',
  PRIMARY KEY (`pkid`),
  UNIQUE KEY `uName` (`uName`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 COMMENT='latin1_swedish_ci' AUTO_INCREMENT=2 ;

CREATE TABLE IF NOT EXISTS `websites` (
  `pkid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  PRIMARY KEY (`pkid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;

CREATE TABLE IF NOT EXISTS `websitesChecked` (
  `pkid` int(11) NOT NULL AUTO_INCREMENT,
  `fkid_website` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL,
  PRIMARY KEY (`pkid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=78 ;
```