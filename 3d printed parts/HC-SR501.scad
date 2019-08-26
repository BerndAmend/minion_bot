$fn=100;

module hcsr501()
{
	// PCB (inklusive Bauteile)
	color("limegreen")
	difference() {
		translate([-32/2,0,0])
			cube([32,24,3]);
		
		translate([0,12,0])
		for(x = [-29/2,29/2]) {
			translate([x,0,-1]) {
				cylinder(h=5,d=2);
			}
		}
	}

	// Dings
	color("black")
	translate([32/2-2.5,0,-9])
		cube([2.5,7.5,9]);

	color("black")
	translate([-32/2,0,-9])
		cube([27,5,9]);
	
	// Connector
	color("black")
	translate([-10/2,24-2.5,-17])
		cube([10,2.5,17]);
	
	// Kondensatoren
	color("black")
	for(x = [-28/2,28/2])
	translate([x,24-2,-8])
		cylinder(d=4,h=8);

	// Detektor
	color("white") {
		translate([-23/2,0.5,2])
				cube([23,23,3.5]);
		translate([0,0.5+23/2,2+3.5]) {
				difference() {
					sphere(d=23);
					translate([0,0,-8])
						cube([23,23,10],true);
				}
			}
	}
}

hcsr501();