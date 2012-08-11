Extract newest sql stuff from trac (web interface and db),
I use the phpmyadmin account
```sql
SELECT ticket, time, author, newvalue FROM ticket_change
  WHERE field='comment' AND newvalue AND time > FILL-IN-DATE-HERE
	ORDER BY time DESC
```
Click export, export as csv, save as updated-comments.csv with these options:
```
	terminated by ,
	enclosed by '
	escaped by \
	AUTO NULL
	no no
```
Process the resulting file in e.g. vim as you need ( `%s,\\','',g` )

Append the file to comments.csv ( `cat updated-comments.csv >> comments.csv` )

`python2 convert.py`

If there is any output besides a list of tickets, check that malformed row in csv

Probably missed some sort of escaping or the replacement algorithm went really wild

When everything looks good:

`tar -czf unknown-horizons.tar.gz unknown-horizons/`

And bother a poor github admin once more!