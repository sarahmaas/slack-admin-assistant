VENV?=venv
PYTHON?=$(shell which python3.7)

.PHONY: run venv remove-venv rebuild-venv clean

run: venv
	$(VENV)/bin/python app.py

venv: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	$(VENV)/bin/pip install -Ur requirements.txt
	touch $(VENV)/bin/activate

remove-venv:
	rm -rf $(VENV)

rebuild-venv: remove-venv venv

lint: venv
	$(VENV)/bin/flake8 --config flake8.cfg

clean: remove-venv
