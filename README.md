To run the script 'blast_api_call.py' open up any CLI tool on your computer and navigate to the directory of the project.

Once you have done so, run the command `python blast_api_call.py`, the command requires you to input a DNA
sequence either via the CLI or by inputting a file name. Examples being:
`python blast_api_call.py -f .\test_sequence_1.txt`
`python blast_api_call.py -f GACTCATTGATGCTATGATGTT`
The process can take up to several minutes, if the API returns a CPU exceeded error, shorten
the DNA sequence length.

Optionally you can also use the -l flag to limit how many results you would like to output into the cli,
example being:
`python blast_api_call.py -f .\test_sequence_1.txt -l 10`
This will return the first 10 formatted hits of the API call.

After the BLAST API call has been completed, a zipfile will be created with JSON data inside,
this is the data that is used to return hits via the CLI, if this data is needed to be used for debugging
purposes, the blast_sequence function call can be omitted for this sole reason, the function call
is denoted by a comment.

