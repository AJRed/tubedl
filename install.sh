

ENVPATH="env"


update_libs() {
	source $ENVPATH/bin/activate

	echo Installing dependencies.
	python -m pip install --requirement requirements.txt
	echo Installation complete.
}

create_venv() {
	echo Creating virtual environment using venv.
	python -m venv $ENVPATH
	update_libs
}

create_virtualenv() {
	echo Creating virtual environment using virtualenv.
	virtualenv $ENVPATH
	update_libs
}
if [[ $# = 0 ]]
then
	create_virtualenv
else
	if [[ "$1" = "-u" ]] || [[ "$1" = "--update" ]]
	then
		update_libs
	fi

fi

