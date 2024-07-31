$(document).ready(function () {
  function formatState(state) {
    if (!state.id) {
      return state.text;
    }
    var $state = $(
      '<span class="text-dark text-start">' + state.text + "</span>"
    );
    return $state;
  }

  $(".js-example-basic-multiple").select2({
    placeholder: "Select your skills",
    width: "250px",
    templateResult: formatState,
    templateSelection: formatState,
  });

  $("#skill-search, #role-search").select2({
    placeholder: "Select your Skills/Roles",
    width: "250px",
    templateResult: formatState,
    templateSelection: formatState,
  });

  function filterProjects() {
    var selectedSkills = $("#skill-search").val() || [];
    var selectedRoles = $("#role-search").val() || [];
    var query = $("#filter-query-box").val().toLowerCase();

    selectedSkills = selectedSkills.map((skill) => skill.toLowerCase());
    selectedRoles = selectedRoles.map((role) => role.toLowerCase());

    $(".project-card").each(function () {
      var projectSkills = $(this)
        .data("skills")
        .split(",")
        .map((skill) => skill.toLowerCase());
      var projectRoles = $(this)
        .data("roles")
        .split(",")
        .map((role) => role.toLowerCase());
      var projectTitle = $(this).data("title").toLowerCase();

      var skillMatch =
        selectedSkills.length === 0 ||
        selectedSkills.some((skill) => projectSkills.includes(skill));
      var roleMatch =
        selectedRoles.length === 0 ||
        selectedRoles.some((role) => projectRoles.includes(role));
      var titleMatch = projectTitle.includes(query);

      if (skillMatch && roleMatch && titleMatch) {
        $(this).show();
      } else {
        $(this).hide();
      }
    });
  }

  $("#skill-search, #role-search, #filter-query-box").on(
    "change keyup",
    filterProjects
  );
  $(".filter-submit-btn").on("click", function (e) {
    e.preventDefault();
    filterProjects();
  });
});
