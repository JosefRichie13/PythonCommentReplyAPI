# Backend for a Comment/Reply App using FastAPI, SQLite and Python

This repo has the code for a Comment/Reply App Backend. The basic functionality of the app is as follows 

* Any number of comments can be added
* Any number of replies can be added but replies should be linked to a comment via the Comment ID
* Deleting a comment will delete the all the replies linked to the comment
  
The below REST API endpoints are exposed

* POST /addComment
* POST /addReply
* GET /getAllComments
* GET /getComment
* GET /commentReplies
* GET /getReply
* PUT /updateComment
* PUT /updateReply
* DELETE /deleteComment
* DELETE /deleteReply

To run it in Dev mode, use the FastAPI run command

```console
fastapi dev .\index.py
```

Once the app is started locally, the below URL's will be available 

```
API Endpoint URL : http://127.0.0.1:8000 
Generated API Docs URL : http://127.0.0.1:8000/docs
```
