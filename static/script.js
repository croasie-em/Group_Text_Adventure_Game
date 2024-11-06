document.getElementById("startButton").addEventListener("click", function() {
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("intro").innerHTML = data.intro;
        document.getElementById("location_desc").innerHTML = data.location_desc;
        document.getElementById("inventory_desc").innerHTML = data.inventory_desc;
        document.getElementById("gameContent").style.display = "block"; // Corrected ID to "gameContent"
        document.getElementById("startButton").style.display = "none"; // Hide start button
    });
});



document.getElementById('submitAction').onclick = function() {
    const action = document.getElementById('actionInput').value;
    fetch('/process_action', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({action: action})
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('location_desc').innerHTML = data.location_desc;
        document.getElementById('inventory_desc').innerHTML = data.inventory_desc;
        document.getElementById('message').innerHTML = data.message;
        document.getElementById('actionInput').value = '';
    });
};