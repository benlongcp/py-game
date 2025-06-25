# Multi-Player Topographical Plane Game

## 🎮 Features

### **Dual-Window Multi-Player System**
- **Player 1 (Red Dot)**: Controls with Arrow Keys + Spacebar
- **Player 2 (Purple Dot)**: Controls with WASD + Left Ctrl
- Each player has their own window that follows their character
- Both players interact in the same shared world

### **Enhanced Physics**
- **Player vs Player Collisions**: Red and purple dots bounce off each other realistically
- **Projectile Interactions**: Projectiles affect all objects (blue square, both players)
- **Newtonian Mechanics**: All collisions follow conservation of momentum
- **Rotational Physics**: Blue square spins when hit off-center

### **Visual Effects**
- **Pulse Effects**: Blue square pulses light blue when hit
- **Momentum Indicators**: Triangular indicators show movement direction and speed
- **Independent Cameras**: Each window follows its own player

## 🎯 How to Play

### **Launch the Game**
```bash
python main.py
```

### **Controls**
**Player 1 (Red Dot Window):**
- Move: Arrow Keys (↑↓←→)
- Shoot: Spacebar

**Player 2 (Purple Dot Window):**
- Move: WASD Keys
- Shoot: Left Ctrl

### **Gameplay Objectives**
- Hit the blue square to make it move and spin
- Collide with the other player for physics interactions
- Shoot projectiles to affect all objects
- Try to coordinate or compete with the other player!

## 🏗️ Architecture

### **Modular Design**
- `GameEngine`: Centralized game state and physics
- `TopographicalPlane`: Rendering and input for each window
- `Objects`: RedDot, PurpleDot, BlueSquare, Projectile classes
- `Physics`: Collision detection and response
- `Rendering`: Visual effects and drawing

### **Multi-Window System**
- Shared `GameEngine` instance manages all objects
- Each window references the same game state
- Independent cameras follow different players
- Synchronized physics updates across both views

## 🔧 Technical Implementation

### **Phase 1: Game Engine Extraction**
- Separated game logic from rendering
- Created centralized state management
- Enabled shared object references

### **Phase 2: Dual Player Support**
- Added PurpleDot class (inherits from RedDot)
- Implemented WASD + Ctrl input system
- Added player-vs-player collision physics

### **Phase 3: Multi-Window Setup**
- Created dual TopographicalPlane instances
- Implemented independent camera systems
- Added window positioning and management

## 🎨 Visual Features

- **Triangular Grid**: Dynamic grid that scrolls with camera
- **Vignette Effect**: Subtle edge darkening for depth
- **Color-Coded Players**: Red and purple for easy identification
- **Pulse Effects**: Visual feedback on collisions
- **Momentum Indicators**: Show speed and direction

## 🚀 Performance

- **60 FPS**: Smooth gameplay at 16ms frame intervals
- **Efficient Rendering**: Only draws visible objects
- **Optimized Physics**: Minimal computational overhead
- **Memory Management**: Proper object lifecycle handling

Enjoy the enhanced multi-player physics sandbox experience! 🎉
