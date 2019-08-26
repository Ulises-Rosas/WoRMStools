[![DOI](https://zenodo.org/badge/204058054.svg)](https://zenodo.org/badge/latestdoi/204058054)

# WoRMStools


Features:

- [x] get up-to-date information from [WoRMS database](http://www.marinespecies.org)
- [x] Terminal-based scripts

Software requierements:
* Python 3

#### Installation

By the moment, there's no need of further steps to install WoRMStools. You can just download this repository, unzip it and move into main directory in order to get access to executables. 

Using `git`:

1. clone it: `git clone https://github.com/Ulises-Rosas/WoRMStools.git`
2. move into:  `cd WoRMStools`

### AphiaID

We can obtain the species ID which WoRMS database identify a given species (i.e. aphiaID). If this ID is not known, then species cannot be validated or continue with downstream procedures. Therefore, to know species aphiaID is an important step towards getting metadata inside WoRMS database.

Let's suppose we have the following a list of species stored at [species.txt](https://github.com/Ulises-Rosas/WoRMStools/blob/master/species.txt):

```Shell
cat species.txt
```

```
Conus roosevelti
Latirus hemphilli
Favartia peasei
Lolliguncula panameusis
Pholoides tuberculata
```
We can obtain their aphiaIDs by running:
```Shell
./src/worms.py species.txt -id
```
By default worms.py uses its input to name all outputs, however this can be modified with `--out` option. Since we did not specify any output name, by default the output name is `species_worms_aphiaID.tsv` and is contains the following:

```Shell
species	aphiaIDs	Obs
Conus roosevelti	429945	
Latirus hemphilli	447141	
Favartia peasei	738152	
Lolliguncula panameusis		Record not found in WoRMS
Pholoides tuberculata		Record not found in WoRMS
```

### Validate names

Currently accepted name according to WoRMS for each species can be obtained with the option `-val`. The output, when using this option, has the following columns: **species**, **validated names** and **obs**. If there were species that cannot be validated through WoRMS, it is stated on the **obs** column. 

Example:
```Shell
./src/worms.py species.txt -val
```
By default the output name is `species_worms_val.tsv` and is contains the following:
```
species	validated names	Obs
Conus roosevelti	Conus tiaratus	
Latirus hemphilli	Pustulatirus hemphilli	
Favartia peasei	Favartia peasei	
Lolliguncula panameusis	Lolliguncula (Lolliguncula) panamensis	
Pholoides tuberculata		Record not found in WoRMS
```

### Synonyms

Synonyms of each species can be obtained with the option `-syn`. This option is aphiaID-dependent, which means that it obtains synonyms if there is any available aphiaID for each given species, including non-accepted ones. The output, when using this option, has the following columns: **species**, **synonyms** and **obs**. If there was a species that are not found in WoRMS its validated name is taken and stated on the **obs** column. Furthermore, if this species cannot be validated<sup>\*</sup>, it is also stated in the **obs** column.

Example:
```Shell
./src/worms.py species.txt -syn
```
By default the output name is `species_worms_syn.tsv` and is contains the following:
```
species	synonyms	Obs
Conus roosevelti		
Latirus hemphilli		
Favartia peasei	Murex foveolatus, Murex peasei	
Lolliguncula (Lolliguncula) panamensis	Lolliguncula panamensis, Lolliguncula tydeus	Deprecated name: Lolliguncula panameusis
Pholoides tuberculata		Record not found in WoRMS
```

*\*While species that does not have an aphiaID can be either validated in order to get an aphiaID or simply skipped, it is highly recomendable to introduce a list of validated species (see how [here](https://github.com/Ulises-Rosas/WoRMStools#validate-names)).*

### Taxonomic rank

Different taxonomical categories can obtained with the option `--at`. This option is aphiaID-dependent, which means that it obtains taxonomical categories if there is any aphiaID available for each given species, including non-accepted ones. The output, when using this option, varies according to introduced values into `--at` option (see example). The structure of column names, however, has the following structure: **\[Taxa\]** + **species** + **obs**. If there was a species that are not found in WoRMS its validated name is taken and stated on the **obs** column. Furthermore, if this species cannot be validated<sup>\*</sup>, it is also stated in the **obs** column.

Example:
```Shell
./src/worms.py species.txt --at Class Family
```
By default the output name is `species_worms_ranks.tsv` and is contains the following:
```
Class	Family	Species	Obs
Gastropoda	Conidae	Conus roosevelti	
Gastropoda	Fasciolariidae	Latirus hemphilli	
Gastropoda	Muricidae	Favartia peasei	
Cephalopoda	Loliginidae	Lolliguncula (Lolliguncula) panamensis	deprecated name: Lolliguncula panameusis
		Pholoides tuberculata	Record not found in WoRMS
```

Finally, this option can be used together with all above options.

*\*While species that does not have an aphiaID can be either validated in order to get an aphiaID or simply skipped, it is highly recomendable to introduce a list of validated species (see how [here](https://github.com/Ulises-Rosas/WoRMStools#validate-names)).*
