import sqlite3
from fastapi import FastAPI, Response, status
from pydantic import BaseModel
from helpers import *

app = FastAPI()

@app.get("/")
def landingPage():
    return ("Hello, welcome to Comment and Reply API in Python.")


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

# Adds a Reply
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
    generatedIDForReply = generateID()  # Storing the UUID to insert and return in response
    valuesToAddReply = (generatedIDForReply, sanitizedText, 'REPLY', currentEpochTime(), addAReplyBody.commentID)
    cur.execute(queryToAddReply, valuesToAddReply)
    postConnection.commit()
    return {"status": "Reply added", "replyID": generatedIDForReply}



# Gets all the comments
@app.get("/getAllComments")
def getAllTheComments():
    getConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = getConnection.cursor()

    queryToGetComments = "SELECT TEXTCONTENT, TEXTID, TEXTTIME FROM COMMENTREPLY WHERE TEXTTYPE = 'COMMENT'"
    allComments = cur.execute(queryToGetComments).fetchall()

    formattedComments = []
    for commentText, commentID, commentTime in allComments:
        formattedComments.append({"commentText": commentText, "commentID": commentID, "commentTime": commentTime})

    return formattedComments



# Gets a specific comment based on its ID
@app.get("/getComment")
def getCommentByID(response: Response, commentID: str):
    getConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = getConnection.cursor()

    queryToGetComment = "SELECT TEXTCONTENT, TEXTTIME FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'COMMENT'"
    valuesToGetComment = [commentID]
    commentCheck = cur.execute(queryToGetComment, valuesToGetComment).fetchone()
    if commentCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Comment with the ID " + commentID + " exists. Please recheck"}

    queryToGetReplyCount = "SELECT COUNT(*) FROM COMMENTREPLY WHERE COMMENTID = ?"
    valuesToGetReplyCount = [commentID]
    replyCountCheck = cur.execute(queryToGetReplyCount, valuesToGetReplyCount).fetchone()

    return {"commentID": commentID, "commentText": commentCheck[0], "commentTime": commentCheck[1], "replyCount": replyCountCheck[0]}



# Gets all the replies of a Comment based on its ID
@app.get("/commentReplies")
def getRepliesOfAComment(response: Response, commentID: str):
    getConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = getConnection.cursor()

    queryToGetComment = "SELECT TEXTCONTENT FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'COMMENT'"
    valuesToGetComment = [commentID]
    commentCheck = cur.execute(queryToGetComment, valuesToGetComment).fetchone()
    if commentCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Comment with the ID " + commentID + " exists. Please recheck"}

    queryToGetCommentReplies = "SELECT TEXTCONTENT, TEXTID, TEXTTIME FROM COMMENTREPLY WHERE COMMENTID = ?"
    valuesToGetCommentReplies = [commentID]
    commentRepliesCheck = cur.execute(queryToGetCommentReplies, valuesToGetCommentReplies).fetchall()

    formattedCommentReplies = []
    for replyText, replyID, replyTime in commentRepliesCheck:
        formattedCommentReplies.append({"replyText": replyText, "replyID": replyID, "replyTime": replyTime})

    return formattedCommentReplies



# Gets a reply based on its ID
@app.get("/getReply")
def getReplyByID(response: Response, replyID: str):
    getConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = getConnection.cursor()

    queryToGetReply = "SELECT TEXTCONTENT, TEXTTIME, COMMENTID FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'REPLY'"
    valuesToGetReply = [replyID]
    replyCheck = cur.execute(queryToGetReply, valuesToGetReply).fetchone()
    if replyCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Reply with the ID " + replyID + " exists. Please recheck"}

    return {"replyID": replyID, "replyText": replyCheck[0], "replyTime": replyCheck[1], "commentID": replyCheck[2]}



# Body for updating a comment or a reply, text is mandatory
class updateACommentOrReply(BaseModel):
    comment: str

# Updates a comment
@app.put("/updateComment")
def updateCommentByID(commentID: str, updateCommentOrReplyBody: updateACommentOrReply, response: Response):
    putConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = putConnection.cursor()

    queryToCheckComment = "SELECT * FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'COMMENT'"
    valuesToCheckComment = [commentID]
    commentCheck = cur.execute(queryToCheckComment, valuesToCheckComment).fetchone()
    if commentCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Comment with the ID " + commentID + " exists. Please recheck"}

    queryToUpdateComment = "UPDATE COMMENTREPLY SET TEXTCONTENT = ? WHERE TEXTID = ?"
    valuesToUpdateComment = (updateCommentOrReplyBody.comment, commentID)
    cur.execute(queryToUpdateComment, valuesToUpdateComment)
    putConnection.commit()
    return {"status": "Comment updated"}


# Updates a reply
@app.put("/updateReply")
def updateCommentByID(replyID: str, updateCommentOrReplyBody: updateACommentOrReply, response: Response):
    putConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = putConnection.cursor()

    queryToCheckReply = "SELECT * FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'REPLY'"
    valuesToCheckReply = [replyID]
    replyCheck = cur.execute(queryToCheckReply, valuesToCheckReply).fetchone()
    if replyCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Reply with the ID " + replyID + " exists. Please recheck"}

    queryToUpdateReply = "UPDATE COMMENTREPLY SET TEXTCONTENT = ? WHERE TEXTID = ?"
    valuesToUpdateReply = (updateCommentOrReplyBody.comment, replyID)
    cur.execute(queryToUpdateReply, valuesToUpdateReply)
    putConnection.commit()
    return {"status": "Reply updated"}



# Deletes a comment by its ID. When a comment is deleted all its associated replies are also deleted.
@app.delete("/deleteComment")
def deleteCommentByID(commentID: str, response: Response):
    delConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = delConnection.cursor()

    queryToCheckComment = "SELECT * FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'COMMENT'"
    valuesToCheckComment = [commentID]
    commentCheck = cur.execute(queryToCheckComment, valuesToCheckComment).fetchone()
    if commentCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Comment with the ID " + commentID + " exists. Please recheck"}

    queryToDeleteComment = "DELETE FROM COMMENTREPLY WHERE TEXTID = ? OR COMMENTID = ?"
    valuesToDeleteComment = [commentID, commentID]
    cur.execute(queryToDeleteComment, valuesToDeleteComment)
    delConnection.commit()
    return {"status": "Comment with ID " + commentID + " and all its replies are deleted"}



# Deleted a reply by its ID.
@app.delete("/deleteReply")
def deleteCommentByID(replyID: str, response: Response):
    delConnection = sqlite3.connect("COMMENTREPLY.db")
    cur = delConnection.cursor()

    queryToCheckReply = "SELECT * FROM COMMENTREPLY WHERE TEXTID = ? AND TEXTTYPE = 'REPLY'"
    valuesToCheckReply = [replyID]
    commentCheck = cur.execute(queryToCheckReply, valuesToCheckReply).fetchone()
    if commentCheck is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"status": "No Reply with the ID " + replyID + " exists. Please recheck"}

    queryToDeleteReply = "DELETE FROM COMMENTREPLY WHERE TEXTID = ?"
    valuesToDeleteReply = [replyID]
    cur.execute(queryToDeleteReply, valuesToDeleteReply)
    delConnection.commit()
    return {"status": "Reply with ID " + replyID + " is deleted"}