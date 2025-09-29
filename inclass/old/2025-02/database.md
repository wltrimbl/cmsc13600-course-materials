On the department server, you can find a file called 
/home/wltrimbl/136/sms-messages-2012.db.  It contains ~120 SMS messages that I received or sent in 2012-2013, 
in the format Apple stored its SMS messages at the time.  

0)  Copy the file to your laptop.  You should probably use SCP. (PuTTy/SCP on Windows)

1)  You can open the file with an SQLITE terminal (`sqlite3` on the commmand line usually works, if not you can install an sqlite terminal client) or with a graphical SQL browser (DB Browser is one such).  

It looks like this:

    $ sqlite3 sms-messages-2012.db 
    sqlite> .tables
    _SqliteDatabaseProperties  msg_group                
    group_member               msg_pieces               
    message   

    sqlite> SELECT * FROM message LIMIT 2;
    ROWID|address|date|text|flags|replace|svc_center|group_id|association_id|height|UIFlags|version|subject|country|headers|recipients|read
    9890|(206) 554-9250|1342525822|Yo nuff C whaddap wichu?|3|0||223|0|0|4|0||us|||1
    9894|+13608184000|1342531993|You've got a new voicemail from (630) 252-0097.Transcript: Unable to transcribe this message. |2|0||224|0|0|0|0||us|||0

    sqlite> SELECT * FROM msg_group LIMIT 2;
    ROWID|type|newest_message|unread_count|hash
    223|0|10130|0|87623215
    224|0|9894|0|-727840271

2)  A brief search-engine investigation for "date format apple sms db" turns up that the time format is number 
seconds since 1/01/2001 or something like that: 
https://stackoverflow.com/questions/10746562/parsing-date-field-of-iphone-sms-file-from-backup

The following SQL command turns the ten-digit times into dates between April 2012 and April 2013:
SELECT datetime(date + strftime('%S', '2001-01-01 00:00:00'), 'unixepoch', 'localtime') AS date, * FROM message;

We can put this in our table by first modifying the table schema, then setting the values of the new column:
ALTER table message ADD nicedate;
UPDATE message SET nicedate=datetime(date + strftime('%S', '2001-01-01 00:00:00'), 'unixepoch', 'localtime');

1) Write a command that evaluates the number of different addresses (in the addressbook) that the database has messages either from or to.

SELECT   __________  FROM message;


2)  Write a command that counts the number of messages attached to each contact in the addressbook.

SELECT   ___________________  FROM message;


3)  The `flags` field distinguishes between incoming and outgoing messages.  Outgoing texts have flags = 3, incoming texts have flags=2.
Write a command that counts the number of incoming and outgoing messages.


4) The `msg_group` identifies the most recent message from each contact.  Write an expression that joins this with messages (to show the message group id for the newest message).

