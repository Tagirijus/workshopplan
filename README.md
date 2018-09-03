# Workshop Plan

This is an approach for some kind of plain text syntax for planning workshops, seminars, tutorials, training lessons, etc. I tried to put this all into a Sublime Text 3 plugin with syntax highlighting, analyzing output as a sublime popup message and also the ability to export the overall plan into another format like HTML or PDF. The syntax basically is just YAML.

The syntax highlighting can look like this:

![screenshot](documentation/screenshot.png)

## Installation

I tested this plugin in Sublime Text 3 (build 3176).

To install the plugin, clone the repo to a new folder like this: `[SUBLIME_FOLDER]/Packages/WorkshopPlan`. An install with the `Package Control` is not possible yet, since I am not sure how to do this. Help is appreciated here!

After cloning you should set up a key binding like this:

```JSON
	{ "keys": ["alt+e"], "command": "workshopplan" },
```

And now when pressing `Alt+E` the plugin starts.

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
- `Length`: an integer for the length of the block in MINUTES
- `Type`: one of these types, describing (and later coloring) the block: `none`, `discussion`, `theory`, `exercise` and `break`.
- `Materiel`: a list holding the needed materials for this block.

I also thought about blocks to have these keys, while they are not needed for analyzing or changing the export:

- `Description`: the text description of the block
- `Goal`: the goal for the block
- `Instructions`: teh instructions the teacher should do

There are auto-completions for adding a new `block` or a `break` (just type "block" or "break" and tab).

An example `.wplan` file is [here](documentation/example.wplan).

## To do

- Export into HTML and / or PDF
