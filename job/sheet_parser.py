from pprint import pprint
import pickle
from typing import List
from job import build
from job import cif_names_to_build
from job.tagging_paths import get_page_type


def to_html():
    ''.join([s[0:5], '<b>', s[5:7], '<b>', s[7:len(s)]])
    return


def parse_for_content(sheet_title: str, marsha: str, values: List[List[str]]) -> list:
    def complete_build_sequence_piece():
        pass

    b = build.Build(sheet_title, marsha)
    # Get the specific subclass of CIF needed based on page_type
    page_type = get_page_type(sheet_title)
    TargetClass = getattr(cif_names_to_build, page_type.replace(' ', '') )
    cif = TargetClass(b)


    content_identifiers = build.content_identifiers
    build_sequence = []
    i = 0
    # while i <= len(values)-1:
    while i <= 123:
        # If blank cell, shouldn't be any after previous filter
        if values[i] == '':
            i += 1

        elif values[i] in cif.names:
            build_sequence.append( cif.names[values[i]]() )
            i += 1

        # If content identifier
        elif values[i] in content_identifiers and values[i+1] != '':
            for component in build_sequence[-1]:
                if component['type'] == 'article':
                    if component.get('title') == values[i]:
                        component['title'] = values[i+1]
                    elif component.get('body') == values[i]:
                        component['body'] = values[i+1]
                elif component['type'] == 'wrapper':
                    if values[i] in component['ref']:
                        ref_index = component['ref'].index(values[i])
                        component['ref'][ref_index] = values[i+1]
            i += 2

        else:
            i += 1

    return build_sequence


if __name__ == '__main__':
    with open('job/values.pickle', 'rb') as pickle_file:
        values = pickle.load(pickle_file)
    pprint(values)
    print("\n\n")
    parsed = parse_for_content('Hotel Overview', 'TCISI', values)
    print("\n\n\nFinal:")
    pprint(parsed)
