document.getElementById('btn').addEventListener('click', function(){
  const val = document.getElementById('inpt').value;
  const url = 'http://127.0.0.1:5001/roadmap?' + (new URLSearchParams({ topic: val })).toString();
  chrome.tabs.create({ url });
  return false;
});