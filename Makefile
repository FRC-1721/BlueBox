# Shortcuts to do stuff

venv:
	mkdir -p bb_venv
	python -m venv bb_venv


# Setup the service
service:
	sudo ln bin/bluebox.service /etc/systemd/system/bluebox.service
	sudo systemctl daemon-reload
	sudo systemctl enable bluebox
	sudo systemctl restart bluebox

restart:
	sudo systemctl restart bluebox

stop:
	sudo systemctl stop bluebox
