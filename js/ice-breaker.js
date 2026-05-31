const QUESTIONS = [
  "What's the most iconic piece of your 80s workout outfit tonight — and where did you find it?",
  "Richard Simmons or Jane Fonda — who would you rather have lead your warm-up, and why?",
  "What's the most embarrassing gym or aerobics class story you still tell at parties?",
  "If this room suddenly became a Jazzercise video, what would the title of tonight's workout be?",
  "What's a totally normal thing that secretly makes you want to do jumping jacks?",
  "Which 80s hit would you pick for the group high-kick finale?",
  "What's the weirdest workout fad you've ever tried — and did it work?",
  "If someone here challenged you to a headband showdown, leg-warmer duel, or sweatband sprint, which are you accepting first?",
  "What's your signature aerobics move when nobody's watching?",
  "What's the dumbest way you've ever injured yourself while \"getting in shape\"?",
  "Neon pink, electric purple, or highlighter yellow — what's your power color for maximum sweat?",
  "If you could throw a party with any fitness theme imaginable, what would it be?",
  "What's the most unhinged post-workout snack combination you've ever eaten?",
  "Who at this party would you trust to lead the grapevine during the group warm-up?",
  "What's one 80s fashion trend you're glad stayed in the 80s — and one you're bringing back tonight?",
];

(function () {
  "use strict";

  var grid = document.getElementById("ice-breaker-grid");
  var shuffleBtn = document.getElementById("ice-breaker-shuffle");

  function renderQuestions(questions) {
    if (!grid) {
      return;
    }

    grid.innerHTML = "";
    questions.forEach(function (question, index) {
      var item = document.createElement("li");
      item.className = "ice-breaker-card";
      item.innerHTML =
        '<span class="ice-breaker-card__number" aria-hidden="true">' +
        (index + 1) +
        '</span><p class="ice-breaker-card__text">' +
        question +
        "</p>";
      grid.appendChild(item);
    });
  }

  function shuffleQuestions() {
    var shuffled = QUESTIONS.slice();
    for (var i = shuffled.length - 1; i > 0; i -= 1) {
      var j = Math.floor(Math.random() * (i + 1));
      var temp = shuffled[i];
      shuffled[i] = shuffled[j];
      shuffled[j] = temp;
    }
    renderQuestions(shuffled);
  }

  renderQuestions(QUESTIONS);

  if (shuffleBtn) {
    shuffleBtn.addEventListener("click", shuffleQuestions);
  }
})();
