# GenomeAdaptation<br />
***Master thesis project***<br />
by: Timmy Forberg

"""This code grows yeast-cells that divide and mutate to adapt to an evolutionary pressure (a toxic environment).
 The growth happens in cycles where at the end of each cycle the population is reduced, to then regrow in the next cycle.
 Over these cycles, agents collect mutations that can change its cell cycle time, making it divide faster or slower depending on the mutation.

 The size of such a change is determined by deletion data (i.e real measurements of yeast growth change for each Loss of
 ORF-function for each evolutionary pressure.
 The likelihood of such mutations is weighted by the yeast's number of Non-Synonymous nucleotides for each ORF. For a more detailed description of the imported data see *Data set up* below."""

**How to run the program:**
Simple discription<br />
- Download all the files. (Store them in the same folder)<br />
- Run Main.py<br />
Advanced discription<br />
-  Download all the files in this repo. (Store them in the same folder)  <br />
-  If you have your own data to use, open LoadData.py and change the filenames to match the filenames of your data.   
For spesifics on how the data should look, see further below.<br />
-  Open up InitilizeConstants.py and make sure the values are to your liking.  <br />
-  Run Main.py

**Data set up:**

  First, make a unique fixed list of ORF names. (It can, but does not necessarily need to be sorted.)
Ex. <br />
YAL018C  <br />
YAL019W-A  <br />
YAL034C  <br />
...  
This file exists so that, if we get a mutation at some index, we know what ORF that corresponds to.
But practically this data will only be useful in plotting. 

  Second, determine the Target size. 
For each ORF above, determine the number of non-synonymous mutations, and determine the number of mutations that will result in stop-codons. Note that only 1 out of 3 specific nucleotide mutations is going to result in an acctual stop-codon. So before adding the two numbers together, go ahead and divide the latter one with a third. This new number is the target size and reflects the probability that a LOF mutation for a particular ORF will occur.
Ex. <br />
4  <br />
0.667  <br />
7.333  <br />
...  <br />

  Third, For each ORF and each environment determine a number GT that will affect a cells cell cycle time like this:                             
- new_cell cycle_time = old_cell_cycle_time + GT*old_cell_cycle_time  <br />
This is the way a LOF mutation will affect its cells ability to grow.


                            

