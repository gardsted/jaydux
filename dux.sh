run(){
pushd $(dirname $0)
. venv/bin/activate
python -m jaydux
}

run
