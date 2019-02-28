# Crawler
Web application to pull out images from web sites by crawling to a given depth.

## Installation
### Backend
Uses python, flask, beautifulsoup (for parsing html only) and celery for handling asynchronous requests.

`pip install -r requirements.txt` 

should take care of all the dependencies for the backend. It can be run with a wsgi server like gunicorn for production.

### Frontend
Uses Node.js, React and Bootstrap. Need to provide the details of the backend server and port in App.js. 

`npm build`

should create a bundle that's good for production.

