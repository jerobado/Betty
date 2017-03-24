CHANGELOG
---------
All notable changes to this project will be documented on this file.

**Patch 0.7**

_Release date: 2017-06-01_ [unreleased]

* User Interface (UI)
    * [**TODO**] A new hint will pop-up will appear when the user hover the mouse pointer in one of the entries in the tracker, this will show the template details entered. [ISSUE #2](https://github.com/mokachokokarbon/Betty/issues/2)
    * The last known size of the _Tracker_ can now be retrieved.
* Development (the bloody part)
    * Betty is now implemented in Python 3.6.0 and in PyQt 5.7.1
    * Reimplemented how the app will restore its geometry and state.


**Patch 0.6**

_Release date: 2016-12-01_

* Highlight(s) 
    * Changes in the _Set Criteria_ fields can now be seen in the Preview box on both _Filing_ and _Searching_ template forms.
    * Added _Access keys_ on both _Filing_ and _Searching_ template forms by holding the `ALT` key.
* Filing
    * Added an **Intent to Use** checkbox (_"Please file on intent to use basis if applicable in your jurisdiction."_).
    * Changed _Unilever_ to **Others** in the client selection box.
    * Changed the _Preview_ button into **Copy All** button.
* Searching
    * Changed the _Preview_ button into **Copy All** button.

**Patch 0.5**

_Release date: 2016-09-01_

* Fixed
    * Fixed an issue in the _Add new Template_ dialog wherein the `Return` and `Enter` keys are not accepted when pressed.
* User Interface (UI)
    * Added a naming convention on the main window's title bar. 
	* Added an icon identifier in the _Add new Template_ dialog box.
	* Added an icon identifier in the _Tracker_.
	* Changed how the user interacts with the _Tracker_: A **clicked** will retrieve the template and **double-clicked** will now edit the selected item on the list.
* Filing
    * Lowercase characters entered in the _TMNC_ field are now converted into uppercase in the _Preview_ box.
* Searching
    * Added _Abbott_ as new client in Searching form.
    * Updated the _With Artwork_ special instruction as per process update.
    

**Patch 0.4**

_Release date: 2016-07-01_

* User Interface (UI)
    * Resize the main window to make it larger 
    * Retains the last known window size and position after closing the application
    * Revamp the 'About' section to show basic information about the application
* Filing
    * Added client selection in Filing form (GE and Unilever)
    * Added default special instructions in GE
* Searching
    * Added _Google_ as new client in Searching form
    * Added default special instruction in Google
    * Formatted the special instruction _"Artwork attached to illustrate..."_ into Bold 


**Patch 0.3**

_Release date: 2015-12-01_

* User Interface (UI)
    * Added Template tracker
    * Added sub-menu 'Append Template'      
* Filing
    * Added Filing template/form
* Searching
    * Added Marker field for tracking purposes


**Patch 0.2**

Release date: 2015-05-29

* Searching
    * Added Searching template/form


**Patch 0.1**

_Date created: 2015-03-10_

* Initial
    * Added everything here :)