# GenomeAdaptation
Master thesis project, 

"""This code grows yeast-cells that divide and mutate to adapt to an evolutionary pressure (a toxic environment).
 The growth happens in cycles where at the end of each cycle the population is reduced to then regrow in the next cycle.
 Over these cycles, agents collect mutations that can change its cell cycle time, making it divide faster or slower.

 The size of such a change is determined by deletion data (i.e real measurements of yeast growth change for each Loss of
 ORF-function for each evolutionary pressure.
 The likelihood of such mutations is weighted by the yeast's number of Non-Synonymous nucleotides for each ORF."""

How to run the program:

  Simple discription
1. Download all the files. (Store them in the same folder)
2. Run Main.py

  Advanced discription
1. Download all the files in this repo. (Store them in the same folder)
2. If you have your own data to use, open LoadData.py and change the filenames to match the filenames of your data. 
For spesifics on how the data should look, see further below.
3. Open up InitilizeConstants.py and make sure the values are to your liking.
4. Run Main.py

This is how you set up the data: 

  First, make a unique fixed list of ORF names. (It can, but does not necessarily need to be sorted.)
Ex. 
YAL018C
YAL019W-A
YAL034C
...
This file exists so that, if we get a mutation at some index, we know what ORF that corresponds to.
But practically this data will only be useful in plotting. 

  Second, determine the Target size. 
For each ORF above, determine the number of non-synonymous mutations, and determine the number of mutations that will result in stop-codons. Note that only 1 out of 3 specific nucleotide mutations is going to result in an acctual stop-codon. So before adding the two numbers together, go ahead and divide the latter one with a third. This new number is the target size and reflects the probability that a LOF mutation for a particular ORF will occur.
Ex. 
4
0.667
7.333
...

  Third, For each ORF and each environment determine a number GT that will affect a cells cell cycle time like this:                           
new_cell cycle_time = old_cell_cycle_time + GT*old_cell_cycle_time 
This is the way a LOF mutation will affect its cells ability to grow.


                            

