<h1 style="font-size: 30px; text-align: center; margin: 15px; padding: 10px;">CircuitChivalry</h1> 

# Start  ![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)

1. Create virtualenv
```
python -m venv [path to venv folder]
```

2. Activate virtualenv
``` 
.\venv\Scripts\activate (for Windows)
source env/bin/activate (for Linux)
```

3. Install pygame
``` 
pip install pygame
```

4. Run the game
```
python main.py
```

CircuitChivalry/
│
├── venv/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── game_manager.py
│   │   ├── scene_manager.py
│   │   ├── settings.py
│   │   └── constants.py
│   │
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── enemy.py
│   │   ├── platform.py
│   │   ├── generator.py
│   │   └── crystal.py
│   │
│   ├── levels/
│   │   ├── __init__.py
│   │   ├── base_level.py
│   │   ├── sector1_gateway.py
│   │   ├── sector2_data_tunnel.py
│   │   ├── sector3_arena.py
│   │   ├── sector4_core.py
│   │   └── transition_level.py
│   │
│   ├── effects/
│   │   ├── __init__.py
│   │   └── music_manager.py
│   │
│   └── ui/
│       ├── __init__.py
│       ├── menu.py
│       └── cutscene.py    
│
├── assets/
│   ├── images/
│   ├── music/
│   └── fonts/
