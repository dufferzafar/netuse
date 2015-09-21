
*This stuff is old, clunky & un-maintained.*

# Internet Usage

Parse [Networx](http://www.softperfect.com/products/networx) backup XMLs to visualise data.

## Table of Contents

* [The Story](#story)
* [The Plan](#plan)
* [Stuff to do](#todo)
* [Changelog](#changelog)

## <a name="story"></a>The Story

I've been creating a backup of network usage data every month for the past one year. Stuff like "Bytes Downloaded", "Bytes Uploaded", "Session Dialup Durations".

[Networx](http://www.softperfect.com/products/networx) saves these backups in XML format.

I now wish to visualise all this data - through charts, bars - whatever.

## <a name="plan"></a>The Plan

The plan is to begin with some python scripts which will scrape the XML to cleanup the data and will spit out js files containing the entire dataset as arrays.

The output js files will look something like:

```javascript
// Downloaded data in MBs for 12 months. Each array will 30/31 values.

var downloads['January']  = [381, 121, 10, 85, 71, 113, 117];
var downloads['February'] = [136, 7, 310, 241, 65, 0, 0];
var downloads['March']    = [56, 107, 53, 0, 0, 19, 44];

// Similar structure for uploads[] and time[]
```

I will then include these datasets in an another js file which will plot them using [D3](www.d3js.org)

The plotting part will be a simple web application (sort-of) built using Bootstrap (for UI), jQuery UI (for datepicker, controls etc.), 

## <a name="todo"></a>Todo

* Facy Plot
  * Axis Labels
  * Centered Plot
  * X-Axis - time scale
  * Graph Legend
  * Linear/Cardinal/Basis

* Get info like:
  * Averages of time spent, data downloaded per day
  * Average Data downloaded per hour

* Create a Simple UI
  * Bootstrap

## <a name="changelog"></a>Changelog

3/1/2014:

* Did some design improvements to the graph

29/12/2013:

* Refactored the entire code of plotter.
* Plots time and bytes on the same graph.

28/12/2013:

* Restructured Files.
* Updated: A bug in dataset creation that was medding up the dates.

25/12/2013:

* Networx XMLs Parsed. Dataset created.

14/12/2013:

* Got D3 to work as I wanted. Onto datasets now...

15/11/2013:

* Wrote the Readme
* Moved from Python-Scripts to a brand new repo.
