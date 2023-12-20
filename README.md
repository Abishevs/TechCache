# TechCache - An Inventory Management Program for Small Warehouses such as Makerspaces/Workshops
![Status](https://img.shields.io/badge/Status-Under_Development-red)

## MOTO
With TechCache, track each bolt and nut.
So you can build and tweak, and never go nuts!

## Why?

When working with electronics, one knows how many small parts are needed
to be kept nearby. These are often purchased in bulk because you never
know when a specific part or component will be needed again. But over a
longer period, you may forget what was purchased and how much is left
P.S. It's a bit harder for screws, nuts, and bolts, but one usually
knows how much has been used and how much was bought. 

## Description

This program is intended to make it easier to keep track of all the
components in your workshop, for example, in 3D printing projects,
robotics, or similar activities.

In this program, you can save and keep track of how much you have of
each item, have descriptions/manuals, links to purchase sites, etc.

* Catppuccin Mocha themed :)

## Functionality
Created with Pyqt6

* Item information in a table view
* Edit/update item information by doubleclicking, to open an dialog box
* Add item, by clickin on a "+" button in bottom right corner 
* RegEx searching. All columns included
* Column sorting by clicking on the header
* Export/import database in csv format

## Installation on Unix 
Q: How to install on windows?. 
A: windows? what's that?

```bash
git clone https://github.com/Abishevs/TechCache.git 
cd TechCache
py -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage
```bash
cd src
py -m tech_cache.main
```
And then you can load in mock_data.csv, which is located in root
directory. To test how it looks

### TODO
- [ ] Add item delete functionality
- [ ] Add bulk select
- [ ] Create an pyinstaller

