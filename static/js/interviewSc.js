function toggle_Checkboxes() {
  document.querySelector('.custom-multiselect').classList.toggle('active');
}

// Global checkboxes for count display
const top_Checkboxes = document.querySelectorAll('.checkboxes input[type="checkbox"]');
top_Checkboxes.forEach(cb => {
  cb.addEventListener('change', () => {
    const count = Array.from(topCheckboxes).filter(c => c.checked).length;
    document.getElementById('selectedCount').innerText = count > 0 ? `${count} Selected` : "Select Fields";
  });
});


function openPopup() {
    document.getElementById("interviewPopup").style.display = "flex";
}
function closePopup() {
    document.getElementById("interviewPopup").style.display = "none";
}

function toggleDropdown(btn) {
  btn.classList.toggle("open");
  const list = btn.nextElementSibling;
  list.style.display = btn.classList.contains("open") ? "block" : "none";
}

// Inside DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
  const list = document.querySelector(".list-items");
  if (!list) return;

  const dropdownCheckboxes = list.querySelectorAll("input[type='checkbox']");
  const btnText = document.querySelector(".btn-text");

  function updateText() {
    const count = Array.from(dropdownCheckboxes).filter(cb => cb.checked).length;
    btnText.innerText = count > 0 ? `${count} Selected` : "Select Fields";
  }

  dropdownCheckboxes.forEach(cb => cb.addEventListener("change", updateText));
  updateText();
});

function addInterviewCard(session) {
  const container = document.getElementById("interviewCardSection");

  const card = document.createElement("div");
  card.className = "col";
  card.id = `card-${session.id}`;

  card.innerHTML = `
    <div class="card border-success shadow-sm">
      <div class="card-body">
        <h5 class="card-title text-success">${session.job}</h5>
        <p class="card-text"><strong>Status:</strong> ${session.status}</p>
        <p class="card-text"><strong>Duration:</strong> ${session.duration} mins</p>
        <p class="card-text"><strong>Scheduled:</strong> ${session.scheduled_at}</p>
        <p class="card-text"><strong>Ends:</strong> ${session.ended_at}</p>

        <form method="POST" action="${session.delete_url}" onsubmit="return confirmDelete(event, ${session.id})">
          <input type="hidden" name="csrfmiddlewaretoken" value="${document.querySelector('[name=csrfmiddlewaretoken]').value}">
          <button type="submit" class="btn btn-danger btn-sm mt-2">Delete</button>
        </form>
      </div>
    </div>
  `;

  container.prepend(card);
}


document.querySelector("form").addEventListener("submit", function (e) {
  e.preventDefault(); // prevent form from submitting (for demo)
  
  // Fake data (replace with actual form values)
  const session = {
    job: document.querySelector("#id_job").selectedOptions[0].text,
    status: document.querySelector("#id_status").value,
    duration: document.querySelector("#id_duration_minutes").value,
    scheduled_at: document.querySelector("#id_scheduled_date").value + ' ' + document.querySelector("#id_scheduled_time").value,
    ended_at: document.querySelector("#id_ended_date").value + ' ' + document.querySelector("#id_ended_time").value
  };

  addInterviewCard(session); // Inject card

  // You can submit the form here if needed
  // this.submit();
});

function confirmDelete(event, sessionId) {
  event.preventDefault();

  if (confirm("Delete this session?")) {
    fetch(`/InterviewScheduling/delete/${sessionId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(res => {
      if (res.ok) {
        document.getElementById(`card-${sessionId}`).remove();
      } else {
        alert("Delete failed.");
      }
    });
  }
  return false;
}
