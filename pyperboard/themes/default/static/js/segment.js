document.body.addEventListener("load", initSegmentMenus(), false);

function initSegmentMenus() {

    var segmentMenus = document.getElementsByClassName("segment-menu");

    for (var i = 0; i < segmentMenus.length; i++) {

        var segmentMenu = segmentMenus[i];

        var segmentGroup = segmentMenu.dataset.group;
        var segmentMenuItems = document.querySelectorAll('[id*="' + segmentGroup + '__"]');

        segmentMenuItems.forEach(function (element, index) {
            var itemSegment = element.dataset.segment;
            var menuItem = createSegmentMenuItem(itemSegment, segmentGroup);

            segmentMenu.appendChild(menuItem);

            if (index === 0) {
                menuItem.click();
            }
        });

    }
}

function createSegmentMenuItem(segmentName, segmentGroup) {
    var button = document.createElement('span');
    button.classList.add('segment-menu-item');
    button.innerText = segmentName;
    button.dataset.segment = segmentName;

    button.onclick = function (event) {
        var parentMenu = event.target.parentNode;
        clearSegmentButtonsState(parentMenu);
        event.target.classList.add("is-selected");
        showSegment(segmentName, segmentGroup);
    };

    return button;
}


function clearSegmentButtonsState(parentMenu) {

    var segmentMenuItems = parentMenu.querySelectorAll('.segment-menu-item');

    segmentMenuItems.forEach(function (element) {
        element.classList.remove("is-selected");
    });
}


function showSegment(segmentName, segmentGroup) {
    var segments = document.querySelectorAll('[id*="' + segmentGroup + '__"]');

    segments.forEach(function (element) {
        element.classList.remove("active");
    });

    document.getElementById(segmentGroup + '__' + segmentName).classList.add("active");
}