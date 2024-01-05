# Space Invaders
![Screenshot 2024-01-03 at 3 00 31 AM](https://github.com/andrewpols/space-invaders-pygame/assets/139817202/2c6334f8-713b-4cf9-818d-6cc1de4ef1f1)

## Background
- This program recreates the iconic Space Invaders game using Python and [Pygame](https://github.com/pygame/pygame).
- Through [Pygbag](https://github.com/pygame-web/pygbag), a Python WebAssembly package, this code is available on non-local servers (it is ran through the index.html and apk file shown in the root directory).
- The source code can be found in the src folder in the root directory (Note: The index.html file in the root directory is NOT part of the original souce code—it is built through Pygbag). The main loop of the main.py file is AsyncIO-aware for Pygbag to build it into an accesible file. 
- **Play now via [GitHub Pages](https://andrewpols.github.io/space-invaders-pygame/)**

## Aim of the Game
- Starting with 3 lives, survive and kill all aliens!
- Each alien awards 100 points, while every hit taken from an alien loses a life.
- A bonus alien will periodically fly at the top of the screen. Hit it for extra points and an extra life.
- Once you're done, play again.

## Controls
- Move Left/Right: L/R Arrow Keys
- Shoot: Spacebar

## Troubleshooting
- For some unknown reason, the game might slow down when your computer's battery is low (not to an unplayable amount).
- If this does happen, plugging in the computer to a charger will fix the problem.
