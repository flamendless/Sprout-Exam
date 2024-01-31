CMD="/mnt/c/Windows/System32/cmd.exe"

run() {
	echo ${CMD};
	if ! command -v ${CMD} &> /dev/null; then
		echo "${CMD} not found"
		return
	fi

	PORT="7777"
	URL="http://127.0.0.1:${PORT}"
	${CMD} /c "start chrome ${URL}/docs" &

	poetry run uvicorn src.main:app --reload --port ${PORT}
}

analyze() {
	echo "Running: poetry run ruff check src/"
	poetry run ruff check src/
}

fix() {
	echo "Running: poetry run ruff check --fix src/"
	poetry run ruff check --fix src/
}

if [ "$#" -eq 0 ]; then
	echo "First use: chmod +x build.sh"
	echo "Usage: ./build.sh run | analyze | fix"
else
	"$1" "$@"
fi
