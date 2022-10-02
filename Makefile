
default: run-streamlit

run-streamlit:
	export $(cat .env | xargs) && streamlit run app.py

install-requirements:
	pip install -r requirements.txt

save-requirements:
	pip freeze > requirements.txt
