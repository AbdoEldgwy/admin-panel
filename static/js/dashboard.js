function openEditModal(id, name, mail, phone, fields, status, evaluation_point) {
    document.getElementById('editModal').style.display = 'block';
    document.getElementById('candidateId').value = id;
    document.getElementById('name').value = name;
    document.getElementById('mail').value = mail;
    document.getElementById('phone').value = phone;
    document.getElementById('fields').value = fields;
    document.getElementById('status').value = status;
    document.getElementById('evaluation_point').value = evaluation_point;
}

function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target == document.getElementById('editModal')) {
    closeModal();
    }
}

// Handle edit form submission
document.getElementById('editForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    const candidateId = formData.get('candidate_id');

    fetch(`/admin-dashboard/candidate/${candidateId}/edit/`, {
    method: 'POST',
    body: formData,
    headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
    })
    .then(response => response.json())
    .then(data => {
    if (data.status === 'success') {
        alert('Candidate updated successfully');
        location.reload();
    } else {
        alert('Error: ' + data.message);
    }
    })
    .catch(error => {
    alert('Error: ' + error);
    });
});

// Handle delete
function deleteCandidate(id) {
    if (confirm('Are you sure you want to delete this candidate?')) {
    fetch(`/admin-dashboard/candidate/${id}/delete/`, {
        method: 'POST',
        headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
        alert('Candidate deleted successfully');
        location.reload();
        } else {
        alert('Error: ' + data.message);
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
    }
}

// Select All Checkbox Functionality
document.getElementById('selectAll').addEventListener('change', function() {
    const checkboxes = document.getElementsByClassName('row-checkbox');
    for (let checkbox of checkboxes) {
        checkbox.checked = this.checked;
    }
    updateDeleteButton();
});

// Individual Checkbox Functionality
document.querySelectorAll('.row-checkbox').forEach(checkbox => {
    checkbox.addEventListener('change', function() {
        updateDeleteButton();
        updateSelectAllCheckbox();
    });
});

// Update Delete Button Text
    function toggleCheckboxes(source) {
    checkboxes = document.getElementsByName('selected_ids');
    for (let i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = source.checked;
    }
    }
// Update Select All Checkbox State
function updateSelectAllCheckbox() {
    const checkboxes = document.querySelectorAll('.row-checkbox');
    const selectAllCheckbox = document.getElementById('selectAll');
    const checkedBoxes = document.querySelectorAll('.row-checkbox:checked');
    
    selectAllCheckbox.checked = checkboxes.length === checkedBoxes.length;
    selectAllCheckbox.indeterminate = checkedBoxes.length > 0 && checkedBoxes.length < checkboxes.length;
}

document.getElementById('aiFilterForm').addEventListener('submit', function(e) {
  e.preventDefault();

  const btn = document.getElementById('aiFilterBtn');
  const progress = document.getElementById('filterProgress');
  btn.disabled = true;
  progress.style.display = 'block';
  progress.innerText = 'Filtering started...';

  fetch(this.action, {
    method: 'POST',
    headers: {
      'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
    }
  }).then(response => response.body.getReader())
    .then(reader => {
      let decoder = new TextDecoder();
      let buffer = '';

      function read() {
        reader.read().then(({ done, value }) => {
          if (done) {
            progress.innerText = '✅ Filtering completed. Reloading...';
            setTimeout(() => window.location.reload(), 2000);
            return;
          }
          buffer += decoder.decode(value, { stream: true });
          const lines = buffer.split('\n');
          buffer = lines.pop(); // keep the last incomplete line

          for (const line of lines) {
            if (line.startsWith('PROGRESS:')) {
              progress.innerText = line.replace('PROGRESS:', '').trim();
            }
          }
          read();
        });
      }
      read();
    });
});
