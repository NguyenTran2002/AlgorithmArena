# Function to determine the operating system
run_by_OS() {
    if [ "$(uname)" == "Darwin" ]; then
        open "http://localhost:2828"  # macOS command
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
        xdg-open "http://localhost:2828"  # Linux command
    else
        echo "Consult ReadMe for Instruction on Windows."
    fi
}

# Start the Docker services in detached mode
docker-compose up --build -d

# Wait for a brief moment for the containers to initialize
sleep 2

$(run_by_OS)