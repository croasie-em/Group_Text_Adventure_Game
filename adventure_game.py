from flask import Flask, render_template, request, session, jsonify, redirect, url_for
app = Flask(__name__)
app.secret_key = 12345
# Initialise game variables
'''Main game loop'''
locations = {
    'entrance': {
        'name': 'The Temple Entrance',
        'description': 'A grand archway leads into a dark and mysterious temple.',
        'directions': {'north': 'hallway'},
        'items': []  # Optional: add items if needed
    },
    'hallway': {
        'name': 'A dimly lit Hallway',
        'description': 'Torches flicker on the walls, casting long shadows. There are doors to the east and west.',
        'directions': {'east': 'chamber', 'west': 'treasury', 'south': 'entrance'},
        'items': []  # Optional: add items if needed
        },
    'chamber': {
        'name': 'The Treasury',
        'description': 'This is where the legendary treasure is said to be hidden!',
        'directions': {'west': 'hallway'},
        'items': ['treasure']  # Example item
        },
    }
current_location = 'entrance'
inventory = []

# Game functions
def show_intro():
    return '''<p>Welcome to the Adventure of the Hidden Treasure!</p>
              <p>You are an intrepid explorer seeking a legendary treasure hidden deep within an ancient temple.</p>
              <p>Your journey will be fraught with peril, but the rewards are immeasurable.</p>
              <p>Good luck!</p>'''
# Show the current location
def show_current_location(location):
    loc = locations[location]
    description = f"<h3>You are in {loc['name']}.</h3><p>{loc['description']}</p>"
    if 'items' in loc and loc['items']:
        items = "<p>You see the following items:</p><ul>" + "".join(f"<li>{item}</li>" for item in loc['items']) + "</ul>"
        description += items
    return description
# Move the player
def move_player(location, direction, locations):
    '''Moves the player to a new location if possible'''
    new_location = locations[location]['directions'].get(direction)
    if new_location:
        return new_location, ''
    else:
        return location, 'You cannot go that way.'
# Adds an item to the player's inventory
def take_item(location, item):
    if 'items' in locations[location] and item in locations[location]['items']:
        inventory.append(item)
        locations[location]['items'].remove(item)
        return f'You take the {item}.'
    else:
        return 'There is no such item here.'
# Shows the player's inventory
def show_inventory():
    if inventory:
        items = "<p>Your inventory:</p><ul>" + "".join(f"<li>{item}</li>" for item in inventory) + "</ul>"
        return items
    else:
        return '<p>Your inventory is empty.</p>'
# Flask routes
@app.route('/')
def index():
    intro = show_intro()
    location_desc = show_current_location(current_location)
    inventory_desc = show_inventory()
    return render_template('index.html', intro=intro, location_desc=location_desc, inventory_desc=inventory_desc)
@app.route('/action', methods=['POST'])
def action():
    global current_location
    message = ""
    action = request.form['action'].lower()
    if action == 'quit':
        return redirect(url_for('index'))
    elif action.startswith('go'):
        direction = action.split()[-1]
        current_location, message = move_player(current_location, direction)
    elif action == 'take':
        item = request.form['item'].lower()
        message = take_item(current_location, item)
    elif action == 'inventory':
        message = show_inventory()
    # Redisplay the page with updated information
    location_desc = show_current_location(current_location)
    inventory_desc = show_inventory()
    return render_template('index.html', location_desc=location_desc, inventory_desc=inventory_desc, message=message)
if __name__ == '__main__':
    app.run(debug=True)