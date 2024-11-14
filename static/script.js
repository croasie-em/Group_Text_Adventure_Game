// Function to initialize the game and display the starting information
function startGame() {
    document.querySelector('.start-button').style.display = 'none';
    document.getElementById('game-content').style.display = 'block';

    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.location_desc; // Only location details
        document.getElementById("message").innerHTML = data.intro;  // Only introduction message
        document.getElementById("inventory").innerHTML = data.inventory_desc;
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
        // Always update the game-output with the current location description
        document.getElementById("game-output").innerHTML = data.location_desc;

        // Update the message ONLY if there's a message to show
        if (data.message) {
            document.getElementById("message").innerHTML = data.message;
        } else {
            document.getElementById("message").innerHTML = "";  // Clear any previous message
        }

        // Always update the inventory
        document.getElementById("inventory").innerHTML = data.inventory_desc;

        // Check if the victory message is in the response
        if (data.message && data.message.includes("Congratulations! You have successfully navigated to the forest edge")) {
            // Display a victory screen or disable inputs to prevent further actions
            document.getElementById("game-content").style.display = "none";
            document.querySelector('.start-button').style.display = 'block';
            document.getElementById("message").style.color = "green";
        }
    });
}


// Function to take an item
function takeItem() {
    const item = document.getElementById("item").value.trim();
    if (item === "") {
        document.getElementById("message").innerHTML = "Please specify an item to take.";
        return;
    }

    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: `take ${item}` })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("game-output").innerHTML = data.location_desc; // Only location details
        if (data.message) {  // Update feedback message only if there is one
            document.getElementById("message").innerHTML = data.message;
        }
        document.getElementById("inventory").innerHTML = data.inventory_desc;
    });
}

// Function to quit the game
function quitGame() {
    // Send a request to the backend to handle quitting the game
    fetch('/quit_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Update the game output to show the quit message
        if (data.message) {
            document.getElementById("message").innerHTML = data.message;
        }
        document.getElementById("game-output").innerHTML = ""; // Clear game output
        document.getElementById("inventory").innerHTML = ""; // Clear inventory

        // Optionally, hide game content to show that the game has ended
        document.getElementById('game-content').style.display = 'none';
        document.querySelector('.start-button').style.display = 'block'; // Show start button again for restarting
    })
    .catch(error => {
        console.error("Error quitting game:", error);
        document.getElementById("message").innerHTML = "An error occurred while quitting the game. Please try again.";
    });
}

