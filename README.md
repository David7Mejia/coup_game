# Coup The Game (ok the foundations of a FullStack Coup game)

 The app is made using Django/Python3.x for the backend and React/JS for the frontend.
 For setup instructions, please see below. The game uses a PostgreSQL database.
 Due to time constraints not all the actions were implemented.
### Actions:
- Income
- Foreign Aid
- Coup
- Tax
- Assassinate
- Exchange
- Steal

### No counteractions or challenge were implemented (yet), the UI is fairly basic (see attached image in directory)
You choose the number of players
Then you start the game Player 1 being human and the rest being bots.

## There is still a lot to implement (Version1.0 ) but the basics are there, and it provides a good foundation for a basic experience as an MVP.


# Frontend
## Project setup
```
cd frontend/coup-frontend
```
```
npm install
```
```
npm start
```

# Backend
## Project setup
```
cd backend-coup
```

<!-- install requirements.txt file -->

```
pip install -r requirements.txt
```

## Example .env file
```
place here: /backend_coup
```
```
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_HOST=localhost
DB_PORT=5432

```
## Simple PSQL install/setup

### Example (Linux with apt):

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```


### Example (macOS with Homebrew):
```
brew install postgresql
```

### PSQL commands
```
# Log in to the PostgreSQL interactive terminal
sudo -u postgres psql

# Create a new database
CREATE DATABASE your_database_name;

# Create a new user and grant necessary permissions
CREATE USER your_username WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE your_database_name TO your_username;

# Exit the PostgreSQL interactive terminal
\q

```
