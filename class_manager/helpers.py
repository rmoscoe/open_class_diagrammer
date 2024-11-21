import spectra

def flatten_dict(original_dict, parent_key=""):
    items = []
    for key, value in original_dict.items():
        new_key = f"{parent_key}/{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_dict(value, new_key).items())
        else:
            items.append((new_key, value))
    return dict(items)

def prepare_dict_for_form(subdict):
    choices = []
    for key, value in subdict.items():
        if isinstance(value, dict):
            choices.extend((prepare_dict_for_form(value)))  # Grouping by key
        else:
            choices.append((key, value))  # Individual choice
    return choices

def build_color_theme(hex_string):
    theme = { "primary_color": hex_string }
    base_color = spectra.html(hex_string)
    white = spectra.html("#ffffff")
    black = spectra.html("#000000")
    print(base_color.to("hsl").values)
    content_color = base_color.blend(white, 0.65) if base_color.to("hsl").values[2] < .70 else base_color.blend(white, 0.3)
    content_color = content_color.darken(10) if content_color.to("hsl").values[2] > .95 else content_color
    theme["content_color"] = content_color.hexcode
    border_color = base_color.blend(white, 0.85) if base_color.to("hsl").values[2] < .80 else base_color.blend(black, .25)
    theme["border_color"] = border_color.hexcode
    dark_primary_color = base_color.saturate(5) if base_color.to("hsl").values[1] < .95 else base_color
    dark_primary_color = dark_primary_color.brighten(5) if base_color.to("hsl").values[2] < .95 else dark_primary_color
    dark_primary_color = dark_primary_color.blend(black, 0.1) if dark_primary_color.hexcode == hex_string else dark_primary_color
    theme["dark_primary_color"] = dark_primary_color.hexcode
    dark_content_color = content_color.saturate(5) if content_color.to("hsl").values[1] < .95 else content_color
    dark_content_color = dark_content_color.brighten(5) if content_color.to("hsl").values[2] < .95 else dark_content_color
    dark_content_color = dark_content_color.blend(black, 0.1) if dark_content_color.hexcode == content_color.hexcode else dark_content_color
    theme["dark_content_color"] = dark_content_color.hexcode
    dark_border_color = border_color.saturate(5) if border_color.to("hsl").values[1] < .95 else border_color
    dark_border_color = dark_border_color.brighten(5) if dark_border_color.to("hsl").values[2] < .95 else dark_border_color
    dark_border_color = dark_border_color.blend(black, 0.1) if dark_border_color.hexcode == border_color.hexcode else dark_border_color
    theme["dark_border_color"] = dark_border_color.hexcode
    return theme