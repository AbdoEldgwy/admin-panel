function openPopup() {
    document.getElementById("interviewPopup").style.display = "flex";
}
function closePopup() {
    document.getElementById("interviewPopup").style.display = "none";
}


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
