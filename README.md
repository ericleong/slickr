slickr
======

A collection of python and bash scripts to collect and analyze frame rendering performance in Android apps.

## requirements

* [python](https://www.python.org/)
* [matplotlib](http://matplotlib.org/) - only needed for `plot.py`

## examples

**Make sure to enable the "In adb shell dumpsys gfxinfo" option for "Profile GPU rendering" inside _"Developer options"_ in your settings app!**

Scroll for 8 seconds and save the GPU profiling information for the current screen into a file.

```bash
$ ./slickr.sh > profile.txt
```

Scroll for 8 seconds and display the average frame delay (in milliseconds).

```bash
$ ./slickr.sh | avg.py
```

Scroll for 8 seconds and plot the recorded data and other metrics.

```bash
$ ./slickr.sh | plot.py
```

Compare the frame delay histograms and demand curves of two (or more) saved profiles.

```bash
$ ./compare.py profile1.txt profile2.txt
```

## api

```bash
$ slickr.sh <application package name>
```

Application package name is the Java package name for the Android application. For example, for the [Tumblr app](https://play.google.com/store/apps/details?id=com.tumblr), it is `com.tumblr`. It can be gleaned from the play store url for an application.

If an app has multiple activities open, `profile.py` will choose the activity with `visibility=0` (the currently visibile activity).