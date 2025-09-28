python
from pymol import cmd
nframes = 120
for i in range(1, nframes+1):
    cmd.frame(i)
    cmd.ray(800, 800)
    cmd.png(f"rotation/frame{i:04d}.png")
python end
