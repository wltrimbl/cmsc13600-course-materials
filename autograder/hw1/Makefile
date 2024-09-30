ALL:=$(wildcard *)

autograder.zip: $(ALL)
	-mv randhead.py randhead-ans.py
	zip -r autograder.zip *
	-mv randhead-ans.py randheads.py

clean:
	rm -rf example/__pycache__ example/.pytest_cache tests/__pycache__ tests/.pytest_cache ./.pytest_cache 
