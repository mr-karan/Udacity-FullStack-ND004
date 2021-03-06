from google.appengine.ext import db
from handlers.blog import BlogHandler
from helpers import *

class DeletePostHandler(BlogHandler):

    def get(self, post_id, post_user_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        if not post:
            return self.redirect('/login')

        # To Check if user owns the post
        if self.user and self.user.key().id() == post.user_id:
            post.delete()
            self.redirect('/')

        elif not self.user:
            self.redirect('/login')

        else:
            key = db.Key.from_path('Post', int(post_id), parent=blog_key())
            post = db.get(key)
            if not post:
                return self.redirect('/')

            comments = db.GqlQuery(
                "select * from Comment where ancestor is :1 order by created desc limit 10", key)

            error = "You don't have permission to delete this post"
            self.redirect("permalink.html", post=post, comments=comments, error=error)
