slickr
======

A collection of python and bash scripts to collect and analyze frame rendering performance in Android apps.

## requirements

* [python](https://www.python.org/)
* [matplotlib](http://matplotlib.org/) - only needed for `plot.py`

## setup

### on device

**Make sure to enable the "In adb shell dumpsys gfxinfo" option for "Profile GPU rendering" inside _"Developer options"_ in your settings app!**

_You may need to kill and restart your app for the logging to work!_

### on computer

If you can't execute the scripts, you may need to mark them as executable.

```bash
$ chmod +x *.sh *.py
```

should do the trick on Unix-like operating systems.

## examples

Scroll for 8 seconds and save the GPU profiling information for the current screen into a file.

```bash
$ ./slickr.sh > profile.txt
```

Scroll for 8 seconds and display the average frame delay (in milliseconds).

```bash
$ ./slickr.sh | ./avg.py
```

Scroll for 8 seconds and plot the recorded data and other metrics.

```bash
$ ./slickr.sh | ./plot.py
```

Compare the frame delay histograms and demand curves of two (or more) saved profiles.

```bash
$ ./compare.py profile1.txt profile2.txt
```

## api

```bash
$ slickr.sh <package> <iterations> <distance>
```

* `package` is the Java package name for the Android application. For example, for the [Tumblr app](https://play.google.com/store/apps/details?id=com.tumblr), it is `com.tumblr`. It can be gleaned from the play store url for an application.

    If an app has multiple activities open, `profile.py` will choose the activity with `visibility=0` (the currently visibile activity). On devices below [Lollipop](https://developer.android.com/about/versions/lollipop.html), all profile data is exported.

* `iterations` is the number of 2 second iterations to run (since 128 frames, the default buffer size, is a duration of about 2 seconds at 60 frames per second). Default is `4`.

* `distance` is the scroll distance in pixels. It defaults to 3x the display density (at the bucket the device belongs to).
