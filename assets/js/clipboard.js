function copy() {
  var copyText = document.getElementById("gist-share-url");
  copyText.select();
  document.execCommand("copy");
}

const clipboard = document.getElementById("clipboard");
if (typeof(clipboard) != 'undefined' && clipboard != null)
{
  clipboard.addEventListener('click', copy);
}
