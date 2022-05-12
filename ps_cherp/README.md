ps_cherp README
===============

Scripts to read MIT data for a house election and output the fictional results under the "Pun Salad Crackpot
House Election Reform Proposal (ps_cherp).

There are two equivalent scripts, one Perl (ps_cherp), one Python (ps_cherp.py). In limited testing, they
generate the same results.

Each takes an election year (1976, 1978, ..., 2020) as a command line argument.
It assumes you've downloaded the MIT Election Lab CSV spreadsheet from [here](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IG0UN2) to your Linux "Downloads" directory ($HOME/Downloads).

I wrote the Perl script first, and it's more polished with moderate commenting. "perlcritic" likes it at its most
stringent setting.

The Python script is an afterthought, just thought I'd see if I could do it. I don't know Python at all, and
it was (more or less) brute-force translated from Perl, with a lot of Googling. It probably would make an experience Pythoner blanch.

Much more detail is at my blog, Pun Salad, right [here](https://punsalad.com/cgi-bin/ps?spec=2022/05/11/1652297303).

