let sectionIndex = 0;
const data = {
  skills: [
    {
      skill: "Python",
      questions: [
        {
          question: "Which of the following is a key feature of Python?",
          correct: ["Interpreted language"],
          wrong: ["Compiled language", "Statically typed", "Verbose syntax"],
        },
        {
          question: "What is the purpose of the 'import' statement in Python?",
          correct: [
            "To include and use modules or packages in a Python script",
          ],
          wrong: [
            "To define a new variable",
            "To create a new function",
            "To handle exceptions",
          ],
        },
        {
          question:
            "Which of the following is a built-in data structure in Python?",
          correct: ["List"],
          wrong: ["Array", "Vector", "Tuple"],
        },
        {
          question: "What is the purpose of the 'try-except' block in Python?",
          correct: ["To handle exceptions and errors in a program"],
          wrong: [
            "To define a new function",
            "To create a loop",
            "To import a module",
          ],
        },
        {
          question:
            "Which of the following is a common way to read data from a file in Python?",
          correct: ["Using the 'open()' function and 'read()' method"],
          wrong: [
            "Using the 'input()' function",
            "Using the 'print()' function",
            "Using the 'write()' method",
          ],
        },
      ],
    },
    {
      skill: "TensorFlow",
      questions: [
        {
          question: "What is the primary purpose of TensorFlow?",
          correct: ["To build and deploy machine learning models"],
          wrong: [
            "To manage databases",
            "To create web applications",
            "To perform data visualization",
          ],
        },
        {
          question:
            "Which of the following is a key component of the TensorFlow architecture?",
          correct: ["Tensor"],
          wrong: ["Array", "Matrix", "Scalar"],
        },
        {
          question:
            "What is the purpose of the 'tf.keras' module in TensorFlow?",
          correct: [
            "To provide a high-level API for building and training neural networks",
          ],
          wrong: [
            "To handle image processing",
            "To perform data preprocessing",
            "To deploy models as web services",
          ],
        },
        {
          question:
            "Which of the following is a common activation function used in TensorFlow models?",
          correct: ["ReLU (Rectified Linear Unit)"],
          wrong: ["Sigmoid", "Tanh", "Softmax"],
        },
        {
          question: "What is the role of the 'tf.data' module in TensorFlow?",
          correct: [
            "To provide a flexible and efficient way to load and preprocess data for machine learning models",
          ],
          wrong: [
            "To handle model deployment",
            "To perform hyperparameter tuning",
            "To visualize model performance",
          ],
        },
      ],
    },
    {
      skill: "Deep Learning",
      questions: [
        {
          question: "What is the primary goal of deep learning?",
          correct: ["To learn complex patterns and representations from data"],
          wrong: [
            "To perform linear regression",
            "To handle structured data",
            "To build rule-based systems",
          ],
        },
        {
          question:
            "Which of the following is a common type of deep learning model?",
          correct: ["Convolutional Neural Network (CNN)"],
          wrong: ["Decision Tree", "Random Forest", "Linear Regression"],
        },
        {
          question:
            "What is the purpose of the backpropagation algorithm in deep learning?",
          correct: [
            "To update the weights of a neural network during training",
          ],
          wrong: [
            "To preprocess data",
            "To visualize model performance",
            "To deploy models in production",
          ],
        },
        {
          question:
            "Which of the following is a key hyperparameter in deep learning models?",
          correct: ["Learning rate"],
          wrong: ["Correlation coefficient", "Variance", "Entropy"],
        },
        {
          question: "What is the role of regularization in deep learning?",
          correct: ["To prevent overfitting and improve model generalization"],
          wrong: [
            "To handle missing data",
            "To perform feature selection",
            "To optimize model architecture",
          ],
        },
      ],
    },
    {
      skill: "Flask",
      questions: [
        {
          question: "What is the primary purpose of the Flask web framework?",
          correct: ["To build web applications and RESTful APIs"],
          wrong: [
            "To perform data analysis",
            "To create mobile apps",
            "To manage databases",
          ],
        },
        {
          question:
            "Which of the following is a key component of a Flask application?",
          correct: ["Routes"],
          wrong: ["Threads", "Databases", "Caching"],
        },
        {
          question: "How do you define a route in a Flask application?",
          correct: ["Using the '@app.route()' decorator"],
          wrong: [
            "Using the 'import' statement",
            "Using the 'class' keyword",
            "Using the 'def' keyword",
          ],
        },
        {
          question: "What is the purpose of the 'request' object in Flask?",
          correct: ["To access data from the client-side request"],
          wrong: [
            "To handle database connections",
            "To render HTML templates",
            "To manage user sessions",
          ],
        },
        {
          question: "How do you render HTML templates in a Flask application?",
          correct: ["Using the 'render_template()' function"],
          wrong: [
            "Using the 'print()' function",
            "Using the 'open()' function",
            "Using the 'write()' function",
          ],
        },
      ],
    },
    {
      skill: "Web Development",
      questions: [
        {
          question:
            "What is the primary purpose of HTML (Hypertext Markup Language)?",
          correct: ["To define the structure and content of web pages"],
          wrong: [
            "To add interactivity to web pages",
            "To style web pages",
            "To handle server-side logic",
          ],
        },
        {
          question: "Which of the following is a key component of a web page?",
          correct: ["HTML elements"],
          wrong: ["Database tables", "Python functions", "Mobile app screens"],
        },
        {
          question:
            "What is the role of CSS (Cascading Style Sheets) in web development?",
          correct: ["To control the presentation and styling of web pages"],
          wrong: [
            "To handle user input",
            "To perform data analysis",
            "To manage server-side processes",
          ],
        },
        {
          question:
            "Which of the following is a common way to add interactivity to web pages?",
          correct: ["Using JavaScript"],
          wrong: ["Using SQL", "Using Flask", "Using TensorFlow"],
        },
        {
          question: "What is the purpose of a web server in web development?",
          correct: [
            "To handle and respond to client requests for web pages and resources",
          ],
          wrong: [
            "To perform data preprocessing",
            "To train machine learning models",
            "To manage user authentication",
          ],
        },
      ],
    },
  ],
};

$(document).ready(function () {
  let sections = "";
  data.skills.forEach((skill, skillIndex) => {
    if (skillIndex == 0) {
      sections +=
        "<li class='nav-item'><a class='nav-link active ' aria-current='page' href='#''>" +
        skill.skill +
        "</a></li>";
    } else {
      sections +=
        "<li class='nav-item'><a class='nav-link' aria-current='page' href='#''>" +
        skill.skill +
        "</a></li>";
    }
  });

  $("#sections").append(sections);

  $(".nav-link").on("click", function (event) {
    $(".nav-link").each(function (index, element) {
      $(element).removeClass("active");
    });
    $(this).addClass("active");
    const skillIndex = $(this).data("skill-index");
    displayQuestions(sectionIndex++);
  });

  displayQuestions(sectionIndex++);

  $(".option").click(function () {
    console.log("clicked");
    $(this).css("border-color", "#FDBA04");
    $(this).css("box-shadow", "0 0 5px 2px #FDBA04");
  });
});

function displayQuestions(skillIndex) {
  const questionsContainer = $("#question-container");
  questionsContainer.empty();
  const skill = data.skills[skillIndex];

  skill.questions.forEach((q, qIndex) => {
    let questionHtml = `<div class="mt-3"><h4>${qIndex + 1}. ${
      q.question
    }</h4><div class="container my-5"><div class="options row"><div class="row justify-content-evenly mb-5">`;
    let options = q.correct.concat(q.wrong);
    shuffle(options);

    options.forEach((option, optionIndex) => {
      questionHtml += `<div class="option col-4">${option}</div>`;
      if (optionIndex == 1) {
        questionHtml += '</div><div class="row justify-content-evenly">';
      }
    });
    questionHtml += "</div></div></div></div>";
    questionsContainer.append(questionHtml);
  });
}

function shuffle(array) {
  let currentIndex = array.length;

  // While there remain elements to shuffle...
  while (currentIndex != 0) {
    // Pick a remaining element...
    let randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex],
      array[currentIndex],
    ];
  }
}
