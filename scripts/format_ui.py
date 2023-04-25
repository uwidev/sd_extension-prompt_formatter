import gradio as gr
import re
import unicodedata

from modules import script_callbacks


bracketing = '([{<)]}>'

none = r'(?:\\[()\[\]{}<>]|[^,(){}\[\]{}<>])+'
paren = r'\(+' + none + r'\)+'
square = r'\[+' + none + r'\]+'
curly = r'{+' + none + r'}+'
angle = r'<+' + none + r'>+'

re_tokenize = re.compile('|'.join([none, paren, square, curly, angle]))
re_brackets_fix_whitespace = re.compile(r'\s*[^\\\S]([\(<{\)>}:]+)\s*')
re_networks = re.compile(r'<.+?>')
re_brackets_open = re.compile(r'[(\[{]+')

ui_prompts = []


def get_closing(c: str):
    return bracketing[bracketing.find(c) + len(bracketing)//2]


def fix_bracketing(token: str):
    # token should always have at least 1 matching pair
    # tokenizer() should always ensure that's always the case
    if not re.match(r'[\(\[{<]', token):
        return token
    
    stack = []
    ret = list(token)

    opening = ret[0]
    closing = get_closing(opening)
    
    for i, c in enumerate(token):
        if token[i] == opening:
            stack.append(i)
        elif token[i] == closing:
            if stack:
                stack.pop()
            else:
                ret[i] = ''

    while stack:
        ret.pop(stack.pop())
    
    return ''.join(ret)


def normalize(data: str):
    return unicodedata.normalize("NFKC", data)


def tokenize(data: str):
    return re_tokenize.findall(data)


def remove_whitespace(tokens: list):
    pruned = [' '.join(token.strip().split()) for token in tokens]
    pruned = list(filter(None, pruned))
    return list(map(lambda token : re_brackets_fix_whitespace.sub(r"\1", token), pruned))


def min_normalized_brackets(tokens: list):
    return list(map(fix_bracketing, tokens))


def brackets_to_weights(tokens: list):
    return list(map(token_bracket_to_weight, tokens))


def token_bracket_to_weight(token:str):
    # If weighting already exists, just get rid of excess brackets
    if not re_brackets_open.match(token):
        return token
    
    brackets = re_brackets_open.match(token).group(0)
    power = len(brackets) if brackets[0] in '{(' else -len(brackets)
    depth = abs(power)

    if re.search(r':\d+.?\d*', token):
        return token[depth-1:len(token)-1 if depth == 1 else - depth]
    
    weight = 1.1 ** power
    return token[depth-1:len(token)-1 if depth == 1 else -depth] + ('' if token[-depth-1:-depth] == ':' else ':') + f'{weight:.2f}' + get_closing(brackets[0])


def extract_networks(tokens: list):
    return list(filter(lambda token: re_networks.match(token), tokens))


def remove_networks(tokens: list):
    return list(filter(lambda token : not re_networks.match(token), tokens))


def format_prompt(*prompts: list):
    ret = []
    for prompt in prompts:
        prompt_norm = normalize(prompt)
        tokens = tokenize(prompt_norm)
        tokens = remove_whitespace(tokens)
        tokens = min_normalized_brackets(tokens)
        tokens = brackets_to_weights(tokens)
        networks = extract_networks(tokens)
        tokens = remove_networks(tokens)
        tokens.extend(networks)
        ret.append(', '.join(list(tokens)))
    
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