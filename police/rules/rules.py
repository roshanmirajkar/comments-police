from __future__ import print_function
import re
from police.utils import black_word_regex, gray_word_regex
from unidecode import unidecode
from copy import copy as shallow_copy
import string
import math
import requests
import json
import urllib2
import logging

# First rule that takes comment and checks to see if > %50 of chars are uppcase
def check_cap(comment):
    # if sum of uppercase chars are > comment len /2 ( more than 50%) then return false
    # filters out punctuation
    for b in string.punctuation:
        copy = shallow_copy(comment)
        copy = copy.replace(b, "")
    # removes white space and checks chart
    for z in string.punctuation:
        copy = copy.replace(" ", "")
    if (sum(1 for a in copy if a.isupper()) > (len(copy)/2)):
        result = {}
        result['name'] = 'uppercase_words'
        sample_message = u'<h3>Woah there caps lock on? '\
                         u'You have quite a bit of uppercase characters. Your '\
                         u'comment may be deleted due to unreadability, would you '\
                         u'like to change your comment or submit anyway?</h3>'
        result['sample_message'] = sample_message
        return result
    else:
        return False


# Second rule that takes comment and checks to see if max char threshold has been exceeded
def max_char(comment):
    commentIn = comment
    if (len(commentIn) >= 2000):
        result = {}
        result['name'] = 'maximum_chars'
        sample_message = u'<h3>Nice typing! Unfortunately you have exceeded the 2000 character '\
                         u'limit. Please reduce the length of your comment to prevent auto deletion. Would '\
                         u'you like to submit anyway?<h3>'
        result['sample_message'] = sample_message
        return result
    else:
        return False



# Third rule that takes in comment and checks to see if spam repetition is present
def spam_catch(comment):
    commentinCheck = comment
    # amount of unique words
    uniqueWords = len(set(s.lower() for s in commentinCheck.split()))
    # amount of words in comment
    totalWords = len(commentinCheck.split())
    result = {}
    result['name'] = 'catch_spam'
    sample_message = u'<h3>Hey there! we have detected that this comment '\
    u'may be spam. Please change your comment '\
    u'or hit submit?<h3>'
    result['sample_message'] = sample_message
    #if there is one word check how many unique chars are there
    if totalWords == 3:
        count = {}
        for s in commentinCheck:
            if count.has_key(s):
                count[s] += 1
            else:
                count[s] = 1
        for key in count:
            if count[key] > 1:
                sample_message = u'<h3>Hey we know that your comment is spam<h3>'
                result['sample_message'] = sample_message
                return result
    #compare unique words to total words
    elif totalWords > 2 and (uniqueWords < totalWords/(math.log(totalWords))):
        return result
    else:
        return False

# Fourth rule that takes in comment and checks to see if black words are present
def contains_black_words(comment):
    ascii_comment = unidecode(comment).replace('\n', ' ')
    violations = black_word_regex.findall(ascii_comment)
    if violations == []:
        return False
    else:
        result = {}
        result['name'] = 'black_words'
        violations = list(set(map(lambda x:
                                  x[0].strip(), violations)))
        result['violations'] = violations
        sample_message = u'<h3>You\'ve used one or more words that will cause your' \
                         u' comment to be deleted automatically. Would you' \
                         u' like to rephrase your comment or try to submit' \
                         u' anyways?</h3><br> <h4>Caught banned words:</h4><ul><li>{}</li>'.format(
                             '\t'.join(violations))
        result['sample_message'] = sample_message
        return result

# Fifth rule that takes in comment and checks to see if gray words are present
def contains_gray_words(comment):
    ascii_comment = unidecode(comment).replace('\n', ' ')
    violations = gray_word_regex.findall(ascii_comment)
    if violations == []:
        return False
    else:
        result = {}
        result['name'] = 'gray_words'
        violations = list(set(map(lambda x:
                                  x[0].strip(), violations)))
        result['violations'] = violations
        sample_message = u'<h3>You\'ve used one or more words that someone might'\
                         u' find offensive. Would you' \
                         u' like to rephrase your comment or try to submit' \
                         u' anyways?</h3><br> <h4>Caught words:</h4><ul><li>{}</li>'.format(
                             '\t'.join(violations))
        result['sample_message'] = sample_message
        return result

# Sixth rule that takes in the comment and optionally takes in the "ReplyTo username" if this comment is a response to another.
# Checks comment for any negative/aggressive words/phrases around second person word (you, your, you're, etc).
# Also when there is a replyTo username, this checks if the comment includes that username of the original commenter.
def directed_aggression(comment, reply=None):
    bad_flag = False
    violations = []
    # Store variations of ways to address a user
    user = ['you', 'u', 'yu', 'your', 'youre', 'yo', 'yourself', 'yourselves']
    comment = unidecode(comment)
    normalized_comment = comment.lower()
    user_name_location = -1
    if reply is not None:
        reply = reply.lower()
        user_name_location = normalized_comment.find(reply)
    # Check if the username is mentioned in the comment, if so make the username one word and change within comment.
    if user_name_location > -1:
        short = re.sub('[^0-9A-Za-z]', '', reply)
        user.append(short)
        normalized_comment = re.sub(reply, short, normalized_comment)
    normalized_comment = re.sub('[?:&-]', ' ', normalized_comment)
    normalized_comment = re.sub('[^0-9A-Za-z ]', '', normalized_comment)
    words = normalized_comment.split(' ')
    # Regex will go through and look for these word stems.  More can be appended.
    grey_regex = re.compile("(?:\A|\W)(stupid|dum|ignor|idiot|jerk|shut up|die|(?:kill\w*)|pathetic|"
                            "imbecile|rape|lobotom|moron|murder|loser|kkk)(?:\w*)")

    for index, word in enumerate(words):
        # If a word has a 'user' word, get the surrounding words and check for the negative 'grey' stems.
        if word.strip() in user:
            high = get_high(index, len(words))
            low = get_low(index)
            surrounding = []
            for i in range(low, high):
                surrounding.append(words[i].strip())
            phrase = ' '.join(surrounding)
            # If any negative 'grey' stem is in the phrase, store entire phrase as violation.
            if re.search(grey_regex, phrase) is not None:
                bad_flag = True
                violations.append(phrase)

    # Currently the violations will always be stored,
    # but in the future there may be cases when it is unnecessary to store the violating phrase.
    # Also note that the phrase captured as violating has been 'normalized', meaning
    # the replyTo username is all one word, everything is lowercase and all non alphanumeric chars are removed.
    # So it is not currently the exact copy of what the commenter typed.
    if bad_flag:
        if violations:
            return {'name': 'directed_aggression',
                    'sample_message': "<h3>We do not allow for any aggression directed at another user. This comment will be reviewed before posting.</h3>",
                    'violations': violations}
        else:
            return {'name': 'directed_aggression',
                    'sample_message': "<h3>We do not allow for any aggression directed at another user. This comment will be reviewed before posting.</h3>"}
    else:
        return False


# Gets the index of the word five ahead of this index, or returns maximum if out of bounds.
def get_high(index, max):
    high = index + 5
    if high > max:
        return max
    else:
        return high


# Gets the index of the word one before this index, or returns 0.
def get_low(index):
    low = index - 1
    if low < 0:
        return 0
    else:
        return low

# seventh rule
def find_link(comment):
    try: 
        x = re.search("(?P<url>https?://[^\s]+)", comment).group("url")
        r = requests.get('http://api.mywot.com/0.4/public_link_json2?hosts=example.COM/www.EXAMPLE.NET/&callback=process&key=<965e77c0a4baa31e51d3e60625733cd2e7874ae8>')

        result = {}
        result['name'] = 'find_link'
        sample_message = u'<h3> You sure you want to post that link?<h3>'
        result['sample_message'] = sample_message
        return result
    except Exception as e:
        return False
        # Logs the error appropriately. 

# Idea is to store functions in the array to be run each time for extensibility
rules = [check_cap, max_char, spam_catch, directed_aggression, contains_black_words, contains_gray_words,find_link]
