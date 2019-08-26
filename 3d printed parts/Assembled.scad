use <RPi.scad>
use <RPi Camera.scad>
use <HC-SR501.scad>

$fn=100;

// Which part should be shown
part = "assembled"; // [assembled,foot,mount]

module foot() {
	for(mir=[0,1])
		mirror([0,mir,0])
		translate([-46,-27,-20]) {
			translate([0,-2,-5])
			cube([2,7,55]);
			translate([2,0,17])
				difference() {
					translate([0,-2,0])
					cube([7,7,7.5]);
					translate([1.5,-1.2,3])
					cube([6,7,1.5]);
					translate([5,2.5,4])
					cylinder(d=2.7,h=4);
					translate([5,2.5,-0.5])
					cylinder(d=2,h=4);
				}
		}
	translate([-46,-27,-25]) {
		cube([2,55,7]);
		translate([0,0,48])
			cube([2,55,7]);
	}
}

module mount() {
	for(mir=[0,1])
		mirror([0,mir,0]) {
			translate([16.5,22,1]) {
				difference() {
					union() {
						translate([0,0,0.5])
						cube([5,7.5,25.5]);
						translate([0,-9.5,26])
							cube([4,4,9.5]);
						translate([0,5.5,-2])
							difference() {
								cube([15,2,4]);
								translate([-1,-0.5,1])
								cube([17,1,1.5]);
							}
					}
					translate([2.5,2.5,-3])
						cylinder(d=2,h=15);
					translate([2,-7.5,27])
						cylinder(d=1.9,h=12);
				}
			}
		}

	translate([16.5,-29,24])
		cube([5,58,3]);
		
	for(mir=[0,1])
		mirror([0,mir,0])
			translate([16.5,-12.5,24]) {
				difference() {
					cube([43.5,4,3]);
					translate([41.5,2,-4])
						cylinder(h=10,d=2);
					translate([29,2,-4])
						cylinder(h=10,d=2);
				}
			}
}

if(part == "assembled") {
	pi3();

	translate([36,0,22])
	rotate([0,0,-90])
		rpicam();
	
	translate([30.5,0,36.5])
	rotate([0,0,90])
		hcsr501();

	foot();
	mount();
} else if(part == "foot") {
	foot();
} else if(part == "mount") {
	mount();
}