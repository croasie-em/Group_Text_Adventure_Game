// Function to add a typewriter effect to the text element with a specified ID
// The function will simulate typing each character one by one for a better user experience
function typewriter(elementId, speed = 50) {
    const element = document.getElementById(elementId);
    if (!element) {
        console.error(`Element with ID "${elementId}" not found.`);
        return;
    }

    // Extract the text content from the element and clear it for the effect
    const text = element.innerText || element.textContent;
    element.innerHTML = ''; // Clear existing content

    let i = 0;
    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, speed); // Call the type function recursively
        }
    }
    type(); // Start the typing effect
}

// Initialize the typewriter effect once the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    typewriter('intro-text', 20);
});

// Function to start the game, hiding the start button and showing the game content
function startGame() {
    document.querySelector('.start-button').style.display = 'none';
    document.getElementById('game-content').style.display = 'block';

    // Send request to start a new game
    fetch('/start_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Update game details and introduction message
        document.getElementById("game-output").innerHTML = data.location_desc;
        document.getElementById("message").innerHTML = data.intro;
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
            document.getElementById("message").innerHTML = "";
        }

        // Check if the victory message is in the response
        if (data.victory) {
            // Display a victory message and reset the game state
            document.getElementById("game-content").style.display = "none";
            document.querySelector('.start-button').style.display = 'block';
            document.getElementById("message").style.color = "green";
            document.getElementById("message").innerHTML = "Congratulations! You have successfully navigated to the forest edge and completed your adventure! 🎉";
        }
    });
}

// Function to take an item specified by the player
function takeItem() {
    const itemInput = document.getElementById("item");
    const item = itemInput.value.trim();

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
        // Update the location description and feedback message
        document.getElementById("game-output").innerHTML = data.location_desc;
        if (data.message) {
            document.getElementById("message").innerHTML = data.message;
        }

        // Clear the input field
        itemInput.value = "";
    });
}


// Function to show or hide the inventory
function showInventory() {
    fetch('/process_action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: 'inventory' })
    })
    .then(response => response.json())
    .then(data => {
        const inventoryBox = document.getElementById("inventory-box");
        inventoryBox.innerHTML = data.inventory_desc;

        // Toggle the visibility of the inventory box
        if (inventoryBox.style.display === "none" || inventoryBox.style.display === "") {
            inventoryBox.style.display = "block";
        } else {
            inventoryBox.style.display = "none";
        }
    });
}

// Function to quit the game, resetting all game-related elements
function quitGame() {
    fetch('/quit_game', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Display the quit message and clear game output
        if (data.message) {
            document.getElementById("message").innerHTML = data.message;
        }
        document.getElementById("game-output").innerHTML = "";
        document.getElementById("inventory-box").innerHTML = "";

        // Hide game content and show start button to allow a new game to begin
        document.getElementById('game-content').style.display = 'none';
        document.querySelector('.start-button').style.display = 'block';
    })
    .catch(error => {
        console.error("Error quitting game:", error);
        document.getElementById("message").innerHTML = "An error occurred while quitting the game. Please try again.";
    });
}
