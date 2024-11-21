window.onload = () => {
    const formDivs = Array.from(document.querySelectorAll("form > div")).concat(Array.from(document.querySelectorAll("form > fieldset > div")));
    formDivs.forEach(div => {
        const label = div.querySelector("label");
        const input = div.querySelector("['name']");
        const select = div.querySelector("select");
        const textarea = div.querySelector("textarea");

        const field = input ?? select ?? textarea;
        console.log(`Field: ${field}`);

        if (field?.hasAttribute("required")) {
            label.classList.add("font-bold");
            const labelText = label.innerText;
            let newLabel = "";
            for (let i = 0; i < labelText.length - 1; i++) {
                newLabel += labelText[i];
            }
            newLabel += "*:";
            label.innerText = newLabel;
        }

        // const errorList = div.querySelector("ul.errorlist");
        // if (input && errorList) {
        //     input?.classList.add("invalid");
        // } else {
        //     input?.classList.remove("invalid");
        // }

        const helpText = div.querySelector(".helptext");
        if (field?.matches(":focus")) {
            helpText?.classList.remove("hidden");
            helpText?.classList.add("flex");
        } else {
            helpText?.classList.add("hidden");
            helpText?.classList.remove("flex");
        }

        input?.addEventListener("focusout", (event) => {
            if (!event.relatedTarget || !event.relatedTarget.closest('a[href]')) {
                field?.classList.remove("invalid");
                errorList?.remove();
                helpText?.classList.add("hidden");
                helpText?.classList.remove("flex");
            }
        });

        input?.addEventListener("focusin", (event) => {
            event.stopPropagation();
            helpText?.classList.remove("hidden");
            helpText?.classList.add("flex");
        });
    });
}

const hexToRgb = (hex) => {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? [parseInt(result[1], 16), parseInt(result[2], 16), parseInt(result[3], 16)] : null;
}

const getLuminance = (r, g, b) => {
    const red = 0.2126;
    const green = 0.7152;
    const blue = 0.0722;
    const gamma = 2.4;

    const a = [r, g, b].map((v) => {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, gamma);
    });
    return a[0] * red + a[1] * green + a[2] * blue;
}

const getContrast = (rgb1, rgb2) => {
    const lum1 = getLuminance(...rgb1);
    const lum2 = getLuminance(...rgb2);
    const brighter = Math.max(lum1, lum2);
    const darker = Math.min(lum1, lum2);
    return (brighter + 0.05) / (darker + 0.05);
}

const setTextColor = (hexColor) => {
    const rgbColor = hexToRgb(hexColor);
    const contrastWhite = getContrast([255, 255, 255], rgbColor);
    const contrastBlack = getContrast([0, 0, 0], rgbColor)
    return contrastWhite >= contrastBlack ? "text-black" : "text-white";
}