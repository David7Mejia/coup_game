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
## 1 Install Env 
```
pip install virtualenv
```
## 2 Create environment for backend 
```
virtualenv venv
```

## 3 Activate Env
```
- On Windows:
    
    
    .\venv\Scripts\activate

    
- On macOS and Linux:
    
   
    source venv/bin/activate
  
```
## 4 Install requirements.txt file
```
pip install -r requirements.txt
```
# **If PSQL is not installed follow these instructions:
### Example (Linux with apt):

```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

## 5 PSQL commands
The default password for postgreSQL on download is postgres
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

## Put PSQL Credentials in .env file 
LOCATION: coup_game/backend_coup/.env
```
DB_NAME=your_database_name(from above)
DB_USER=your_username(from above)
DB_PASSWORD=your_password(from above)
DB_HOST=localhost
DB_PORT=5432

```


