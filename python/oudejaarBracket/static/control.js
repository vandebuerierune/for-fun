let selectedTeam = null;

function selectTeam() {
    selectedTeam = document.getElementById('team-select').value;
    fetch('/select_team', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team: selectedTeam }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById('overlay').style.display = 'none';
            document.getElementById('actions').style.display = 'block';
            document.getElementById('actions-heading').innerText = `${selectedTeam}, select your action`;
        }
    });
}

function reportWin() {
    fetch('/report_win', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team: selectedTeam }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Win reported successfully!');
            window.location.href = '/';  // Reload the bracket page
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function reportChallenge() {
    fetch('/report_challenge', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Challenge completed reported successfully!');
        } else {
            alert(`Error: ${data.error}`);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('overlay');
    const actions = document.getElementById('actions');
    const selectHeading = document.getElementById('select-heading');
    const actionsHeading = document.getElementById('actions-heading');
    const teamSelect = document.getElementById('team-select');

    window.selectTeam = selectTeam;
    window.reportWin = reportWin;
    window.reportChallenge = reportChallenge;
});