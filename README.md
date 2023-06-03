![Demonstration](/demo/demo.gif)
plz ignore the bug [smiling:0.91], it's already fixed, gif will update... later!

# sd_extension-prompt_formatter
This is an extension for [AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui) that adds a magic button next to your prompt to make it look neat and "optimized." It does several things.
1. Normalizes the characters to their standard equivalent ([NFKC](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms))
2. Normalizes brackets to their minimum matching pair
3. Removes excessive whitespace
4. Properly spaces commas, bracketing, commas, and `|`
5. Converts nested brackets `((a))` to a single bracket weight `(a:1.21)`

Works for txt2img and img2img for both positive and negative prompts.

*Currenty as of commit 54d57c2 v0.3, may not respect escaped parenthesis and square brackets, and may crash the extension.*

**Example**

Raw Prompt
```
photorealistic   photo of a handsome male (wizard  :1.2）， <lora:LuisapHotlineStyle:0.5> <lora:ElegantHanfuRuqunStyle:0.2>    short beard, white wizard  shirt, (with golden    trim:0.8), (((bald))
```

Formatted
```
photorealistic photo of a handsome male (wizard:1.2), <lora:LuisapHotlineStyle:0.5> <lora:ElegantHanfuRuqunStyle:0.2> short beard, white wizard shirt, (with golden trim:0.8), (bald:1.21)
```

Raw Prompt
```
a, [[b, [c, [A:B], [A|B], [A :1.2 AND B :1.2]], e]]
```

Formatted
```
a, (b, (c, [A:B], [A|B], [A :1.2 AND B :1.2]:0.91), e:0.83)
```


Inspiration from taken from [canisminor1990/sd-webui-kitchen-theme](https://github.com/canisminor1990/sd-webui-kitchen-theme)'s prompt formatter.

## Installation
1. In your Stable Diffusion Web UI, navigate to **Extensions** > **Install from URL**
2. Copy and paste this repository to the URL install

`https://github.com/uwidev/sd_extension-prompt_formatter`

3. Install
4. Go to the **Installed** tab and click **Apply and restart UI**

## Other planned(?) features
- [x] take into account [prompt editing](https://github.com/AUTOMATIC1111/stable-diffusion-webui/wiki/Features#prompt-editing) (do not convert [from:to:when] ⏫ ✅ 2023-04-27
- [x] fix: do not convert {} to () (wildcard fix) ⏫ ✅ 2023-04-27
- [x] handle additional bracekt weighting within nested brackets e.g. ((A), (B)) => ((A, B)) => (A, B:1.21) ✅ 2023-04-27
- [x] Somehow magically resolve mixed bracketing (e.g. `([<1girl>])` who types their prompts like this?!1) ✅ 2023-04-27 **maybe fixed?**
- [ ] Respect new lines (useful when splitting prompt on BREAK)
- [ ] Further simplify `[(a:0.91)]` => `(a:0.83)`, instead of `((a:0.91):0.91)`
- [ ] A `Revert` button just in case it formats it incorrectly (and my logic be funky) 🔼 
- [ ] Have moving networks to the back a option rather than always enforced.
- [x] Extension settings menu.
- [x] Option to convert token spaces to underscore
- [ ] have an option multiple weighted tagged blocks into individual blocks? e.g. (A, B:1.2) => (A:1.2), (B:1.2)
- [ ] Update the top right token counter so that it's not red on prompt format (need to learn javascript for that one it seems)
- [ ] Option to normalize brackets to their maximum matching pair (e.g. `(((a` -> `(((a)))`
- [x] proper testing of prompts for faster development ✅ 2023-04-27
