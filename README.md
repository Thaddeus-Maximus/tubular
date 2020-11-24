# Tubular
Tubeframe FE analyisis that doesn't suck. By "doesn't suck", what I mean is:
- Maintainable; allows you to re-import new geometry without re-selecting all entities
- Documented; allows you to make a "recipe" for how a frame is analyzed (or follow one of our examples)
- Exportable; allows you to do your own post-processing on a number of runs
- Delightful; gives you additional tools that you wouldn't easily have in other FE softwares
- Open; you've got full access to the innards if you really want to go there.

# Dependencies
Python 3.7 with these packages:
[https://github.com/JWock82/PyNite](PyNite), which depends on
- numpy
- scipy
- matplotlib
- PrettyTable
- VTK (this one is annoying, but you'll want it for visualization)
[https://github.com/tpaviot/pythonocc-core](PythonOCC-Core) 7.4.1

Conda may make installing these dependencies easier.
PyNite is not available from pip. The package pynite (lowercase) is for Fortnite... which isn't helpful.