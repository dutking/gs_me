async function drawPlot(path) {
    const response = await fetch(path)
    const spec_data = await response.json()

    if ("bookmarks" in spec_data) {
        const bookmarks_path = path.replace("spec.json", "bookmarks.json")
        spec_data.bookmarks.remote.url = bookmarks_path
    }

    if ("purity" in spec_data) setPurity(spec_data.purity)
    if ("ploidy" in spec_data) setPloidy(spec_data.ploidy)

    console.log(spec_data)
    const container = document.querySelector(".container")
    window.GSAPI = await genomeSpyApp.embed(container, spec_data)
    insertSelector()
}

window.setPurity = (purity) => {
    window.customSelector.querySelector("#purity").innerText = purity
}

window.setPloidy = (ploidy) => {
    window.customSelector.querySelector("#ploidy").innerText = ploidy
}

function insertSelector() {
    const target = document.querySelector(
        ".container genome-spy-bookmark-button"
    )
    target.after(window.customSelector)
}

window.addEventListener("load", async () => {
    console.log("Page loaded")
    const selector = document.querySelector(".order-selector")

    if (selector) {
        selector.addEventListener("change", async function () {
            const path = this.value
            window.currentPath = path
            console.log(window.currentPath)
            await window.GSAPI.finalize()
            window.GSAPI = null

            const container = document.querySelector(".container")
            container.innerHTML = ""
            const newContainer = document.createElement("div")
            newContainer.className = "container"
            container.parentNode.replaceChild(newContainer, container)

            await drawPlot(path)
        })

        const first_path = document.querySelector(
            ".order-selector option:first-child"
        ).value
        window.currentPath = first_path
        console.log(window.currentPath)
        window.customSelector = document.querySelector(".selector-container")
        await drawPlot(first_path)
    }
})
