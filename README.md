# Get Highway Features

<!--start-->
Get highway features from ArcGIS network dataset.

## Getting Started

1 - Clone this repo.

2 - Create an environment with the requirements.
    
```
        > make env
```

3 - Explore - If you are more into Python, a good place to start is `jupyter lab` from the root of the project, and 
  look in the `./notebooks` directory. If GIS is more your schtick, open the project 
  `./arcgis/get-highway-features.aprx`.

## BumpVersion Cliff Notes

[Bump2Version](https://github.com/c4urself/bump2version) is preconfigured based on hints from 
[this article on Medium](https://williamhayes.medium.com/versioning-using-bumpversion-4d13c914e9b8).

If you want to...

- apply a patch, `bumpversion patch`
- update version with no breaking changes (minor version update), `bumpversion minor`
- update version with breaking changes (major version update), `bumpversion major`
- create a release (tagged in version control - Git), `bumpversion --tag release`
<!--end-->

<p><small>Project based on the <a target="_blank" href="https://github.com/knu2xs/cookiecutter-geoai">cookiecutter 
GeoAI project template</a>. This template, in turn, is simply an extension and light modification of the 
<a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project 
template</a>. #cookiecutterdatascience</small></p>
