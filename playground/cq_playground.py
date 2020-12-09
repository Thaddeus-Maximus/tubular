from cadquery import *

def parsewire(wire):
	print(wire)

stp = importers.importStep("tubes.step")
print(stp.wires())
stp.each(parsewire)
show_object(stp)