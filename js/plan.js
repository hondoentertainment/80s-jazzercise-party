(function () {
  "use strict";

  var STATUS_KEY = "jjp-plan-status";
  var adminCode = sessionStorage.getItem("jjp-admin-code") || "";
  var plan = window.JJP_PLAN || {};

  var codeForm = document.getElementById("plan-code-form");
  var codeInput = document.getElementById("plan-code");
  var dashboard = document.getElementById("plan-dashboard");
  var statusEl = document.getElementById("plan-status");
  var subtitle = document.getElementById("plan-subtitle");
  var summary = document.getElementById("plan-summary");
  var categoryFilter = document.getElementById("plan-category-filter");
  var tasksBody = document.getElementById("plan-tasks-body");
  var scheduleBody = document.getElementById("plan-schedule-body");
  var signsList = document.getElementById("plan-signs-list");
  var committeeList = document.getElementById("plan-committee-list");
  var meta = document.getElementById("plan-meta");

  var statusOptions = ["Not Started", "In Progress", "Done"];

  function setStatus(message, type) {
    if (!statusEl) {
      return;
    }
    statusEl.textContent = message;
    statusEl.className = "form-note" + (type ? " form-note--" + type : "");
  }

  function loadStatuses() {
    try {
      return JSON.parse(localStorage.getItem(STATUS_KEY) || "{}");
    } catch (error) {
      return {};
    }
  }

  function saveStatuses(statuses) {
    localStorage.setItem(STATUS_KEY, JSON.stringify(statuses));
  }

  function getTaskStatus(task) {
    var saved = loadStatuses();
    return saved[String(task.id)] || task.status || "Not Started";
  }

  function statusClass(status) {
    return "plan-status plan-status--" + status.toLowerCase().replace(/\s+/g, "-");
  }

  function renderSummary(tasks) {
    if (!summary) {
      return;
    }

    var counts = { total: tasks.length, done: 0, inProgress: 0, notStarted: 0 };
    tasks.forEach(function (task) {
      var status = getTaskStatus(task);
      if (status === "Done") {
        counts.done += 1;
      } else if (status === "In Progress") {
        counts.inProgress += 1;
      } else {
        counts.notStarted += 1;
      }
    });

    summary.innerHTML =
      '<p class="plan-summary__title">' +
      (plan.title || "Party Planning") +
      "</p>" +
      '<div class="plan-summary__stats">' +
      '<span><strong>' +
      counts.done +
      "</strong> done</span>" +
      '<span><strong>' +
      counts.inProgress +
      "</strong> in progress</span>" +
      '<span><strong>' +
      counts.notStarted +
      "</strong> not started</span>" +
      '<span><strong>' +
      counts.total +
      "</strong> total tasks</span>" +
      "</div>";
  }

  function renderTasks(filterCategory) {
    if (!tasksBody) {
      return;
    }

    var tasks = (plan.tasks || []).filter(function (task) {
      return !filterCategory || task.category === filterCategory;
    });

    tasksBody.innerHTML = "";
    tasks.forEach(function (task) {
      var row = document.createElement("tr");
      var currentStatus = getTaskStatus(task);
      var options = statusOptions
        .map(function (option) {
          return (
            '<option value="' +
            option +
            '"' +
            (option === currentStatus ? " selected" : "") +
            ">" +
            option +
            "</option>"
          );
        })
        .join("");

      row.innerHTML =
        "<td>" +
        task.id +
        "</td>" +
        '<td><span class="plan-category">' +
        task.category +
        "</span></td>" +
        "<td>" +
        task.task +
        "</td>" +
        '<td><select class="plan-status-select" data-task-id="' +
        task.id +
        '" aria-label="Status for task ' +
        task.id +
        '">' +
        options +
        "</select></td>" +
        "<td>" +
        task.assigned +
        "</td>" +
        "<td>" +
        (task.notes || "—") +
        "</td>";
      tasksBody.appendChild(row);
    });

    tasksBody.querySelectorAll(".plan-status-select").forEach(function (select) {
      select.addEventListener("change", function () {
        var statuses = loadStatuses();
        statuses[select.dataset.taskId] = select.value;
        saveStatuses(statuses);
        renderSummary(plan.tasks || []);
      });
    });

    renderSummary(plan.tasks || []);
  }

  function renderSchedule() {
    if (!scheduleBody) {
      return;
    }

    scheduleBody.innerHTML = "";
    (plan.schedule || []).forEach(function (item) {
      var row = document.createElement("tr");
      row.innerHTML =
        "<td>" +
        item.day +
        "</td>" +
        "<td>" +
        item.time +
        "</td>" +
        "<td>" +
        item.action +
        "</td>";
      scheduleBody.appendChild(row);
    });
  }

  function renderSigns() {
    if (!signsList) {
      return;
    }

    signsList.innerHTML = "";
    (plan.signs || []).forEach(function (item) {
      var li = document.createElement("li");
      li.innerHTML =
        "<span>" +
        item.name +
        '</span><span class="plan-qty">× ' +
        item.quantity +
        "</span>";
      signsList.appendChild(li);
    });
  }

  function renderCommittee() {
    if (!committeeList) {
      return;
    }

    committeeList.innerHTML = "";
    (plan.committee || []).forEach(function (member) {
      var li = document.createElement("li");
      li.innerHTML =
        "<strong>" +
        member.name +
        "</strong><span>" +
        member.role +
        "</span>";
      committeeList.appendChild(li);
    });
  }

  function renderCategories() {
    if (!categoryFilter) {
      return;
    }

    var categories = [];
    (plan.tasks || []).forEach(function (task) {
      if (task.category && categories.indexOf(task.category) === -1) {
        categories.push(task.category);
      }
    });

    categories.sort().forEach(function (category) {
      var option = document.createElement("option");
      option.value = category;
      option.textContent = category;
      categoryFilter.appendChild(option);
    });

    categoryFilter.addEventListener("change", function () {
      renderTasks(categoryFilter.value);
    });
  }

  function renderAll() {
    if (subtitle && plan.subtitle) {
      subtitle.textContent = plan.subtitle;
    }

    if (meta) {
      meta.textContent =
        "Source: " +
        (plan.sourceFile || "Project workbook") +
        (plan.exportedAt ? " · Exported " + new Date(plan.exportedAt).toLocaleString() : "") +
        " · Status changes save in this browser only.";
    }

    renderCategories();
    renderTasks("");
    renderSchedule();
    renderSigns();
    renderCommittee();
  }

  function unlockDashboard() {
    if (codeForm) {
      codeForm.classList.add("is-hidden");
    }
    if (dashboard) {
      dashboard.classList.remove("is-hidden");
    }
    renderAll();
  }

  if (adminCode) {
    if (codeInput) {
      codeInput.value = adminCode;
    }
    unlockDashboard();
  }

  if (codeForm) {
    codeForm.addEventListener("submit", function (event) {
      event.preventDefault();
      adminCode = codeInput ? codeInput.value.trim() : "";
      if (!adminCode) {
        setStatus("Enter the admin code.", "error");
        return;
      }

      fetch("/api/poll?admin=1&code=" + encodeURIComponent(adminCode))
        .then(function (response) {
          return response.json().then(function (data) {
            if (!response.ok) {
              throw new Error(data.error || "Invalid admin code.");
            }
            return data;
          });
        })
        .then(function () {
          sessionStorage.setItem("jjp-admin-code", adminCode);
          setStatus("Planning site unlocked.", "success");
          unlockDashboard();
        })
        .catch(function (error) {
          setStatus(error.message || "Invalid admin code.", "error");
        });
    });
  }
})();
