#ASYNC API SCRAPER

### REQUIREMENTS
Python version >= 3.9.7
python-environ >= 0.4.54
aiohttp >= 3.8.1

### DESCRIPTION
Python scripts to get data from `jsonplaceholder.typicode.com` api and save data to csv.

### QUICK START

1. clone repo from `git@github.com:qbasista/api-scraper.git`
2. create environment (you can use pyenv or other python enviroment tool)
3. install requirements: `pip install .`
4. set .env file:
   1. copy from example: `cp core/.env core/.env.example`
   2. in .env you have default value for API_URL and IO_REQUEST_LIMIT
   3. to change api url change API_URL 
   4. to change limit of request per second change value for IO_REQUEST_LIMIT
5. run code: `python core/main.py`
6. check result:
   1. `assets/users.csv` -> all users
   2. `assets/albums.csv` -> all albums
   3. `assets/photos.csv` -> all photos
   4. `asstes/photos/*` -> all downloaded files