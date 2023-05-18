function inject_menu() {
  const menu = document.createElement('div');
  menu.setAttribute('id', 'LearnMate_menu');
  img_url = chrome.runtime.getURL('menu_image.gif');
  menu.innerHTML = `
    <img id="LearnMate_img" src="${img_url}" />
  `;
  document.body.appendChild(menu);
}

inject_menu();