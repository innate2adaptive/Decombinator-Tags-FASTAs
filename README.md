# Decombinator ancillary files


This repository contains the additional files required to run the [Decombinator **(v4)** TCR analysis pipeline](https://github.com/innate2adaptive/Decombinator). It contains several different types of files:

* FASTA files
    * These are simply the germline sequences for the TCR V and J genes, as directly downloaded from [IMGT/GENE-DB](http://www.imgt.org/genedb/).
    * Note that only one sequence is used per gene (that of the prototypic allele, i.e. TRxx*01). In cases where a single tag covers more than one gene only one sequence is used here.
    * Used by the ```Decombinator``` and ```CDR3translator``` scripts. 
    * These are standard FASTA format.
* Tag files
    * These are short sections of sequence which specifically identify the presence of particular genes in a TCR rearrangement.
    * Used by ```Decombinator```.
    * These are text files in a custom format where each line contains three pieces of information, separated by spaces:
        * Tag sequence
        * 'Jump' value, i.e. how far from the end of the gene in question is that tag (to allow determination of how many nucleotides were deleted)
        * Gene name 
* Translate files
    * These files contain the location of the conserved CDR3 junction-specifying amino acid residues in each gene covered by the software, and what those residues should be based on their germline sequence.
    * Used by the ```CDR3translator``` script.
    * These are in a comma delimited format, where the fields are:
        * Gene name
            * NB: this is the 'legacy' Decombinator gene name used for this tag, which in some cases will cover >1 gene
        * Position of the residue in the germline amino acid sequence of that gene (for that above named gene, which is the one used for translation purposes)
        * Identity of that residue (e.g. usually cysteine for V genes, or phenylalanine for J genes)
        * List of different genes covered by this tag, if indeed there are more than one (separated by '|' characters)
        * List of all alleles covered by this tag, as of [IMGT/GENE-DB](https://www.imgt.org/genedb/) accessing in April of 2020 (separated by '|' characters)
        * The [IMGT-labelled predicted functionalities](http://www.imgt.org/IMGTScientificChart/SequenceDescription/IMGTfunctionality.html#P1-2) of those covered genes (separated by '|' characters) 
            * F (functional), ORF (open reading frame), or P (pseudogene)
* CDR files
    * These are a recent addition, containing the amino acid sequences of the CDR1 and CDR2 of the genes as listed in IMGT (where known).
    * Used by the ```CDR3translator``` script.
    * As with the tags, these are in in a space delimited format where each field corresponds to:
        * Gene name
        * CDR1 sequence
        * CDR2 sequence 
      
That there are two 'tag sets' for humans, along with corresponding associated FASTA, translate, and CDR files. These are the 'original' and 'extended' tag sets. The original set was generated for the original [2013 Decombinator paper](http://dx.doi.org/10.1093/bioinformatics/btt004), and contains all of the prototypical alleles (i.e. '*01') for each 'functional' TCR gene. The extended set includes tags for the prototypical alleles of *all* genes, regardless of predicted functionality (including ORFs and pseudogenes), incorporated prior to the [2017 updated protocol/pipeline paper](https://doi.org/10.3389/fimmu.2017.01267). The order of appearance of genes in each file is conserved across each of the files (so the index of occurrence in one can be used to pull the corresponding information out of a different file). There is only one set of tags for mice (the original set).

Tags in the extended tag set are set slightly further back into their respective genes than the original set, making use of longer read technology to allow for a greater degree of non-template base removal during recombination.

Note that currently (early 2020) only the extended tag set is supported; original sets are left in for backwards compatibility. 