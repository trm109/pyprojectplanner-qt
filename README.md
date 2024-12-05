# Py Project Planner

## Running the client

### Requirements
Python 3.12 (others may work, but this is the only tested one)

### Installation/Building
Steps:
1. `cd client`
2. `pip install -r requirements.txt`
### Running
Assuming you are still in `./client/`
1. `python main.py`

## Running the server

### Requirements
Docker is the backend's only dependency.

### Installation/Building
Steps:
1. `cd server`
2. `docker build server -t kanban`
3. `cd ..`
### Running
1. `docker run -d -p 8000:8000 -v ./data:/data/ kanban`
2.  The server is now running in the background, you can check on it via `docker ps` and `docker logs container_name`
