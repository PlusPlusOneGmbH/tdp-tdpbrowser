# TDP Browser
The Browser lists all installed tdp-packages in your current project and allows you to place Files and read the documentation. 

<img width="953" height="760" alt="grafik" src="https://github.com/user-attachments/assets/d4ccb0c3-cdd8-488d-8e97-5962efa25f09" />

You can adjust the search-behaviour as follows:
- Search with Keyword: Looks for "TouchDesignerPackage" in the installed packages keyword.
- Search with Prefix: Looks for packages that start with "tdp-"

Also, all packages that do not include a ToxFiles memeber will also be excluded.

To refresh the list simply press the "Refresh" parameter, call the .Update() method or use the refresh button in the UI.

The Browser will install a shortcut in to the UI to open it, but you can also press shortcut (default F7) to open to browser.

The Browser also has a button to open a commandline (not, windows only) for installing packages directly.

To place a File, simply double-click or drag and drop in to the network editor.


# Setup
Run the following in your textport to setup the browser.
```python
mod.tdptdpbrowser.Setup()
```