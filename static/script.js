// Function to initialize the game and display the starting information
function play_game() {
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("message").innerHTML = data.intro;
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
        document.querySelector(".start-button").style.display = "none";
    });
}

// Function to handle directional movement (north, south, east, west)
function goDirection(direction) {
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: `go ${direction}` })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("message").innerHTML = data.message;
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}

// Function to quit the game
function quitGame() {
    document.getElementById("message").innerHTML = "You have quit the game.";
    document.getElementById("game-output").innerHTML = "";
}

// Function to display inventory
function showInventory() {
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'inventory' })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("inventory").innerHTML = data.inventory_desc;
        document.getElementById("message").innerHTML = data.message;
    });
}


function startGame() {
    // Hide the Start Game button
    document.querySelector('.start-button').style.display = 'none';

    // Show the game content
    document.getElementById('game-content').style.display = 'block';

    // Optionally, start the game logic on the backend
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.intro;
        document.getElementById("message").innerHTML = data.location_desc;
    });
}
