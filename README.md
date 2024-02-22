# ccompress
just provide the manga/comic(ending in .cbz/.cbr/.zip) as a parameter and the script will do the rest.
the script has some additional flags to tailor the compression to one's heart's content.


- ```-q``` for quality(between 1 and 100)
- ```-f``` for the (filter)[https://imagemagick.org/Usage/filter/] to use with imagemagick
- ```-o``` specify the output directory, defualts to ```~/Documents/manga/compressed```
- ```-r``` specify the value for the (-resize)[https://legacy.imagemagick.org/Usage/resize/] flag of imagemagick, defaults to 60%
# dependencies
- imagemagick
