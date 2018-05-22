tocbot.init({
    tocSelector: '.toc',
    contentSelector: '.content',
    headingSelector: 'h1, h2',
    throttleTimeout: 150,
    scrollSmooth: false
});

initClipboard();
initClipboardToolip();

tippy('.copy-button', {
    theme: 'light',
    arrow: true,
    trigger: 'click',
});

function initClipboard() {
    var clipboard = new ClipboardJS('.copy-button', {
        target: function (trigger) {
            return trigger.previousElementSibling;
        }
    });

    clipboard.on('success', (event) => {
        event.clearSelection();
    });
}

function initClipboardToolip() {
    var codeElements = document.querySelectorAll(".codehilite");
    codeElements.forEach(function (element) {
        var copyButton = document.createElement('button');
        copyButton.classList.add('copy-button');
        copyButton.title = "Copied!";
        element.append(copyButton);
    });

    var copyButtonElements = document.querySelectorAll(".copy-button");
    copyButtonElements.forEach(function (element) {
        element.addEventListener('mouseleave', function (event) {
            var tooltip = event.target._tippy;
            if (tooltip !== null && tooltip.state.visible) {
                tooltip.hide();
            }
        });

    });
}