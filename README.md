# Zewail City Campus Pathfinding AI

A Python artificial-intelligence course project that models the Zewail City campus as a weighted search problem and finds routes between campus locations using classic AI search algorithms.

The project combines a color-coded campus map, a room/building lookup spreadsheet, a PyQt5 desktop interface, and several search algorithms including A* search, breadth-first search, greedy best-first search, hill climbing, and simulated annealing.

## Preview

### Campus Map

![Color-coded Zewail City campus map](public/images/projects/zewail-campus-pathfinding-ai/campus-map.png)

### A* Route Example

![A* route generated from the project code](public/images/projects/zewail-campus-pathfinding-ai/astar-route.png)

### Algorithm Route Comparison

The image below was generated from the project code using the same start and goal positions across several algorithms.

![Algorithm route comparison generated from project code](public/images/projects/zewail-campus-pathfinding-ai/route-comparison.png)

## GUI Preview

The screenshots below are deterministic interface renderings reconstructed from the widget geometry, labels, styles, and assets defined in `AI_Project1.py`. They are not AI-generated images. The visualization area is shown as a scrollable image viewport, matching the intended design of the original GUI.

<table>
  <tr>
    <td align="center" width="50%">
      <img src="public/images/projects/zewail-campus-pathfinding-ai/gui-main-window-initial.png" alt="Initial PyQt5 main window layout" />
      <br />
      <strong>Main Window Layout</strong>
    </td>
    <td align="center" width="50%">
      <img src="public/images/projects/zewail-campus-pathfinding-ai/gui-room-route-with-visualization.png" alt="Room workflow with route visualization and output panel" />
      <br />
      <strong>Route Output Workflow</strong>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <img src="public/images/projects/zewail-campus-pathfinding-ai/gui-coordinate-entry-mode.png" alt="Coordinate entry workflow enabled" />
      <br />
      <strong>Coordinate Entry Mode</strong>
    </td>
    <td align="center" width="50%">
      <img src="public/images/projects/zewail-campus-pathfinding-ai/gui-start-position-dialog.png" alt="Start position input dialog" />
      <br />
      <strong>Start Position Dialog</strong>
    </td>
  </tr>
</table>

## Project Overview

The application treats the campus image as a searchable grid. Each pixel color represents a semantic region such as a road, building, blocked area, or landmark. The route planner evaluates movement across this grid using weighted traversal costs and a goal-directed heuristic.

The desktop GUI supports two destination-entry workflows:

- **Coordinate-based routing** by entering a target `(x, y)` location.
- **Room/building-based routing** using the `Rooms.xlsx` lookup sheet.

The project also includes non-GUI scripts that reproduce route outputs directly from the algorithm code, making the visual results easier to review without launching the full interface.

## Features

- Color-coded campus map used as the search space.
- Weighted movement costs based on map region color.
- Eight-direction movement over the map grid.
- Coordinate-based and room/building-based destination selection.
- PyQt5 desktop interface with input, output, visualization, and route-description panels.
- Multiple search algorithms implemented in Python.
- Reproducible route-image generation from the project code.

## Search Algorithms

The project includes implementations of:

- Breadth-first tree search
- Breadth-first graph search
- Depth-first search
- Iterative deepening search
- Greedy best-first search
- A* search
- Hill climbing
- Simulated annealing

## Repository Structure

| File | Purpose |
|---|---|
| `AI_Project1.py` | Main PyQt5 GUI application. |
| `functions.py` | Search-problem classes, search nodes, and search algorithms. |
| `project.py` | Campus-map problem formulation and route-program wrapper. |
| `helper.py` | Static reference dictionaries used during development. |
| `Rooms.xlsx` | Building and room coordinate lookup table used by the GUI workflow. |
| `image.png` | Original color-coded campus map used by the code. |
| `generate_sample_route.py` | Generates a standalone A* route example. |
| `generate_readme_images.py` | Regenerates the README images from the actual project code. |
| `sample_astar_route.png` | A generated A* route output kept for quick review. |
| `public/images/projects/zewail-campus-pathfinding-ai/` | README image assets generated from the project, including route outputs and GUI screenshots. |
| `AI_Project1.sln` / `AI_Project1.pyproj` | Visual Studio project files from the original development environment. |

## How the Search Space Works

The map-processing workflow starts from `image.png`, resizes it, and normalizes colors that represent campus regions. The search problem then defines:

- an initial state;
- a goal state;
- valid movement actions;
- a result function;
- a goal test;
- a step-cost function;
- and a heuristic function.

Movement is possible in eight directions. Each movement step is assigned a cost according to the terrain or region color crossed by the route. The A* search implementation uses the accumulated path cost plus a Euclidean-distance heuristic.

## How to Run / Review

### 1. Install dependencies

```bash
pip install PyQt5 xlwings opencv-python numpy matplotlib Pillow
```

Dependency notes:

- `PyQt5` is used for the desktop GUI.
- `xlwings` is used for reading `Rooms.xlsx` in the GUI workflow.
- `opencv-python` is used for map/image processing.
- `numpy` is used for array operations.
- `matplotlib` is used for plotting and visual-output support.
- `Pillow` is used to generate the README comparison image.

### 2. Generate the sample A* route

```bash
python generate_sample_route.py
```

This creates:

```text
sample_astar_route.png
```

### 3. Regenerate the README images

```bash
python generate_readme_images.py
```

This creates the images under:

```text
public/images/projects/zewail-campus-pathfinding-ai/
```

### 4. Run the GUI application

```bash
python AI_Project1.py
```

The GUI was originally developed around a Windows / Visual Studio workflow and uses `xlwings` to read `Rooms.xlsx`. For the full GUI workflow, it is best reviewed on Windows with Excel available.

## Cleaned-Version Note

This public version was organized from several archived versions of the same course project. The final package keeps the strongest integrated version and removes redundant or incomplete artifacts.

Older versions contained QR-code images, but they were removed because the QR feature was not connected to the selected AI-generated campus route. One QR file was only a placeholder, and another pointed to a fixed Google Maps route rather than to the project’s computed path.

## Summary

This project demonstrates how a real map-like image can be transformed into an AI search problem. It connects classical search algorithms with a practical campus-routing interface, showing how different strategies can traverse the same weighted search space.
