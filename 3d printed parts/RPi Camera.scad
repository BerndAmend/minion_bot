$fn=100;

module rpicam()
{
	// PCB (inklusive Bauteile)
	color("limegreen")
	difference() {
		translate([-25/2,0,0])
			cube([25,24,2]);
		
		translate([0,9.5,0])
		for(x = [-21/2,21/2]) {
			for(y = [0,12.5]) {
				translate([x,y,-1]) {
					cylinder(h=4,d=2);
				}
			}
		}
	}

	// Connector
	color("SaddleBrown")
	translate([-21/2,0,-1.5])
		cube([21,5,2.5]);

	// Camera connector
	color("SaddleBrown")
	translate([-8/2,13.5,2])
		cube([8,9,1.5]);
	// Camera
	color("black")
		translate([-8/2,5.5,2])
			cube([8,8,5]);
}

rpicam();