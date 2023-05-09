// txt2img and img2img tools are created as a row. With Python, we can only create
// our button before the row, not within the row. This will move the format button
// into the row.
onUiLoaded(() => {
	let txt2img_tools = gradioApp().querySelector("#txt2img_tools");
	let txt2img_formatter = txt2img_tools.querySelector("#format")
	let txt2img_tools_row = txt2img_tools.querySelector("div:first-of-type");
	txt2img_tools_row.insertBefore(txt2img_formatter, txt2img_tools_row.firstChild)

	let img2img_tools = gradioApp().querySelector("#img2img_tools");
	let img2img_formatter = img2img_tools.querySelector("#format")
	let img2img_tools_row = img2img_tools.querySelector("div:first-of-type");
	img2img_tools_row.insertBefore(img2img_formatter, img2img_tools_row.firstChild)
})

