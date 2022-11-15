# Library Management API
### Api URL: https://library-mngt.herokuapp.com/ ('GET')
## Authentication
### Register
```
curl 'https://library-mngt.herokuapp.com/register' \
-H 'Content-Type: multipart/form-data' \
-F 'patj/to/image.jpg' \
--data-binary '{"email":"[user@example.com]","password":[YOUR_PASSWORD], "firstname":[YOUR_NAME], "lastname":[LAST_NAME], "regNo":[XX(A-Z)XXXX]}'
```
#### response
```
{
  "token": [YOUR_ACCESS_TOKEN]
}
```
### Login
```
curl 'https://library-mngt.herokuapp.com/login' \
-H 'Content-Type: application/json' \
--data-binary '{"email":"[user@example.com]","password":[YOUR_PASSWORD]}'
```
#### response
```
{
  "token": [YOUR_ACCESS_TOKEN]
}
```
## Manage Books
### Add Book
```
curl 'https://library-mngt.herokuapp.com/addBook' \
-H 'Content-Type: application/json' \
-H 'token: [YOUR_ACCESS_TOKEN]' \
--data-binary '{"title":"[BOOK_TITLE]","author":[BOOK_AUTHOR], "description":[ABOUT_BOOK]}'
```
#### response
```
Added book to the shelf
```
### Take Book
#### Ex: Book Name: Alpha, Author: Chin, BOOK_NAME: ALPHACHIN 
```
curl 'https://library-mngt.herokuapp.com/take' \
-H 'Content-Type: application/json' \
-H 'token: [YOUR_ACCESS_TOKEN]' \
--data-binary '{"bookName":"[BOOK_NAME]"}'
```
#### response
```
Added to your shelf successfully
```
### Return Book
```
curl 'https://library-mngt.herokuapp.com/returnBook' \
-H 'Content-Type: application/json' \
-H 'token: [YOUR_ACCESS_TOKEN]' \
--data-binary '{"bookName":"[BOOK_NAME]"}'
```
#### response
```
You have returned the book
```



