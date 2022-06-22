
npm run start verify path/to/file
npm run start query path/to/file

file expects a csv file with one id per row and nothing else in it.

docker build -t fopro . && docker run -d -v /local/file/path/data:/usr/app/data fopro verify /usr/app/data/fileName.csv