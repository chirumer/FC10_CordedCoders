function inject_menu() {
  const menu = document.createElement('div');
  menu.setAttribute('id', 'LearnMate_menu');
  img_url = chrome.runtime.getURL('static/menu_image.gif');
  console.log(img_url);
  menu.innerHTML = `
    <img id="LearnMate_img" src="${img_url}" />
  `;
  document.body.appendChild(menu);
}

inject_menu();

function inject_quiz_iframe() {
  const iframe = document.createElement('iframe');
  iframe.setAttribute('id', 'LearnMate_quiz_iframe');
  iframe.setAttribute('src', chrome.runtime.getURL('static/quiz_iframe.html'));
  document.body.appendChild(iframe);
}

inject_quiz_iframe();