CMPUT404-assignment-ajax
==============================

The code for the solution of this assignment is based almost entirely on the AJAX sample code from the slides located here: https://github.com/uofa-cmput404/cmput404-slides/tree/master/examples/ObserverExampleAJAX, written by Abram Hindle and Hazel Campbell

The code used for drawing the star pattern was adapted from this: https://stackoverflow.com/questions/25837158/how-to-draw-a-star-by-using-canvas-html5
with attribution given to stackoverflow users Andrei Volgin and markE

This implementation doesn't send the world each time, but it does re-render the entire browser-world whenever it gets a new update, I'm not sure if this causes too much latency (especially in firefox).  I originally had it set so that the browser would just draw the new items whenever it would get an update, but it was harder to keep the browsers and server properly synced up.

Contributors / Licensing
========================

Generally everything is LICENSE'D under the Apache 2 license by Abram Hindle, Justin Liew.


