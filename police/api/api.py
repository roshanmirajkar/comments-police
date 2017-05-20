from police.api import app
from police.rules import evaluate_comment
from flask import request

@app.route('/comment/<comment_section>/', methods=['GET'])
def check_comment(comment_section):
    comment = request.args.get('comment', None)
    reply = request.args.get('reply', None)
    return evaluate_comment(comment, comment_section, reply=reply)
