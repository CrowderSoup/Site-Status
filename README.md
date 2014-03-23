# Site Status

## Current Status

I am currently working on adding a web based front-end to this project using 
Flask. This project has been built with Python 3.4 in mind, and will probably 
have issues if you try to run it on an older version of Python.

<hr/>

This simple script checks to make sure that all the sites you have listed in
your database are returning 200, 'ok' messages. If one isn't, you will be 
emailed at the addresses listed for each user.

This project uses MongoDB. Mongo is perfect for non-relational data, like a log.
This also makes this script much more light weight.

To get started add a few sites like so:

```
python status_check.py insert -s
```

And a user or two:

```
python status_check.py insert -u
```

After which you can run Status Check:

```
python status_check.py check
```

For fun you can also run the script without any arguments to see the stats from 
the last check.