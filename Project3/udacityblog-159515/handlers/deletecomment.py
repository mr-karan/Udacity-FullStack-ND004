from google.appengine.ext import db
from handlers.blog import BlogHandler
from helpers import *

class DeleteCommentHandler(BlogHandler):

    def get(self, post_id, post_user_id, comment_id):
        comment = db.Key.from_path('Comment', int(comment_id), parent=blog_key())
        comment = db.get(comment)
        if not comment:
            return self.redirect('/login')

        if self.user and self.user.key().id() == comment.user_id:
            comment.delete()

            self.redirect('/' + post_id)

        elif not self.user:
            self.redirect('/login')

        else:
            self.write("You don't have permission to delete this comment.")
