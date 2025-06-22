# TBHX Preview Subs

A collection of scripts I use in my translation and typesetting workflow for To Be Hero X previews

## Installation

For running on Windows, the applications may need to have the paths to their executables added to the system's PATH variable

Python is required to run the scripts, and the required packages can be installed using your system's package manager

```bash
# Arch Linux
$: sudo pacman -S python
```

Video downloading uses [yt-dlp](https://github.com/yt-dlp/yt-dlp)

```bash
# Arch Linux
$: sudo pacman -S yt-dlp
```

Subtitle timings are generated using [videosubfinder](https://sourceforge.net/projects/videosubfinder/)

```bash
# Arch Linux, using an AUR helper like yay or paru
$: yay -S videosubfinder
```

OCRed subtitle files are generated using [RapidVideOCR](https://github.com/SWHL/RapidVideOCR)

```bash
# Requires Python to be installed
$: pip install rapid_videocr
```

Subtitles are embedded using [ffmpeg](https://ffmpeg.org/)

```bash
# Arch Linux
$: sudo pacman -S ffmpeg
```

## Usage

For each script, they optionally take in arguments for an entry to run on

Entries are defined in `urls.json` as a string key

```json
{
  "example_entry": "https://www.url-to-some-video-here.com"
}
```

```bash
# Downloading the example_entry
$: ./download.py example_entry
```

If no arguments are given, the script will batch run on every entry in the `urls.json`

Files and output are placed in a directory with the respective entry name

### Scripts

#### `run.py`

Runs the main pipeline for an entry; first downloads the video file, generates the subtitle timings using the video file, creates the OCRed subtitle file, and finally applies the custom style

Requires `dimensions.json` to be set, since the [`ocr.py`](#ocrpy) script uses its values

#### `download.py`

Uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) to download a video file to the entry directory, generated video files are given the entry name as the filename and with the `.mp4` file format

#### `generate_timings.py`

Uses [videosubfinder](https://sourceforge.net/projects/videosubfinder/) to generate subtitle timings to the entry directory, which are saved to the `RGBImages` directory as `.jpeg` files whose timings are encoded in the filename

#### `ocr.py`

Uses [RapidVideOCR](https://github.com/SWHL/RapidVideOCR) to create an OCRed subtitle file to the entry directory using the `RGBImages` directory in the entry directory, and saves the subtitle file with the entry name as the filename and with the Advanced Substation Alpha `.ass` file format

Requires `dimensions.json` to set the subtitle crop boundary edges for the OCR search area

```json
{
  "te": 0.20,
  "be": 0.14,
  "le": 0.25,
  "re": 0.75
}
```

`te` is the top edge, `be` is the bottom edge, `le` is the left edge, and `re` is the bottom edge; the values are defined as a float where `1.0` is the top-most edge of the image and `0.0` is the bottom-most edge of the image for the y-axis, and `1.0` is the right-most edge of the image and `0.0` is the left-most edge of the image for the x-axis

#### `apply_style.py`

Adds and applies custom style defined in `style.ass` to all dialogue lines in the existing subtitle file with the entry name in the entry directory

#### `hardsub.py`

Uses [ffmpeg](https://ffmpeg.org/) to encode a video file with the subtitles embedded (hardsubbed) in, and saves the hardsubbed video file in the entry directory with the filename `[entry_name]_subbed.mp4`
