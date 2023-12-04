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
