import gradio as gr
import regex as re
import unicodedata

from modules import script_callbacks


brackets_opening = '([{<'
brackets_closing = ')]}>'

brackets_opening = '([{<'
brackets_closing = ')]}>'

# base = r'(?:\\[()\[\]{}<>]|[^,(){}\[\]{}<>])+'
# paren = r'\(+' + base + r'\)+'
# square = r'\[+' + base + r'\]+'
# curly = r'{+' + base + r'}+'
# angle = r'<+' + base + r'>+'


# re_tokenize = re.compile('|'.join([base, paren, square, curly, angle]))
re_tokenize = re.compile(r',')
re_brackets_fix_whitespace = re.compile(r'([\(\[{<])\s*|\s*([\)\]}>}])')
re_opposing_brackets = re.compile(r'([)\]}>])([([{<])')
re_networks = re.compile(r'<.+?>')
re_brackets_open = re.compile(r'[(\[{]+')
# re_colon_spacing_composite = re.compile(r'(?P<A>[^:]*?)\s*?(?P<COLON>:)\s*?(?P<B>\S*)(?P<S>\s*)(?(S)\s*?)(?P<AND>AND)')
re_colon_spacing_composite = re.compile(r'\s*(:)\s*(?=\d*?\.?\d*?\s*?AND)')
re_colon_spacing = re.compile(r'\s*(:)\s*')
# re_colon_spacing = re.compile(r'(?P<A>[^:]*?)\s*?(?P<COLON>:)\s*?(?P<B>\S+)(?P<S>\s*)(?(S)\s*?)')
re_colon_spacing_comp_end = re.compile(r'(?<=AND[^:]*?)(:)(?=[^:]*$)')
re_comma_spacing = re.compile(r',+')
re_paren_weights_exist = re.compile(r'\(.*(?<!:):\d.?\d*\)+')
re_is_prompt_editing = re.compile(r'\[.*:.*\]')
re_is_prompt_alternating = re.compile(r'\[.*|.*\]')
re_is_wildcard = re.compile(r'{.*}')
re_AND = re.compile(r'(.*?)\s*(AND)\s*(.*?)')
re_alternating = re.compile(r'\s*(\|)\s*')

ui_prompts = []


def get_bracket_closing(c: str):
    return brackets_closing[brackets_opening.find(c)]


def get_bracket_opening(c: str):
    return brackets_opening[brackets_closing.find(c)]


def normalize_characters(data: str):
    return unicodedata.normalize("NFKC", data)


def tokenize(data: str):
    return re_tokenize.findall(data)


def remove_whitespace_excessive(prompt: str):
    return ' '.join(prompt.split())

    # pruned = [' '.join(token.strip().split()) for token in tokens]
    # pruned = list(filter(None, pruned))
    # return pruned


def align_brackets(prompt: str):
    def helper(match: re.Match):
        return match.group(1) or match.group(2)

    return re_brackets_fix_whitespace.sub(helper, prompt)

    # return list(map(lambda token : re_brackets_fix_whitespace.sub(helper, token), tokens))


def space_AND(prompt: str):
    def helper(match: re.Match):
        return ' '.join(match.groups())

    return re_AND.sub(helper, prompt)


def align_colons(prompt: str):
    def normalize(match: re.Match):
        return match.group(1)
    
    def composite(match: re.Match):
        return ' ' + match.group(1)
    
    def composite_end(match: re.Match):
        print(f'match: {match}')
        return ' ' + match.group(1)

    ret = re_colon_spacing.sub(normalize, prompt)
    ret = re_colon_spacing_composite.sub(composite, ret)
    ret = re_colon_spacing_comp_end.sub(composite_end, ret)
    return ret

    # def helper(match: re.Match):
    #     if match.group('AND'):
    #         return f"{match.group('A')} :{match.group('B')} AND"
        
    #     return f"{match.group('A')}:{match.group('B')}"

    # def edge_case(match: re.Match):
    #     # edge case where if composite with weight at end, fix alignment
    #     if match.group('AND'):
    #         return ' '.join(match.group('AND', 2)) + ' ' + ''.join(match.group(3, 4))

    # ret = re_colon_spacing.sub(helper, prompt)
    # return re_colon_spacing_comp_end.sub(edge_case, ret)

    # def fix_ending_compositing(s: str):
    #     # edge case where if composite, weight isn't followed by AND, need to
    #     # check backwards and check if needs to fix alignment
    #     match = re_colon_spacing_comp_end.match(s)
    #     if match.group('AND'):
    #         return ' '.join(match.group(1, 2)) + ' ' + ''.join(match.group(3, 4))

    # ret = re_colon_spacing.sub(helper, prompt)
    # return fix_ending_compositing(ret)


def align_commas(prompt: str):
    split = re_comma_spacing.split(prompt)
    split = map(str.strip, split)
    split = filter(None, split)
    return ', '.join(split)


def brackets_to_weights(tokens: list, power: int = 0):
    print(tokens)
    ret = []
    re_opening_paren = re.compile('\([^\(]')
    re_opening_square = re.compile('\[[^\[]')
    
    for token in tokens:
        if re_opening_paren.match(token):
            pass
        

    # Assumes colons have already been spaced corretly
    # def normalize(token:str):
    #     pass
        # if not re_brackets_open.match(token):
        #     return token
        
        # brackets = re_brackets_open.match(token).group(0)
        # power = len(brackets) if not brackets[0] == '[' else -len(brackets)
        # depth = abs(power)

        # if (re_paren_weights_exist.search(token) or
        #     re_is_prompt_editing.search(token) or
        #     re_is_wildcard.search(token) or
        #     re_is_prompt_alternating.search(token)):
        #     return str(brackets[0] + token[depth:len(token)-depth] + get_bracket_closing(brackets[0]))     # just return normalized bracketing
        
        # weight = 1.1 ** power
        # return '(' + token[depth:len(token)-depth] + ('' if token[-depth-1:-depth] == ':' else ':') + f'{weight:.2f}' + ')'


    # return list(map(normalize, tokens))


def extract_networks(tokens: list):
    return list(filter(lambda token: re_networks.match(token), tokens))


def remove_networks(tokens: list):
    return list(filter(lambda token : not re_networks.match(token), tokens))


def remove_mismatched_brackets(prompt: str):
    stack = []
    pos = []
    ret = ''
    
    for i, c in enumerate(prompt):
        if c in brackets_opening:
            stack.append(c)
            pos.append(i)
            ret += c
        elif c in brackets_closing:
            if not stack:
                continue
            if stack[-1] == brackets_opening[brackets_closing.index(c)]:
                stack.pop()
                pos.pop()
                ret += c
        else:
            ret += c
    
    while stack:
        bracket = stack.pop()
        p = pos.pop()
        ret = ret[:p] + ret[p+1:]
    
    return ret


# Tokenizing is extremely tedious and perhaps unecessary...
# def tokenize_nested(prompt: str):
#     """
#     Tokenizes the prompt based on commas, brackets, and parenthesis.
#     """
#     result = []
#     re_dividers = re.compile(r'(?<!\\)([\(\)\[\],<>{}])')

#     pos = 0
#     while pos < len(prompt):
#         match = re_dividers.search(prompt, pos)
#         # we know we're at the end of the string when we can't match
#         if match is None:
#             substring = prompt[pos:].strip()
#             if substring:
#                 result.append(substring)
#             break
        
#         # add up to the previous token up to excluding our matched position
#         substring = prompt[pos:match.start()].strip()
#         if substring:
#             result.append(prompt[pos:match.start()].strip())
#             if prompt[match.start()] in '}>':    # brackets don't get added, so this corrects for it
#                 result[-1] = get_bracket_opening(prompt[match.start()]) + result[-1] + prompt[match.start()]
        
#         # if comma, move pos past it
#         if prompt[match.start()] in ',<>{}':     
#             pos = match.end()
        
#         # finally deal with real nested stuff
#         elif prompt[match.start()] in '[(':
#             nested_result, length = tokenize_nested(prompt[match.end():])    # recurses with s, the end of match onwards
#             nested_result[0] = prompt[match.start()] + nested_result[0]
#             result.append(nested_result)
#             pos = match.end() + length
#         elif prompt[match.start()] in '])':                                  
#             result[-1] = result[-1] + prompt[match.start()]                  # return from recurse, including the
#             return result, match.end()                                  # end of the match to correct position
#     return result


# def flatten_tokens(tokens: list):
#     ret = []
#     for token in tokens:
#         if isinstance(token, list):
#             ret.extend(flatten_tokens(token))
#         else:
#             ret.append(token)

#     return ret


def space_bracekts(prompt: str):
    def helper(match : re.Match):
        print(' '.join(match.groups()))
        return ' '.join(match.groups())

    print(prompt)
    return re_opposing_brackets.sub(helper, prompt)


def align_alternating(prompt:str):
    def helper(match: re.Match):
        return match.group(1)

    return re_alternating.sub(helper, prompt)


def format_prompt(*prompts: list):
    ret = []
    for prompt in prompts:
        # Clean up the string
        prompt = normalize_characters(prompt)
        prompt = remove_mismatched_brackets(prompt)

        # Clean up whitespace for cool beans
        prompt = remove_whitespace_excessive(prompt)
        prompt = align_brackets(prompt)
        prompt = space_AND(prompt)      # for proper compositing alignment on colons
        prompt = space_bracekts(prompt)
        prompt = align_colons(prompt)
        prompt = align_commas(prompt)
        prompt = align_alternating(prompt)

        # Further processing for usability
        # prompt = brackets_to_weights(prompt)
        # networks = extract_networks(tokens)
        # tokens = remove_networks(tokens)
        # tokens.extend(networks)

        # tokens = flatten_tokens(tokens)
        # ret.append(', '.join(list(tokens)))
        ret.append(prompt)
    
    return ret


def on_before_component(component: gr.component, **kwargs: dict):
    if 'elem_id' in kwargs:
        if kwargs['elem_id'] in ['txt2img_prompt', 'txt2img_neg_prompt', 'img2img_prompt', 'img2img_neg_prompt']:
            ui_prompts.append(component)
        elif kwargs['elem_id'] == 'paste':
            with gr.Blocks(analytics_enabled=False) as ui_component:
                button = gr.Button(value='🪄', elem_classes='tool', elem_id='format')
                button.click(
                    fn=format_prompt,
                    inputs=ui_prompts,
                    outputs=ui_prompts
                )
                return ui_component


script_callbacks.on_before_component(on_before_component)