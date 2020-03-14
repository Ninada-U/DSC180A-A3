With the configuration file set, just run the python script.
The 'alignments' and 'fastq' folders need to be in the same directory as 
the script, and containing their index files.
The script will download and place corresponding data files into a 
corresponding data folder.

Below is information about setting up the configuration file:
There are three kinds of data: fastq, aligned, and variant. For whichever 
data dictionaries are present, the pipeline will fetch that data with 
the parameters as filters. For example:

config = {
    'fastq': {
        'withdrawn': 0,
        'analysis group': 'low coverage'
    },
    'index': 4
}

This will fetch low coverage fastq data that was not withdrawn, starting 
with the 4th file in the list.

And,

config = {
    'variant': {

    }, 
    'index': 5
}

This will fetch variant data starting with the 5th file.

The available parameters are as follows:

fastq
  withdrawn: [0, 1]
  analysis group: ['low coverage', 'high coverage', 'exome']
aligned
  analysis group: ['low coverage', 'high coverage', 'exome']
variant: n/a