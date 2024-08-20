# Backend for a Comment/Reply App using FastAPI, SQLite and Python

This repo has the code for a Comment/Reply App Backend. The basic functionality of the app is as follows 

* Any number of comments can be added
* Any number of replies can be added but replies should be linked to a comment via the Comment ID
* Deleting a comment will delete the all the replies linked to the comment
  
The below REST API endpoints are exposed

* POST /addComment

  > This endpoint allows you to add a comment.<br><br>
  > The POST Body is
  > ```
  > {
  > "comment": "<COMMENT_TEXT>"
  > }
  > ```

* POST /addReply

  > This endpoint allows you to add a reply to a comment.<br><br>
  > The POST Body is
  > ```
  > {
  > "reply": "<REPLY_TEXT>",
  > "commentID": "<ID_OF_THE_COMMENT_TO_WHICH_THIS_REPLY_IS_ADDED>"
  > }
  > ```
  
* GET /getAllComments
  
  > This endpoint allows you to get all the comments.<br><br>

* GET /getComment
  
  > This endpoint allows you get the comment details of a comment, details include comment time and no of replies for this comment. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?commentID=<COMMENT_ID>
  > ```
  
* GET /commentReplies
  
  > This endpoint allows you get the all the replies of a comment. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?commentID=<COMMENT_ID>
  > ```
  
* GET /getReply
  
  > This endpoint allows you get the reply details of a reply, details include reply time and comment ID. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?replyID=<REPLY_ID>
  > ```
  
* PUT /updateComment

  > This endpoint allows you to update a comment. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?commentID =<COMMENT_ID>
  > ```
  > The PUT Body is
  > ```
  > {
  > "comment": "<COMMENT_TEXT>"
  > }
  > ```
  
* PUT /updateReply

  > This endpoint allows you to update a reply. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?replyID=<COMMENT_ID>
  > ```
  > The PUT Body is
  > ```
  > {
  > "reply": "<REPLY_TEXT>"
  > }
  > ```
  
* DELETE /deleteComment

  > This endpoint allows you to delete a comment. Deleting a comment will delete the all the replies linked to the comment. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?commentID=<COMMENT_ID>
  > ```
  
* DELETE /deleteReply

  > This endpoint allows you to delete a reply. It requires a query param to be sent.<br><br>
  > The Query Parameter is
  > ```
  > ?replyID=<REPLU_ID>
  > ```

To run it in Dev mode, use the FastAPI run command

```console
fastapi dev .\index.py
```

Once the app is started locally, the below URL's will be available 

```
API Endpoint URL : http://127.0.0.1:8000 
Generated API Docs URL : http://127.0.0.1:8000/docs
```
