
## How To
The program expects an `.env` file with the twitter api credentials in the following format:
```
BEARER_TOKEN=TOKEN
API_KEY=KEY
API_SECRET_KEY=SECRET
ACCESS_TOKEN=my-access-token
ACCESS_TOKEN_SECRET=my-access-token-secret
```

Use `npm install && npm run compile` to install dependencies and compile the program. 
The program supports three different modes `query`, `verify`, and `statistic`.
Run the program with `npm run start mode path/to/file`.

For `query` the given file should be a csv file containing only one column per row containing a valid twitter user id. For this user id all followers are querried and stored.

The other modes expect a file input in the format generated from the `query` mode. This is a csv file with the headers `id, name, username, parent`.


## Example Docker command
`docker build -t fopro . && docker run -d -v /local/file/path/data:/usr/app/data fopro verify /usr/app/data/fileName.csv`

## Post Processing Scripts
The post processing scripts folder contains additional scripts to calculate statistical information based on the previously querried datasets. 