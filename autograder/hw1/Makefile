ALL:=$(wildcard *)

autograder.zip: $(ALL)
	zip -r autograder.zip *

clean:
	rm -rf example/__pycache__ example/.pytest_cache tests/__pycache__ tests/.pytest_cache ./.pytest_cache 
