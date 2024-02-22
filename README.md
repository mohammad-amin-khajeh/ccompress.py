# ccompress
a tool for compressing manga and comics on the fly.

just provide the manga/comic(ending in .cbz/.cbr/.zip) as a parameter and the script will do the rest.
the script has some additional flags to tailor the compression to one's heart's content.


- ```-q``` specify the quality, defaults to 50.
- ```-f``` specify the [filter](https://imagemagick.org/Usage/filter/) to use with imagemagick.
- ```-o``` specify the output directory, defualts to ```~/Documents/manga/compressed```
- ```-r``` specify the value for the [-resize](https://legacy.imagemagick.org/Usage/resize/) flag of imagemagick, defaults to 60%.
- ```-e``` specify the format to convert to through the extension defaults to webp.
# dependencies
- imagemagick
- pynotify2(optional, for notifications when conversion is completed)
