import json, re
from pprint import pprint



def sort():
    output = open('comments.txt', 'w')
    with open('2016-july-1819.json', 'r') as f:
        for line in f:
            x = json.loads(line)
            comment = x['object']['content'].encode('utf8').strip()
            clean = re.sub('\\n', ' ', comment)
            output.write(clean + '\n')

    f.close()
    output.close()


if __name__ == '__main__':
    sort()