This little python script makes a boring image that is ment to be a used as a custom horizon
in SkySafari, based on mesurements you make of your horizon obstructions. You can use this image 
as is, or you can use this for a base layer to align photgraphs or panorama of your horizon.
When using this
custom horizon, you have a truer picture of the sky at your site, and you can more accurately
tell if a particular object is actually visible at your site.

It uses a CSV file that you prepare that describes your horizon. The first number on each line
is the compass reading (azimuth), and the second number (after the comma) is the number of degrees
(from 0 at the Earth's horizon) that describes the vertical obstruction of the horizon at that
azimuth.

For example, if your horizon is 
at 20 degrees everywhere, except for a pesky mountain in the south that blocks the sky up to 45
degrees (and is 40 degrees wide at the base, you would use a CSV file like this:

````
160,20
180,45
200,20
```

There is a -m or --mobile option for the program; if on a device like an iPad or iPhone,
the resulting file should be 2048x1024 pixels. Without the -m option, the program will produce
a 4096x2048 file suitable for a computer. The file is a PNG file.

On my Mac, the file is at ./Library/Containers/com.simulationcurriculum.SkySafari6MacPro/Data/Library/Application Support/SkySafari 6 Pro/. 
Your mileage may vary.

On iOS, the file is in "On My iPhone", then "SkySafari Plus", "SkySafari Pro" etc.

Once the file is in the right place, go to SkySafari settings, the "Horizon & Sky". Select 
"as Panoramic Image" or "as Realistic Image", and your file name should be one of the
choices, without the .png part.
