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
  const iframe = document.createElement('iframe');
  iframe.setAttribute('id', 'LearnMate_quiz_iframe');
  iframe.setAttribute('src', chrome.runtime.getURL('static/quiz_iframe.html'));
  document.body.appendChild(iframe);
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