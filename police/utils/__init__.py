from police.utils.utils import build_regex, build_single_regex, special_character_representations
from police.utils.utils import banned_words, gray_words
from re import compile, I

gray_word_string = build_single_regex(build_regex(gray_words, special_character_representations))
black_word_string = build_single_regex(build_regex(banned_words, special_character_representations))

# Compile with I(gnore case)
gray_word_regex = compile(gray_word_string, I)
black_word_regex = compile(black_word_string, I)
