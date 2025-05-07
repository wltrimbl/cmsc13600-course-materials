
clean:
	-rm -Rf .pycache/* */.pycache */*/.pycache .pytest_cache */__pycache__ */*/__pycache__ __pycache__ 
	-rm -Rf app/migrations
	-rm -Rf $( find . -name '__pycache__' -type d) 

runserver:
	python manage.py runserver
