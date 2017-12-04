# Autodrill
Camera assisted drilling of PCBs using LinuxCNC.

## Background and Basic Idea
Making a prototype PCB can be an ambitious task. Typically the process involves the following steps:

1. Design in EDA system
2. Exposure and development (or toner transfer)
3. Etching
4. Drilling
5. Population and soldering

Drilling can be done manually on a drill press (which is tedious and error-prone) or with a CNC drilling machine. The problem of the later is, that the etched PCB has to be carefully aligned to the machine axes. Due to scaling and distortion (e.g. from the printer) a proper alignment can be very challenging. Even a small miss-alignment can ruin the whole PCB.

Autodrill is addressing this alignment problem with a camera and a coordinate transformation. Simply place the PCB on the machine, align 3 or 4 holes and start drilling.

## Software Requirements
* [LinuxCNC](http://linuxcnc.org/) (tested with v2.8)
* Python 2.7
* PyQt4
* OpenCV
* ... TODO

## Build and Run
To build the UI files do:

	$ ./build_ui.sh

To run Autodrill:

	$ autodrill/autodrill.py
	

## Machine Setup
In order to use Autodrill you need a CNC mill (or router) controlled by LinuxCNC and a camera mounted next to the spindle. Choose a camera that is able to focus at small distance. Ideally the camera should be in focus when a drill bit that is mounted in the spindle is still some millimeters above the PCB and all obstacles. This way you should be save to pan over the PCB without crashing the drill bit. 

Although the camera axis should be parallel to the spindle, the alignment is not super critical as long as the vertical distance from the camera to the PCB is always the same. To calibrate the camera-to-spindle offset simply drill a test hole, find it with the camera and save the coordinates.

Also bear in mind that a camera needs light. Some LEDs around the camera will do the job.


## Drills and Tooltable
Autodrill automatically rounds all diameters to the given drill list in *Settings* -> *Drills*. Make sure that you enter the right tool number, matching the LinuxCNC tool table. I recommend to use the drill diameter in µm as tool number e.g. d=0.8mm -> T800

Also make sure that all your drill bits have a depth setting ring that is set to 20.32mm (0.8 inch). See also: [https://mctinfo.net/pdfs/MCT-%20Standard%20Tool%20Ring%20Dimensions.PDF](https://mctinfo.net/pdfs/MCT-%20Standard%20Tool%20Ring%20Dimensions.PDF)

When you insert a drill bit, push it all the way up so that the depth setting ring touches the chuck. This way the tip of the drill should always be at the same height and you only need to touch off once.

## Suggested Workflow
1. Start LinuxCNC and home all axes as usual.
2. Start Autodrill and load the drillfile.
3. Fix the etched PCB on the machine table (e.g. with double sided tape)
4. Go back to Autodrill and use the cursor keys to move the camera's cross hairs exactly over an arbitrary hole (preferably in one corner).
5. Select the corresponding hole in Autodrill, then press *Add Selected Point*.
6. Repeat the steps 4 and 5 three or four times with different holes.
7. Select *File* -> *Write G-Code file*
8. Switch to LinuxCNC and run the generated file. Change the drills as prompted.

## Coordinate Transformation

TODO




