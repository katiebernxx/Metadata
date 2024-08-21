''' Counting number of times each character speaks '''

import re
from collections import defaultdict
import pandas as pd

## Notes: we are identifying character names by if they are all caps and on a single line
    # We do exclude lines with scene descriptors like int and ext to not pick up on setting all caps lines
    # Problems: the scripts are formatted differently and this does not pick up on the line "DADDY and MAMA" for ex because "and" is lowercase
    # This does not work for other formats including the table format

def count_parts(script_text):
    lines = script_text.split('\n')
    part_count = {}
    # word_counts = defaultdict(int)
    # current_characters = []

    # Identifying character names as all caps on a single line, including commas and ampersands
    pattern = re.compile(r'^[A-Z\s,&]+$')

    for line in lines:
        line = line.strip()
        match = pattern.match(line)
        if match:
            # Skip common scene description indicators to prevent matching with all caps setting
            if any(word in line for word in ['INT', 'EXT', 'DAY', 'NIGHT', 'MORNING', 'AFTERNOON', 'EVENING']):
                break
            else:
                # Split the line by commas, ampersands, and ANDs to get individual character names
                characters = [char.strip() for char in re.split('[,&]| AND | and ', line)]
                for character in characters:
                    part_count[character] = part_count.get(character, 0) + 1
    return part_count

def top_three(script_text, verbose = False):
    part_count = count_parts(script_text)
    top_three_keys = [key for key, value in sorted(part_count.items(), key=lambda item: item[1], reverse=True)[:3]]
    # rare_characters = [predefined list]
    # rare_characters_spotted = []
    # for each key in part_count
         # if the key is a character on the rare character list, append that character to rare_characters_spotted
         # return that list as well
    if verbose:
        print(top_three_keys)
    return top_three_keys