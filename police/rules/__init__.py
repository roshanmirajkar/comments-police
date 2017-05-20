from police.rules.rules import rules
from flask import jsonify

# Check the supplied comments against the  rules
def evaluate_comment(comment, section, user_status=None, reply=None, referrer=None):
    results = []
    # Evaluate in order
    # TODO change to coroutines or threads
    for rule in rules:
        if rule.func_name is 'directed_aggression':
            results.append(rule(comment, reply))
        else:
            results.append(rule(comment))
    if not any(results):
        return jsonify(status='ok', comment=comment)
    else:
        return jsonify(status='bad',
                       # Get only the failing results
                       failures=filter(lambda result: result,
                                       results),
                       comment=comment
                       )
