window.onload = () => {
    const formDivs = Array.from(document.querySelectorAll("form > div")).concat(Array.from(document.querySelectorAll("form > fieldset > div")));
    formDivs.forEach(div => {
        const label = div.querySelector("label");
        const input = div.querySelector("input");
        if (input?.hasAttribute("required")) {
            label.classList.add("font-bold");
            const labelText = label.innerText;
            let newLabel = "";
            for (let i = 0; i < labelText.length - 1; i++) {
                newLabel += labelText[i];
            }
            newLabel += "*:";
            label.innerText = newLabel;
        }

        const errorList = div.querySelector("ul.errorlist");
        if (input && errorList) {
            input?.classList.add("invalid");
        } else {
            input?.classList.remove("invalid");
        }

        const helpText = div.querySelector(".helptext");
        if (input?.matches(":focus")) {
            helpText?.classList.remove("hidden");
            helpText?.classList.add("flex");
        } else {
            helpText?.classList.add("hidden");
            helpText?.classList.remove("flex");
        }

        input?.addEventListener("focusout", (event) => {
            if (!event.relatedTarget || !event.relatedTarget.closest('a[href]')) {
                input?.classList.remove("invalid");
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