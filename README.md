ECE-499-590-Fall-2014
=====================

ECE-499-590-Fall-2014

***Approach***
	I wanted to make use of the hsv color-space so that I could track specifically the color, regardless of the lighting and saturation (within a threshold) and not worry about the relationship between the RGB components to still be considered green, so I did a colorspace conversion.  From there, I created a binary mask denoting the color green.  Getting the moments from the mask, I found the centroid of the green object giving me the location of the object, and used that point to draw a red circle on the screen at the centroid of the object.

***Running the project***
To run, enter the d_diff_drive_robot directory and start the robot-view: 
	./robot-view server

Start the object tracking process:
	python cv_tracker.py

Start the process to turn the robot counter-clockwise:
	python robot-view-serial.py



