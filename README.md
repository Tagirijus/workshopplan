# Workshop Plan

This is an approach for some kind of plain text syntax for planning workshops, seminars, tutorials, training lessons, etc. I tried to put this all into a Sublime Text 3 plugin with syntax highlighting, analyzing output as a sublime popup message and also the ability to export the overall plan into another format like HTML or PDF. The syntax basically is just YAML.

The syntax highlighting can look like this:

![screenshot](documentation/screenshot.png)

## Installation

I tested this plugin in Sublime Text 3 (build 3176).

To install the plugin, clone the repo to a new folder like this: `[SUBLIME_FOLDER]/Packages/WorkshopPlan`. An install with the `Package Control` is not possible yet, since I am not sure how to do this. Help is appreciated here!

Now when pressing `Alt+E` the plugin starts and when pressing `Ctrl+R` you get the navigator with some information about the workshop blocks.

## Settings

There is a `general/settings.yaml.dist` which should be copied to `general/settings.yaml` and tweaked. Hopefully the keys are self explaining. Feel free to contact me, if somethign is not clear.

## Usage

The syntax is just YAML, which should look something like this:

```YAML
---
Title: Title of the block
Length: 15
Type: none
```

There are these basic keys, which are needed for the analyzing and exporting stuff later:

- `Title`: the title of the workshop block
- `Length`: an integer for the length of the block in MINUTES, or in the format `H:MM` (seems to be a feature of the YAML parser, cool! :D). The timeformat only works without a leading `0`, though. Instead of `Length: 0:30` it should be `Length: 30` only in the meta data, for example.
- `Type`: one of these types, describing (and later coloring) the block: `none`, `discussion`, `theory`, `exercise` and `break`.
- `Materiel`: a list holding the needed materials for this block.
- `Description`: the text description of the block
- `Goal`: the goal for the block
- `Instructions`: the instructions the teacher should do
- `Notes`: Notes for the teacher

There are also these possible meta data:

```
---
Workshop: Title of the whole workshop
Author: Author of the workshop
Time: 10:00
```

The `Time` also behaves like `LEngth` and should mark the day time start for the workshop.

There are auto-completions for adding a new `block` or a `break` (just type "block" or "break" and tab).

An example `.wplan` file is [here](documentation/example.wplan).

## Other projects

For rendering a `.wplan` file to a nice PDF, see my project [workshopplan_render](https://github.com/Tagirijus/workshopplan_render) here on github. I would like to embed this feature into the Sublime Text 3 plugin, but I could not make it work in a sublime text plugin. So now there is an independent python script for PDF rendering ...

