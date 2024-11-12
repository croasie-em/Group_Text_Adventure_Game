from flask import Flask, render_template, request, session, redirect, url_for, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a string or bytes for the secret key


# Initialise game variables
locations = {
    'endless grove': {
        'name': 'The Endless Grove',
        'description': 'The forest here stretches on with towering trees, their twisted branches interlocking above, blocking most of the light...',
        'directions': {'north': 'old oak', 'east': 'stone circle'},
        'items': ['Backpack']
    },
    'old oak': {
        'name': 'The Old Oak',
        'description': 'A massive oak tree dominates this part of the forest...',
        'directions': {'south': 'endless grove', 'east': 'misty pond'},
    },
    'stone circle': {
        'name': 'The Stone Circle',
        'description': 'A ring of ancient stones, weathered by time...',
        'directions': {'west': 'endless grove', 'north': 'misty pond'},
        'items': ['candlestick']
    },
    'misty pond': {
        'name': 'The Misty Pond',
        'description': 'A small pond appears through the trees, its surface obscured by a layer of mist...',
        'directions': {'west': 'old oak', 'south': 'stone circle', 'east': 'fallen log'},
    },
    'fallen log': {
        'name': 'The Fallen Log',
        'description': 'A giant log lies across the forest floor...',
        'directions': {'west': 'misty pond', 'north': 'forest edge'},
    },
    'forest edge': {
        'name': 'The Forest Edge',
        'description': 'At last, the trees begin to thin...',
        'directions': {}
    }
}


@app.route('/', methods=['GET', 'POST'])
def index():
    # Initialize the game
    if 'location' not in session:
        session['location'] = 'endless grove' # set the initial location
        session['inventory'] = [] # we initialise an empty inventory
        session['message'] = []  # Make sure message is a list
        show_intro() # to display the intro text
        
    if request.method == 'POST':
        # Handle action submitted through form
        action = request.form.get('action')
        if action == 'go':
            direction = request.form.get('direction')
            if direction:
                return process_action(f'go {direction}')
        return process_action(action) #process other actions
    else: #request method == 'GET'
        show_current_location('endless grove')

# render the template with game data
    message = session.pop('message', []) #to get and clear the message
    return render_template('index.html', location=locations[session['location']], inventory=session['inventory'], message=message)

# Game functions
def show_intro():
    message = """\nYou wake up on cold, damp ground, the earthy scent of moss and wet leaves thick around you. Rising slowly, you find yourself surrounded by towering trees, their dense canopy blocking out most of the light and casting deep shadows across the forest floor.
    The forest extends endlessly in every direction, with no clear path or landmark to guide you. Panic settles in as you search your memory for any clue of how you got here—nothing.
    Your pockets are empty, and an eerie silence fills the air, broken only by the faint, haunting sound of a melody drifting from somewhere deeper among the trees.
    The atmosphere feels alive, as though the forest itself is watching, waiting for you to make your move."""
    return jsonify({'message': message})


def show_current_location(location):
    # display the description of the current location
    location_data = locations[location].copy()
    location_data['current location'] = location
    return jsonify(location_data)

# Move the player
def move_player(location, direction):
    new_location = locations[location]['directions'].get(direction)
    if new_location:
        session['location'] = new_location
        show_current_location(new_location)
        return ''
    else:
        return 'You cannot go that way.'

def process_action(action):
    current_location = session['location']
    if action == 'quit':
        return redirect(url_for('index'))
    elif action.startswith('go'):
        direction = action.split()[-1]
        message = move_player(current_location, direction)
    elif action == 'take':
        item = request.form['item'].lower()
        message = take_item(current_location, item)
    elif action == 'inventory':
        message = show_inventory()
    
    session['message'].append(message)
    return redirect(url_for('index'))

# Adds an item to the player's inventory
def take_item(location, item):
    if 'items' in locations[location] and item in locations[location]['items']:
        session['inventory'].append(item)
        locations[location]['items'].remove(item)
        return f'You take the {item}.'
    else:
        return 'There is no such item here.'

# Shows the player's inventory
def show_inventory():
    inventory = session.get('inventory', [])
    if inventory:
        items = "<p>Your inventory:</p><ul>" + "".join(f"<li>{item}</li>" for item in inventory) + "</ul>"
        return items
    else:
        return '<p>Your inventory is empty.</p>'

if __name__ == '__main__':
    app.run(debug=True)
