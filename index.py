import sqlite3
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from helpers import *

app = FastAPI()


# Body for adding a comment, comment text is mandatory
class addAComment(BaseModel):
    comment: str


# Adds a comment
@app.post("/addComment")
def addAComment(addACommentyBody: addAComment):
    sanitizedText = sanitizeString(addACommentyBody.comment).strip()

    postConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = postConnection.cursor()

    queryToAddComment = "INSERT INTO COMMENTREPLY (TEXTID, TEXTCONTENT, TEXTTYPE, TEXTTIME) Values (?, ?, ?, ?)"
    generatedIDForComment = generateID()  # Storing the UUID to insert and return in response
    valuesToAddComment = (generatedIDForComment, sanitizedText, 'COMMENT', currentEpochTime())
    cur.execute(queryToAddComment, valuesToAddComment)
    postConnection.commit()
    return {"status": "Comment added", "commentID": generatedIDForComment}





# Body for adding a reply to a comment, reply text and comment id are mandatory
class addAReply(BaseModel):
    reply: str
    commentID: str


@app.post("/addReply")
def addAReply(addAReplyBody: addAReply, response: Response):
    sanitizedText = sanitizeString(addAReplyBody.reply).strip()

    postConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = postConnection.cursor()

    # Checks if there is any comment with the provided comment ID, if not, its rejected with a 404
    queryToCheckComment = "SELECT * FROM COMMENTREPLY WHERE TEXTID = ? and TEXTTYPE = 'COMMENT'"
    valuesToCheckComment = [addAReplyBody.commentID]
    commentCheck = cur.execute(queryToCheckComment, valuesToCheckComment).fetchall()
    if len(commentCheck) == 0:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Comment with the ID " + addAReplyBody.commentID + " exists. Please recheck"}

    # If the comment ID exists, inserts into the DB
    queryToAddReply = "INSERT INTO COMMENTREPLY (TEXTID, TEXTCONTENT, TEXTTYPE, TEXTTIME, COMMENTID) Values (?, ?, ?, ?, ?)"
    generatedIDForReply = generateID() # Storing the UUID to insert and return in response
    valuesToAddReply = (generatedIDForReply, sanitizedText, 'REPLY', currentEpochTime(), addAReplyBody.commentID)
    cur.execute(queryToAddReply, valuesToAddReply)
    postConnection.commit()
    return {"status": "Reply added", "replyID": generatedIDForReply}