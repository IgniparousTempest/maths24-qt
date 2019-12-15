.PHONY: init
init:
	python3.7 -m venv venv
	venv/bin/pip install -r requirements.txt
	# For making deb package
	venv/bin/pip install -r stdeb

.PHONY: ui
ui:
	pyuic5 maths24/maths24.ui -o maths24/maths24_ui.py

.PHONY: package_deb
package_deb:
	venv/bin/python setup.py --command-packages=stdeb.command bdist_deb
