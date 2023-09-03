for (const clipboard_button of document.querySelectorAll("clipboard-copy")) {
    clipboard_button.addEventListener('click', function(event) {
        event.preventDefault();
        var for_id = clipboard_button.getAttribute('for');
        var copyText = document.getElementById(for_id);
        var ishidden = copyText.hasAttribute('type') && copyText.type =='hidden';
        if (ishidden) { copyText.type = 'text'; }
        copyText.select();
        document.execCommand("copy");
        if (ishidden) { copyText.type = 'hidden'; }
        for (const details of document.querySelectorAll("details")) {
            details.removeAttribute("open");
        }
  })
}
