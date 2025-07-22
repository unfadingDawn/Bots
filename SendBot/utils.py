def check_correctness(text: str) -> bool:
    parts = text.split('\n')
    for part in parts:
        refs = part.split('_')
        if len(refs) != 2:
            return False
        if refs[0][0] != '"' or refs[1][len(refs[1]) - 1] != '"' or refs[0][len(refs[0]) - 1] != '"' or refs[1][
            0] != '"':
            return False
    return True


def add_link_to_file(path: str, link: str) -> bool:
    if check_correctness(link):
        with open(path, "a") as file:
            file.write(f'{link}\n')
            return True
    else:
        return False


def parse_word_from_braces(text: str) -> str:
    result = ''
    for i in range(1, len(text) - 1):
        result += text[i]
    return result


def parse_link(link: str) -> str:
    result: str = ''
    parts = link.split('_')
    result += f'<a href={parts[0]}>'
    result += f'{parse_word_from_braces(parts[1].split('\n')[0])}</a>\n'
    return result


def parse_chat_id(text: str):
    return int(parse_word_from_braces(text.split('_')[2].split('\n')[0]))


def parse_button(text: str) -> (str, str):
    parts = text.split('_')
    first = parse_word_from_braces(parts[0].split('\n')[0])
    second = parse_word_from_braces(parts[1].split('\n')[0])
    return first, second


def find_link(text: str, link: str) -> str | None:
    parts = text.split('\n')
    for i in range(0, len(parts)):
        found_link = parse_word_from_braces(parts[i].split('_')[0])
        if found_link == link:
            return parts[i]
    return None

def delete_link(path: str, link: str = "", name: str = ""):
    new_text= ''
    if name == '':
        with open(path, "r") as file:
            text = file.read()
            parts = text.split('\n')
            for i in range(0, len(parts)):
                if link != parse_word_from_braces(parts[i].split('_')[0].split('\n')[0]):
                    new_text += f'{parts[i]}\n'
        with open(path, "w") as file:
            file.write(new_text)
    if link == '':
        with open(path, "r") as file:
            text = file.read()
            parts = text.split('\n')
            for i in range(0, len(parts)):
                if parts[i] != '' and name != parse_word_from_braces(parts[i].split('_')[1]):
                    new_text += f'{parts[i]}\n'
        with open(path, "w") as file:
            file.write(new_text)


def clean_file(path: str):
    with open(path, "w") as file:
        file.write('')

