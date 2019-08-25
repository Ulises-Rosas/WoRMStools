# WoRMSTools

Features:

- [x] get up-to-date information from [WoRMS database](http://www.marinespecies.org)
- [x] Terminal-based scripts

Software requierements:
* Python 3

#### Installation

By the moment, there's no need of further steps to install WoRMStools. You can just download this repository, unzip it and move into main directory in order to get access to executables. 

Using `git`:

1. clone it: `git clone https://github.com/Ulises-Rosas/WoRMStools.git`
2. move into:  `WoRMStools`

### aphiaID

We can obtain the species ID which WoRMS database identify a given species (i.e. aphiaID). If this ID is not known, then species cannot be validated or continue with downstream procedures. Therefore, to know species aphiaID is an important step towards getting metadata inside WoRMS database.

Let's suppose we have the following a list of species stored at [species.txt](https://github.com/Ulises-Rosas/WoRMStools/blob/master/species.txt):

```Shell
cat species.txt
```
```
Chiton latus
Latirus hemphilli
Odontesthes regia
Lolliguncula panameusis
Pholoides tuberculata
```

