# Baseball Simulation Game

A comprehensive baseball franchise management simulation game built with Python Flask backend and React frontend.

## Features

- **Franchise Management**: Create and manage your own baseball franchise
- **Team Selection**: Choose from multiple teams with different budgets and goals
- **Player Management**: View detailed player statistics and team rosters
- **Game Simulation**: Simulate realistic baseball games with detailed statistics
- **Season Management**: Track standings, schedule, and season progress
- **Save System**: Multiple save slots to manage different franchises

## Technology Stack

- **Backend**: Python Flask with SQLite database
- **Frontend**: React.js with modern UI components
- **Database**: SQLite for game data persistence
- **API**: RESTful API for frontend-backend communication

## Project Structure

```
BaseballSim_Project/
├── backend/                 # Python Flask API server
│   ├── api_server.py       # Main Flask application
│   ├── game_manager.py     # Game state management
│   ├── player_generator.py # Player creation and stats
│   ├── sim_engine.py       # Game simulation logic
│   ├── world_generator.py  # World/league generation
│   └── saves/              # SQLite save files
├── frontend/               # React.js frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   └── App.js         # Main application
│   └── package.json       # Node.js dependencies
└── start_both.bat         # Windows batch file to start both services
```

## Installation & Setup

### Prerequisites

- Python 3.8+ with pip
- Node.js 14+ with npm
- Git

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

4. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the API server:
   ```bash
   python api_server.py
   ```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install Node.js dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

### Quick Start (Windows)

Use the provided batch files for easy startup:

- `start_both.bat` - Starts both backend and frontend
- `start_server.bat` - Starts only the backend
- `start_frontend.bat` - Starts only the frontend
- `stop_all.bat` - Stops all running processes

## Game Features

### Franchise Hub
- View team overview with overall ratings
- Check current standings
- See upcoming games
- Monitor team budget and goals

### Team Management
- Select from multiple teams with different characteristics
- View detailed team rosters
- Analyze player statistics and potential
- Track team payroll and financial status

### Game Simulation
- Realistic baseball game simulation
- Detailed player statistics tracking
- Season progression with standings updates
- Multiple save slots for different franchises

## API Endpoints

- `GET /api/saves` - List all save games
- `POST /api/new_game` - Create a new franchise
- `DELETE /api/saves/<save_name>` - Delete a save game
- `GET /api/franchise/<save_name>/teams` - Get all teams
- `GET /api/franchise/<save_name>/teams/<team_id>` - Get team details
- `POST /api/franchise/<save_name>/select_team` - Select a team
- `GET /api/franchise/<save_name>` - Get franchise data
- `POST /api/franchise/<save_name>/simulate` - Simulate next game

## Development

### Adding New Features

1. Backend changes go in the `backend/` directory
2. Frontend changes go in the `frontend/src/` directory
3. API endpoints are defined in `backend/api_server.py`
4. React components are in `frontend/src/components/`

### Database Schema

The game uses SQLite with the following main tables:
- `teams` - Team information and statistics
- `players` - Player data and ratings
- `schedule` - Game schedule and results
- `standings` - Team win/loss records
- `game_metadata` - Game state and settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Future Enhancements

- Player development and aging
- Trading system
- Draft system
- Advanced statistics
- Multiplayer support
- Historical seasons
- Custom league creation
