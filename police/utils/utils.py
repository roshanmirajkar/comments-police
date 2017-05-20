def build_regex(black_words, character_options):
    regexp = map(lambda x:
                 r'(?:{}s?)'.format(r''.join([character_options[char] for char in x])), black_words)
    return regexp

def build_single_regex(regex_list):
    or_block = reduce(lambda acc, word:
                      '{}|{}'.format(acc, word), regex_list)
    # return r'((?:\A|\s+|\-|\()(?:{})(?:\Z|\s+|[:;\'"\).,]))'.format(or_block)
    return r'(?=((?:\A|\W)({})(?:\Z|\W)))'.format(or_block)

special_character_representations = {
    'a': r'(?:a|@|4)',
    'b': r'(?:b|l3|i3)',
    'c': r'(?:c|\(|k)',
    'd': r'(?:d)',
    'e': r'(?:e|3)',
    'f': r'(?:f|ph)',
    'g': r'(?:g|6|9)',
    'h': r'(?:h)',
    'i': r'(?:i|l|!|1|y)',
    'j': r'(?:j)',
    'k': r'(?:c|\(|k)',
    'l': r'(?:l|1|!|i)',
    'm': r'(?:m)',
    'n': r'(?:n|\|\\\|)',     # matches |\|
    'o': r'(?:o|0|\(\))',     # matches ()
    'p': r'(?:p)',
    'q': r'(?:q|9)',
    'r': r'(?:r)',
    's': r'(?:s|\$|5)',
    't': r'(?:t|7)',
    'u': r'(?:u|v|8)',
    'v': r'(?:v|u)',
    'w': r'(?:w|vv)',
    'x': r'(?:x)',
    'y': r'(?:y)',
    'z': r'(?:z|2)',
    ' ': ' ',
    '-': r'\-'
}

banned_words = ['asshat', 'asshole', 'ass', 'ahole', 'allbyer', 'anus', 'arse', 'arsehole', 'aryan', 'assbag', 'assbandit', 'assbanger', 'assbite', 'assclown', 'asscock', 'asses', 'assface', 'assfuck', 'assgoblin', 'asshat', 'asshole', 'asshopper', 'assjabber', 'assjacker', 'asslick', 'assmonkey', 'assmucus', 'assmunch', 'assmuncher', 'assnigger', 'asspirate', 'assshit', 'assshole', 'asssucker', 'asswad', 'asss', 'asswipe', 'bastard', 'batshit', 'biatch', 'bich', 'bitch', 'bitched', 'bitches', 'bitching', 'bitchy', 'bitchass', 'blowhole', 'blowjob', 'boob', 'boobie', 'boobs', 'booby', 'bullshit', 'bullshitter', 'bullshitting', 'bullshytt', 'bushshit', 'bytchassnigga', 'bytrade', 'cankle', 'cankles', 'ccshoper', 'chickenshit', 'chink', 'chinc', 'choad', 'clit', 'clitface', 'clitfuck', 'cockass', 'clusterfuck', 'cock', 'cockjockey', 'cockhead', 'cockmonkey', 'cockmongler', 'cocknose', 'cocknugget', 'cockshit', 'cocksuck', 'cocksucker', 'cocksuckers', 'cocksucking', 'coksucker', 'coon', 'cooter', 'coochy', 'cockwaffle', 'craphammer', 'crapphammer', 'cum', 'cumbubble', 'cumdumpster', 'cumguzzler', 'cumjockey', 'cumslut', 'cumtart', 'cunnie', 'cumming', 'cums', 'cunt', 'cuntass', 'cuntbag', 'cuntface', 'cunthole', 'cuntlicker', 'cuntrag', 'cuntslut', 'cuntree', 'cuntry', 'dbag', 'darkie', 'darkies', 'dickface', 'dickhead', 'dicks', 'dickslap', 'dickweed', 'dipshit', 'doosh', 'dooshbag', 'dothead', 'douchbag', 'douche', 'douchebag', 'douches', 'dovchebag', 'dumbass', 'dumbfuck', 'dumbfuck', 'dumbshit', 'dyke', 'effin', 'effing', 'fag', 'fagg', 'fagget', 'faggit', 'faggot', 'faggotry', 'faggots', 'faggy', 'fagit', 'fags', 'fcking', 'fckn', 'fcuk', 'fcuking', 'fkn', 'fock', 'focker', 'focking', 'frack', 'fuckbrain', 'fuck', 'fuckbutt', 'fucka', 'fucke', 'fucked', 'fucken', 'fucker', 'fuckface', 'fuckhead', 'fuckheads', 'fuckhed', 'fuckin', 'fucking', 'fuckn', 'fuckup', 'fugglies', 'fuggly', 'fuglies', 'fugly', 'fuk', 'fukin', 'fukk', 'fukka', 'fullmalls', 'fuqing', 'fuuck', 'gayfuck', 'gaybob', 'gaytard', 'gaywad', 'gtfo', 'golem', 'goniff', 'gooch', 'gook', 'gringo', 'hag', 'hardon', 'heb', 'hebe', 'heii', 'honkee', 'honkey', 'honkie', 'honky', 'hore', 'horseshit', 'jackass', 'japs', 'jordaner', 'kike', 'kneegro', 'kneegrow', 'kraphammer', 'krapphammer', 'leftard', 'lesbo', 'lezbo', 'libtard', 'libtarded', 'libtardism', 'lmfwao', 'milf', 'masterbate', 'masturbate', 'masturbating', 'mcfagget', 'minge', 'mothaf', 'motherfuck', 'motherfucken', 'mothafuckin', 'motherfucker', 'motherfuckers', 'motherfuckin', 'motherfucking', 'negress', 'nigga', 'niggah', 'niggard', 'niggardly', 'niggaz', 'nigger', 'niggers', 'niggger', 'nigs', 'nigletnutsack', 'penisenlargement', 'penises', 'piss', 'porno', 'pos', 'progtards', 'panooch', 'prick', 'pussies', 'pussy', 'puzzy', 'retard', 'retarded', 'renob', 'rimjob', 'raghead', 'repiblitarded', 'republitard', 'republiturd', 'republotard', 'republotarded', 'republotards', 'repuglitard', 'repuglotard', 'repuglotarded', 'sandnigger', 'schlimazel', 'schlimiel', 'shti', 'shite', 'shiitehead', 'shiitehold', 'shit', 'shitbaggers', 'shitface', 'shitfaced', 'shithead', 'shithed', 'shithole', 'shitting', 'shitty', 'shyt', 'shyte', 'skank', 'skeet', 'slut', 'sluttt', 'slutty', 'spic', 'stfu', 'sthefu', 'tard', 'teatard', 'teatardist', 'teatards', 'tit', 'titties', 'titty', 'towelhead', 'turd', 'twat', 'vaginal', 'wetback', 'whore', 'whoring', 'wop', 'yokel', 'teabagger', 'tea-bagger', 't-bagger', 'teebagger', 'tee-bagger', 'tbagger', 'teabagged', 'tea-bagged', 't-bagged', 'teebagged', 'tee-bagged', 'tbagged', 'teabagging', 'tea-bagging', 't-bagging', 'teebagging', 'tee-bagging', 'tbagging', 'moochelle', 'tabernac', 'wanker', 'schlong', 'wank', 'whore', 'whorebag', 'queef']

gray_words = ['axewound', 'axwound', 'beaner', 'blow', 'blue waffle', 'boner', 'bs', 'cleveland steamer', 'crappy', 'cornhole', 'cracker', 'damn', 'darwin', 'dick', 'dike', 'dumb', 'erection', 'fat', 'fatter', 'fatty', 'flamer', 'fudge packer', 'fudgepacker', 'gay', 'get some squish', 'glass bottom boat', 'ghetto', 'goddamn', 'goddamnit', 'guido', 'hairy axe wound', 'hard on', 'halfrican', 'hanged', 'heeb', 'hell', 'hildabadeast', 'ho', 'hoodrat', 'hoodrats', 'hoe', 'homo', 'homos', 'hooker', 'idiot', 'jack off', 'jacking off', 'jap', 'jerk', 'jigaboo', 'jungle bunny', 'junglebunny', 'kraut', 'kyke', 'lesbian', 'lezzie', 'lynch', 'lynching', 'make brown bubbles', 'meat flap', 'meds', 'medication', 'messiah', 'mick', 'moron', 'muff', 'muncher', 'muzzie', 'nappy', 'nut butter', 'pecker', 'penis', 'pissed', 'pollock', 'porch monkey', 'porchmonkey', 'pube', 'pubtard', 'puto', 'queer', 'ruski', 'rusty trombone', 'sex', 'sheet', 'sodomite', 'sodomy', 'spick', 'spook', 'steralize', 'sterilize', 'sterilization', 'sterilized', 'suck', 'tart', 'testicle', 'towel head', 'vagina', 'whitey', 'wtf']

if __name__ == '__main__':
    print build_single_regex(build_regex(banned_words[:], special_character_representations))
    # print build_single_regex(build_regex(gray_words[:], special_character_representations))
