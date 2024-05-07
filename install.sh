

ENVPATH="env"


create_venv() {
	echo Creating virtual environment using venv.
	python -m venv $ENVPATH

	source $ENVPATH/bin/activate

	echo Installing dependencies.
	python -m pip install --requirement requirements.txt
	echo Installation complete.
}

create_virtualenv() {
	echo Creating virtual environment using virtualenv.
	virtualenv $ENVPATH

	source $ENVPATH/bin/activate

	echo Installing dependencies.
	python -m pip install --requirement requirements.txt
	echo Installation complete.
}


create_virtualenv

