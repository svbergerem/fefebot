import diaspy.models
import diaspy.streams
import diaspy.connection
import config

class Client:
  def __init__(self):
    self.connection = diaspy.connection.Connection(pod=config.pod, username=config.username, password=config.password)
    self.connection.login()
    self.stream = diaspy.streams.Stream(self.connection, 'stream.json')
  def post(self, text):
    """This function sends a post to an aspect
    :param text: text to post
    :type text: str
    :returns: diaspy.models.Post -- the Post which has been created
    """
    post = self.stream.post(text, aspect_ids='public', provider_display_name='fefebot')
    return post
  def comment(self, post_id, text):
    """This function comments on a post
    :param post_id: ID of post to comment on
    :type post_id: int
    :param text: text of comment
    :type text: str
    """
    diaspy.models.Post(self.connection,id=post_id).comment(text)
