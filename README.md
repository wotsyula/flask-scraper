# flask-scraper
Scraper engine based on [Selenium](https://www.selenium.dev) Python bindings. Uses [Flask](https://flask.palletsprojects.com/en/2.0.x/) for its API and [ReactJS](https://reactjs.org) for its client.

## Requirements
- [Python](https://wiki.python.org/moin/BeginnersGuide/Download)  v3.7+
- [Node.js](https://nodejs.dev/learn/how-to-install-nodejs)  v12+
- [Docker](https://docs.docker.com/desktop/) latest

## Install

1. Set up Python enviromnent:
    ```bash
    python -m venv .env
    source .env/bin/activate
    python -m pip install -r requirements.txt
    ```

    Windows users should use `activate.bat` instead:
    ```powershell
    .env\Scripts\activate.bat
    ```

2. Setup Node.js environment:
    ```bash
    npm install
    ```

3.  Build client:
    ```bash
    npm run build

4. Edit `composer/standalone-chrome` with your VNC password. Replace `flaskscraper@123`.
5. Edit `docker-compose.yml` with your PostgreSQL database. Afterwards start the service with:
    ```bash
    sudo docker compose up
    ```

    Windows users should omit the `sudo`
    ```powershell
    docker compose up
    ```
6. Navigate to home page:
    ```
    http://localhost:5000
    ```

&nbsp;

## Development & Testing

### Environment Variables
- `PYTHONUNBUFFERED`: Used to configure python. Set to `true`
- `FLASK_ENV`: Used to configure Flask server. Set to `development`
- `NODE_ENV`: Used to configure Webpack. Set to `development`
- `DATABASE_URI`: Link to PostgreSQL database. Default `postgres://postgress:postgress@localhost/postgres`
- `SELENIUM_URI`: Link to Selenium API server. Should not include a trailing slash. Default `http:/localhost:4444`

### Directory Structure

```txt
.
+-- src
|   +-- client
|   |   +-- static
|   |       +-- index.htm       # react single page app
|   |       +-- favicon.ico
|   |       +-- main.js         # webpack bundle file
|   +-- server
|       +-- app.py              # flask application file
|       +-- conftest.py         # pytest configuration file
|       +-- routes
|           +-- scrapper        # scripts are stored here
+-- .browserlist                # configuration used by babel-loader
+-- .babelrc                    # babel-loader configuration file
+-- docker-compose.yml          # docker service configuration
+-- Dockerfile                  # docker file for flask container
+-- package.json                # node.js configuration
+-- setup.py                    # python configuration
+-- requirements.txt            # python configuration
```

React.js client files are found in the `src/client` directory. These are compiled using Webpack into `src/client/static` directory. See [README.md](src/client/README.md) for more information

Flask REST server files are found in `src/server` directory. You can add new scripts by creating a folder in `src/server/routes/scraper` directory. See [README.md](src/server/README.md) for more information
### Run Selenium in Docker
```
docker run \
    --rm -d -p 4444:4444/tcp -p 5900:5900/tcp \
    --name selenium \
    -e SE_NODE_SESSION_TIMEOUT=240 \
    -e SE_NODE_MAX_SESSIONS=16 \
    -v /dev/shm:/dev/shm \
    selenium/standalone-chrome:91.0
```

### Start Development Server (Linux / bash)
```bash
export NODE_ENV=development
export FLASK_ENV=development
source .env/bin/activate
npm run watch &
python -m flask run
```

### Start Development Server (Windows / powershell)
```powershell
$env:NODE_ENV=development
$env:FLASK_ENV=development
.env\Scripts\activate.bat
Start-Process -NoNewWindow npm -ArgumentList "run", "watch"
python -m flask run
```
