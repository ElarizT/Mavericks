PORT ?= 8080

up:
	docker compose up --build

build:
	docker compose build

remote:
	@echo "Using port $(PORT)"
	@if ! command -v ngrok >/dev/null 2>&1; then \
		echo "ngrok not found. Installing..."; \
		if [ "$$(uname)" = "Darwin" ]; then \
			brew install ngrok; \
		elif [ "$$(uname)" = "Linux" ]; then \
			curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null; \
			echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list >/dev/null; \
			sudo apt update && sudo apt install -y ngrok; \
		else \
			echo "Unsupported OS. Please install ngrok manually."; \
			exit 1; \
		fi \
	else \
		echo "ngrok is already installed."; \
	fi
	@echo "Starting ngrok on port $(PORT)..."
	@ngrok http $(PORT)
