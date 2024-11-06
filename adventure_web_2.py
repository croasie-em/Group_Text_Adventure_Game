from flask import Flask, render_template, request, jsonify

app = Flask(__name__)
app.secret_key = '12345'

# Define initial game variables
locations = {
    'entrance': {
        'name': 'The Temple Entrance',
        'description': 'A grand archway leads into a dark and mysterious temple.',
        'directions': {'north': 'hallway'},
        'items': []
    },
    'hallway': {
        'name': 'A dimly lit Hallway',
        'description': 'Torches flicker on the walls, casting long shadows. There are doors to the east and west.',
        'directions': {'east': 'chamber', 'west': 'library', 'south': 'entrance'},
        'items': []
    },
    'chamber': {
        'name': 'The Treasury',
        'description': 'A room glittering with gold. The legendary treasure awaits here.',
        'directions': {'west': 'hallway'},
        'items': ['treasure']
    }
}

# Game state variables
current_location = 'entrance'
inventory = []

# Game functions
def show_intro():
    return "Welcome to the Temple Adventure! Seek the hidden treasure deep within the temple."

def show_current_location():
    loc = locations[current_location]
    description = f"<h3>You are in {loc['name']}.</h3><p>{loc['description']}</p>"
    if loc['items']:
        items = "<p>You see the following items:</p><ul>" + "".join(f"<li>{item}</li>" for item in loc['items']) + "</ul>"
        description += items
    return description

def move_player(direction):
    global current_location
    new_location = locations[current_location]['directions'].get(direction)
    if new_location:
        current_location = new_location
        return show_current_location()
    else:
        return "You cannot go that way."

def take_item(item):
    loc = locations[current_location]
    if item in loc['items']:
        inventory.append(item)
        loc['items'].remove(item)
        return f"You have taken the {item}."
    else:
        return "No such item here."

def show_inventory():
    if inventory:
        return "<p>Your inventory:</p><ul>" + "".join(f"<li>{item}</li>" for item in inventory) + "</ul>"
    else:
        return "Your inventory is empty."

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    global current_location, inventory
    current_location = 'entrance'
    inventory.clear()
    return jsonify({
        'intro': show_intro(),
        'location_desc': show_current_location(),
        'inventory_desc': show_inventory()
    })

@app.route('/process_action', methods=['POST'])
def process_action():
    global current_location
    action = request.json.get('action', '').lower()
    if action.startswith("go"):
        direction = action.split()[-1]
        message = move_player(direction)
    elif action.startswith("take"):
        item = action.split()[-1]
        message = take_item(item)
    elif action == "inventory":
        message = show_inventory()
    else:
        message = "Invalid action."

    return jsonify({
        'location_desc': show_current_location(),
        'inventory_desc': show_inventory(),
        'message': message
    })

if __name__ == '__main__':
    app.run(debug=True)
