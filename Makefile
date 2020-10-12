build: requirements.txt
	@echo "--CREATING virtual enviroment venv--";
	@python3 -m venv venv;
	@echo "--INSTALLING dependencies--";
	@. venv/bin/activate; pip install -r requirements.txt;

run:
	@echo "--GETTING data from Spotify--";
	@. venv/bin/activate; python3 app/main.py;

clean:
	@echo "--DELETING venv and pycache--";
	@rm -r venv; find . | grep -E "(.cache|debug.log|.csv)" | xargs rm -rf;
	@find . | grep -E "(__pycache__|.pytest_cache)" | xargs rm -rf;