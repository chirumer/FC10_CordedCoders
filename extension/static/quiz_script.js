fetch('http://127.0.0.1:5001/get_questions').then((response) => {
  response.json().then((data) => {


    let quizData = [];

    data.questions.forEach((question) => {
      quizData.push({
        question: question.question,
        answers: [
          {
            id: 1,
            label: question.choices[0],
            correct: question.answer == 0,
          },
          {
            id: 2,
            label: question.choices[1],
            correct: question.answer == 1,
          },
          {
            id: 3,
            label: question.choices[2],
            correct: question.answer == 2,
          },
          {
            id: 4,
            label: question.choices[3],
            correct: question.answer == 3,
          }
        ]
      });
    });



    // const quizData = [
    //   {
    //     question: "In JavaScript, what value is returned by default when a function doesn't have a return statement?",
    //     answers: [
    //       { id: 1, label: "0", correct: false },
    //       { id: 2, label: "null", correct: false },
    //       { id: 3, label: "undefined", correct: true },
    //       { id: 4, label: "-1", correct: false }
    //     ]
    //   },
    //   {
    //     question: "How to write an IF statement in JavaScript?",
    //     answers: [
    //       { id: 1, label: "if i = 5", correct: false },
    //       { id: 2, label: "if (i == 5)", correct: true },
    //       { id: 3, label: "if i == 5 then", correct: false }
    //     ]
    //   },
    //   {
    //     question: "Which event occurs when the user clicks on an HTML element?",
    //     answers: [
    //       { id: 1, label: "onmouseover", correct: false },
    //       { id: 2, label: "onclick", correct: true },
    //       { id: 3, label: "onchange", correct: false },
    //       { id: 4, label: "onmouseclick", correct: false }
    //     ]
    //   },
    //   {
    //     question: "What does SCSS stand for?",
    //     answers: [
    //       { id: 1, label: "Sassy CSS", correct: true },
    //       { id: 2, label: "Super-powered CSS", correct: false },
    //       { id: 3, label: "Sass CSS", correct: false },
    //       { id: 4, label: "Syntactic CSS", correct: false }
    //     ]
    //   }
    // ];
    
    const quizFormElem = document.getElementById("quiz-form");
    const quizContainerElem = document.getElementById("quiz-container");
    const quizTimerElem = document.getElementById("quiz-timer");
    const quizStartBtn = document.getElementById("quiz-start-btn");
    const quizRestartBtn = document.getElementById("quiz-restart-btn");
    
    let quizTime = 0;
    let quizIndex = 0;
    let quizScore = 0;
    let intervalId = null;
    
    quizFormElem.addEventListener("submit", (e) => {
      e.preventDefault();
    
      const quizInputsElems = document.querySelectorAll("input[name='answer']");
      const correctAnswer = findCorrectAnswer(quizInputsElems);
      quizIndex++;
    
      if (quizIndex >= quizData.length) {
        clearInterval(intervalId);
        intervalId = null;
        
        quizContainerElem.innerHTML = evaluateScore(quizScore, quizData.length);
        document.getElementById('quiz_next_btn').remove();

      } 
       else {
        renderQuiz(quizData[quizIndex], quizIndex);
      }
    });
    
    quizStartBtn.addEventListener("click", (e) => {
      e.target.classList.add("hide");
      quizFormElem.classList.remove("hide");
      
      setTimer();
      
      renderQuiz(quizData[quizIndex], quizIndex);
    });
    
    function renderQuiz(data, index) {
      if (!data) return;
    
      const output = `<h3 class="quiz__question"><span class="quiz__number">${
        index + 1
      }.</span> ${data.question}</h3>
        <div class="quiz__answers">
          ${renderQuizAnswers(data.answers)}
        </div>`;
    
      quizContainerElem.innerHTML = output;
    }
    
    function renderQuizAnswers(answers) {
      let output = "";
    
      answers.forEach((answer) => {
        output += `<div class="quiz__answer">
          <input type="radio" id="answer${answer.id}" name="answer" data-correct="${answer.correct}" required />
          <label for="answer${answer.id}">${answer.label}</label>
        </div>`;
      });
    
      return output;
    }
    
    function findCorrectAnswer(quizInputs) {
      for (let i = 0, l = quizInputs.length; i < l; i++) {
        // If answer is correct
        if (quizInputs[i].checked && quizInputs[i].dataset.correct === "true") {
          quizScore++;
          return quizInputs[i];
        }
      }
    
      return null;
    }
    
    function evaluateScore(correctAnswers, questions) {
      const scoreInPercent = Math.floor((correctAnswers / questions) * 100);
      
      return `<h3>Congratulations!</h3>
              <p>You got ${scoreInPercent}% correct</p>`;
    }
    
    function setTimer() {
      const formatTime = (num, str = "0") => num.toString().padStart(2, str);
    
      let seconds = 0;
      let minutes = 0;
    
      if (!intervalId) {
        intervalId = setInterval(() => {
          if (seconds == 60) {
            seconds = 0;
            minutes++;
          }
    
          quizTimerElem.innerHTML = `${formatTime(minutes)}:${formatTime(seconds)}`;
          seconds++;
        }, 1000); // 1000ms = 1s
      }
    }






  });
});