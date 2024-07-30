$(document).ready(function () {
  const ctx = document.getElementById("myChart");
  const data = {
    labels: ["January", "February", "March", "April", "May", "June", "July"],
    datasets: [
      {
        label: "My First Dataset",
        data: [65, 59, 80, 81, 56, 55, 40],
        fill: false,
        borderColor: "rgb(75, 192, 192)",
        tension: 0.1,
      },
    ],
  };
  new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      width: "200px",
      height: "200px",
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });

  $("#profile-completion").mouseover(function () {
    $("#progress-value").text("Fill");
  });

  $("#profile-completion").mouseleave(function () {
    $("#progress-value").text("50%");
  });

  $("#profile-completion").click(function () {
    $('#staticBackdrop').modal('show');
  });

  function formatState (state) {
    if (!state.id) {
      return state.text;
    }
    var $state = $(
      '<span class="text-dark text-start">' + state.text + '</span>'
    );
    return $state;
  };

  $('#staticBackdrop').on('shown.bs.modal', function () {
    $('.js-example-basic-multiple').select2({
      placeholder: "Select your skills",
      dropdownParent: $('#staticBackdrop'),
      templateResult: formatState,
      templateSelection: formatState
    });
  });

  //   $('#profile-completion').click(function () {

  const daysInYear = 365;
  const submissions = Array.from({ length: daysInYear }, () =>
    Math.floor(Math.random() * 10)
  ); // Example submission data
  const startDate = new Date(new Date().getFullYear(), 0, 1);
  const streakTracker = $(".streak-tracker");
  const daysInMonth = [
    31,
    new Date(startDate.getFullYear(), 1, 29).getDate(),
    31,
    30,
    31,
    30,
    31,
    31,
    30,
    31,
    30,
    31,
  ]; // Handling leap years

  let dayCounter = 0;
  let htmlContent = "";
  for (let monthIndex = 0; monthIndex < daysInMonth.length; monthIndex++) {
    htmlContent += '<div class="month">'; // Add opening month div

    for (let day = 0; day < daysInMonth[monthIndex]; day++) {
      const submissionCount = submissions[dayCounter] || 0;
      let streakClass = "";

      if (submissionCount > 0 && submissionCount <= 2) {
        streakClass = "active-1";
      } else if (submissionCount > 2 && submissionCount <= 5) {
        streakClass = "active-2";
      } else if (submissionCount > 5 && submissionCount <= 8) {
        streakClass = "active-3";
      } else if (submissionCount > 8) {
        streakClass = "active-4";
      }

      htmlContent += `<div class="streak-box ${streakClass}" title="${submissionCount} submissions"></div>`;

      dayCounter++;
    }
    htmlContent += "</div>"; // Add closing month div
  }

  streakTracker.html(htmlContent);
});
