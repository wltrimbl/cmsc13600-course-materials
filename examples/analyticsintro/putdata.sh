curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438019", "title": "Pokemon: The Novel", "author": "Nintendo", "year": 2009}' http://127.0.0.1:8000/tasks/addBook
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9119292100211", "title": "Romeo and Juliet", "author": "William Shakespeare", "year": 1597}' http://127.0.0.1:8000/tasks/addBook
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438020", "title": "Pokemon: The Novel (Japanese)", "author": "Nintendo", "year": 2009}' http://127.0.0.1:8000/tasks/addBook
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "1122921122112", "title": "Databases", "author": "Raghu Ramakrishnan", "year": 2004}' http://127.0.0.1:8000/tasks/addBook
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "1122331221452", "title": "Mathematical Analysis", "author": "William Persson", "year": 2019}' http://127.0.0.1:8000/tasks/addBook

curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438019", "qty": 5}' http://127.0.0.1:8000/tasks/addInv
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9119292100211", "qty": 1}' http://127.0.0.1:8000/tasks/addInv
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "9781497438020", "qty": 6}' http://127.0.0.1:8000/tasks/addInv
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "1122921122112", "qty": 10}' http://127.0.0.1:8000/tasks/addInv
curl -i -X POST -H 'Content-Type: application/json' -d '{"isbn": "1122331221452", "qty": 4}' http://127.0.0.1:8000/tasks/addInv