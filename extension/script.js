let quiz_enabled = false

function create_chatBubble() {
  const div = document.createElement("div");

  div.id = "talkbubble";

  // Set the class name of the div element.
  div.className = "talk-bubble tri-right border round btm-left-in";

  // Create a new div element for the talk text.
  const talkTextDiv = document.createElement("div");

  // Set the class name of the talk text div element.
  talkTextDiv.className = "talktext";

  // Create a new paragraph element for the talk text.
  const paragraph = document.createElement("p");

  // Set the text content of the paragraph element.
  paragraph.innerHTML = "Take a Quiz on this topic! <br>"; 

  const button = document.createElement("button");
  button.textContent = "<Take Quiz>";

  paragraph.appendChild(button);

  // Append the paragraph element to the talk text div element.
  talkTextDiv.appendChild(paragraph);

  // Append the talk text div element to the main div element.
  div.appendChild(talkTextDiv);

  button.addEventListener('click', () => {
    if (quiz_enabled) {
      inject_quiz_iframe();
    }
    else {
      alert('Generating quiz...');
    }
  });

  return div;
}

function inject_menu() {
  const menu = document.createElement('div');
  menu.setAttribute('id', 'LearnMate_menu');
  img_url = chrome.runtime.getURL('static/menu_image.gif');
  console.log(img_url);
  menu.innerHTML = `
    <img id="LearnMate_img" src="${img_url}" />
  `;
  const bubble = create_chatBubble()
  bubble.style.display = 'none';
  menu.addEventListener('click', () => {
    if (bubble.style.display === 'block') {
      bubble.style.display = 'none';
    }
    else {
      bubble.style.display = 'block';
    }
  });
  menu.appendChild(bubble);
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
  quiz_enabled = true;
}


// inject_quiz_iframe();


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