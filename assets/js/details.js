for (const button of document.querySelectorAll(".file-navigation-options .select-menu-item")) {
    button.addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById("gist-share-url").setAttribute('value', button.getAttribute('value'));
        document.getElementById("details-title").innerHTML = button.getAttribute('title');
        document.getElementById("details").removeAttribute("open");
        for (const octicon of document.querySelectorAll(".select-menu-item-icon")) {
            octicon.style.visibility='hidden';
        }
        for (const octicon of button.querySelectorAll(".select-menu-item-icon")) {
            octicon.style.visibility='inherit';
        }
  })
}

for (const dropdown_item of document.querySelectorAll(".dropdown-item")) {
    dropdown_item.addEventListener('click', function(event) {
        for (const details of document.querySelectorAll("details")) {
            details.removeAttribute("open");
        }
  })
}





