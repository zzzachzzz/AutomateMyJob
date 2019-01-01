from pprint import pprint
import pickle
import json
import re
from typing import List, Set
from job import build_data
from job import cif_names_to_build
from job.tagging_paths import get_page_type


def to_html():
    ''.join([s[0:5], '<b>', s[5:7], '<b>', s[7:len(s)]])
    return

# Untagged articles and links that are referenced
# by wrappers are added to the set when identified,
# to prevent being deleted from a ref list.
valid_refs = set()

# Removes elements from components where content was not added.
# Skips appending the component to the cleaned list if the component
# had no content added at all.
def complete_build_section(build_section: List[dict], content_identifiers: Set[str]) -> List[dict]:
    cleaned_build_section = []
    for component in build_section:
        cleaned_build_component = dict(component)  # Create copy of dict for modifying

        if component['type'] == 'article':
            if component.get('title') and component['title'] in content_identifiers:
                del cleaned_build_component['title']
            if component.get('body') and component['body'] in content_identifiers:
                del cleaned_build_component['body']
            if (cleaned_build_component.get('body') or cleaned_build_component.get('title')):
                cleaned_build_section.append(cleaned_build_component)
                if not component.get('tags'):
                    valid_refs.add(component['name'])

        elif component['type'] == 'wrapper':
            cleaned_build_component['ref'] = [x for x in component['ref'] if (x not in content_identifiers or x in valid_refs)]
            if len(cleaned_build_component['ref']) > 0:
                cleaned_build_section.append(cleaned_build_component)

        elif component['type'] == 'image':
            if component['image'] not in content_identifiers:
                cleaned_build_section.append(cleaned_build_component)

    return cleaned_build_section


def get_content_identifiers(build_section: List[dict]) -> Set[str]:
    content_identifiers = set()
    for component in build_section:
        if component['type'] == 'article':
            if component.get('title'):
                content_identifiers.add(component['title'])
            if component.get('body'):
                content_identifiers.add(component['body'])
        elif component['type'] == 'wrapper':
            for x in component['ref']:
                content_identifiers.add(x)
        elif component['type'] == 'image':
            content_identifiers.add(component['image'])
    return content_identifiers


def parse_for_content(sheets_api_response: dict, marsha: str) -> list:
    values = sheets_api_response['values']
    sheet_title = re.search("[^\']*[^\']",
                       sheets_api_response['range']).group()
    print(sheet_title)
    values = [x[0] if len(x) > 0 else '' for x in values]
    # image_replacements = [x[2] if len(x) > 2 else '' for x in values]



    b = build_data.Build(sheet_title, marsha)
    # Get the specific subclass of CIF needed based on page_type
    page_type = get_page_type(sheet_title)
    # Get subclass according to page_type, otherwise
    # default to the base class CIF.
    TargetClass = getattr(cif_names_to_build, page_type.replace(' ', ''),
                          cif_names_to_build.CIF)  # Last argument is default
    cif = TargetClass(b)

    build_sequence = []
    new_build_section = []
    content_identifiers = set()
    i = 0
    while i <= len(values)-1:
        if values[i] == '':
            i += 1

        elif values[i] in cif.names:
            # Complete build_section before beginning next
            if len(new_build_section) > 0:
                new_build_section = complete_build_section(new_build_section, content_identifiers)
                if len(new_build_section) > 0:
                    build_sequence += new_build_section

            new_build_section = cif.names[values[i]]()
            content_identifiers = get_content_identifiers(new_build_section)
            i += 1

        elif values[i] in content_identifiers and values[i+1] != '':
            for component in new_build_section:
                if component['type'] == 'article':
                    if component.get('title') == values[i]:
                        component['title'] = values[i+1]
                    elif component.get('body') == values[i]:
                        component['body'] = values[i+1]
                elif component['type'] == 'wrapper':
                    if values[i] in component['ref']:
                        ref_index = component['ref'].index(values[i])
                        component['ref'][ref_index] = values[i+1]
                elif component['type'] == 'image':
                    component['image'] = values[i+1]
                else:
                    print("Error :thinking:")
            i += 2

        else:
            i += 1

    # Complete last build_section
    if len(new_build_section) > 0:
        new_build_section = complete_build_section(new_build_section, content_identifiers)
        if len(new_build_section) > 0:
            build_sequence += new_build_section

    return build_sequence


if __name__ == '__main__':
    with open('job/resultSample.json', 'r') as f:
        sheets_api_response = json.load(f)
    build_sequence = parse_for_content(sheets_api_response, 'TCISI')
    pprint(build_sequence)
    with open ('job/build_sequence.json', 'w') as f:
        json.dump(build_sequence, f, indent=4)
