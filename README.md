# Incorporate all GitHub forks as branches

When a GitHub project has a lot of forks, sometimes it's difficult to understand which forks have useful activity. There is a "Network" menu of the "Forks" tab, but it has limitations.

Therefore, here is `diggforks`, a utility that finds all forks with GitHub API and explicitly fetches them as branches into the target repository. Then the contents of forks can be visually inspected with advanced logging tools, such as [tably](https://stackoverflow.com/a/61487052/4063520) or VSCode extensions, if you wish.


## Prerequsites

* Create GitHub API token and store it in `~/.diggforks`
* Use [tably](https://stackoverflow.com/a/61487052/4063520) git log formatting, by adding the `tably` command to `.gitconfig` (Note: this procedure is not going to break any existing `.gitconfig` tweaks):

    ```
    cat tably.gitconfig >> ~/.gitconfig
    ```

* With `less` and `more` formatting of `tably` is broken, so use [moar](https://github.com/walles/moar) to have properly formatted colorful pagination


## Usage

Change the current directory to the Git repository of interest and then run:

```
python3 ../diggforks/diggforks.py
git tably mylog3 | moar
```


# TODO

1. Add `setup.py`
2. Add GIF

