# These build to-do lists from a directory listing of PDF files.
PDFS = $(wildcard *.pdf)
TEXT = $(subst .pdf,.txt,$(PDFS))
JSON = $(subst .txt,.json,$(TEXT))

# This is the default target, extract text from all the PDFs.
text: $(TEXT)

json: $(JSON) 

# recipe for running data extractor 
%.json:  %.txt   extract1.py 
	extract1.py $< | jq . >  $@

# recipe for turning pdfs into extracted-text 
%.txt:  %.pdf 
	pdftotext -layout $< $@

# If I tire of typing python manage.py runserver, I can type "make run"
run:
	python manage.py runserver

# If I tire of typing these commands, "make clean"
clean:
	rm db.sqlite3
	python manage.py makemigrations
	python manage.py migrate


