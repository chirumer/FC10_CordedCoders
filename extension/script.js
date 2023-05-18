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

function inject_quiz_iframe() {
  const container = document.createElement('div');
  container.setAttribute('id', 'LearnMate_quiz_container');
  const iframe = document.createElement('iframe');
  iframe.setAttribute('id', 'LearnMate_quiz_iframe');
  iframe.setAttribute('name', 'LearnMate_quiz_iframe');
  iframe.setAttribute('src', chrome.runtime.getURL('static/quiz_iframe.html'));
  const closeButton = document.createElement('div');
  closeButton.className = 'close-button';
  closeButton.style = 'position: absolute; top: 7px; right: 5px; width: 20px; height: 20px; cursor: pointer; z-index: 1002';
  const closeButtonImage = document.createElement('img');
  closeButtonImage.src = chrome.runtime.getURL('static/close_button.png');
  closeButtonImage.alt = 'Close';
  closeButtonImage.style = 'width: 100%; height: 100%;'
  closeButton.appendChild(closeButtonImage);
  closeButton.addEventListener('click', () => {
    iframe.remove();
    closeButton.remove();
  });
  container.appendChild(iframe);
  container.appendChild(closeButton);
  document.body.appendChild(container);
}


function enable_quiz() {
  alert('quiz enabled');
  fetch('http://127.0.0.1:5001/get_questions').then((response) => {
    response.json().then((data) => {
      console.log(data);
    });
  });
}


inject_quiz_iframe();


// function enable_roadmap() {
// }


function main() {
  inject_menu();

  const generate_questions = 'http://127.0.0.1:5001/generate_questions?' + (new URLSearchParams({url: window.location.href}).toString())
  fetch(generate_questions).then(() => {
    enable_quiz();
  });

  // const generate_roadmap = 'http://127.0.0.1:5001/generate_questions?' + (new URLSearchParams({url: 'https://en.wikipedia.org/wiki/Gun#History'}).toString())
  // fetch(generate_questions).then(() => {
  //   enable_roadmap();
  // });
}

main();