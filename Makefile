create_venv:
	python3 -m venv .venv
activate_venv:
	source .venv/bin/activate
isntall_deps:
	pip install -r requirements.txt
freeze:
	python -m pip freeze
update_req:
	python -m pip freeze > requirements.txt

	