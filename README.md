![Demonstration](/demo/demo.gif)
# sd_extension-prompt_formatter
This is an extension that adds a magic button next to your prompt to make it look neat and "optimized." It does several things.
1. Normalizes letters/symbols/etc to their standardized equivalent for compatability ([NFKC](https://en.wikipedia.org/wiki/Unicode_equivalence#Normal_forms))
2. Fixes commas 
3. Removes excessive whitespace
4. Normalizes brackets to their minimum matching pair
5. Converts nested brackets to a single bracket weight
6. Moves networks to the end of the prompt

Works for txt2img and img2img for both positive and negative prompts. **Also respects escaped brackets.**

**Example**

Raw prompt
```
photorealistic   photo of a handsome male (wizard  :1.2）， <lora:LuisapHotlineStyle:0.5> <lora:ElegantHanfuRuqunStyle:0.2>    short beard, white wizard  shirt, (with golden    trim:0.8), (((bald))
```

Formatted
```
photorealistic photo of a handsome male, (wizard:1.2), short beard, white wizard shirt, (with golden trim:0.8), (bald:1.21), <lora:LuisapHotlineStyle:0.5>, <lora:ElegantHanfuRuqunStyle:0.2>
```

Inspiration from taken from [canisminor1990/sd-webui-kitchen-theme](https://github.com/canisminor1990/sd-webui-kitchen-theme)'s prompt formatter.

## Installation
1. In your Stable Diffusion Web UI, navigate to **Extensions** > **Install from URL**
2. Copy and paste this repository to the URL install
	`https://github.com/uwidev/sd_extension-prompt_formatter`
3. Install
4. Go to the **Installed** tab and click **Apply and restart UI**

## Other planned(?) features in no particular order
- [ ] A `Revert` button just in case it formats it incorrectly (and my logic be funky) ⏫
- [ ] Option to convert token spaces to underscore
- [ ] Update the top right token counter so that it's not red on prompt format (need to learn javascript for that one it seems)
- [ ] Somehow magically resolve mixed bracketing (e.g. `([<1girl>])` who types their prompts like this?!1)
- [ ] Option to normalize brackets to their maximum matching pair (e.g. `(((a` -> `(((a)))`
