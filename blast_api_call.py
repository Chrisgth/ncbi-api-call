import argparse
import json
import zipfile

from Bio import Blast


def read_sequence(file_path):
    # Reads DNA sequence from a file
    with open(file_path, 'r') as file:
        return file.read().strip()


def blast_sequence(sequence):
    # Calls the BLAST api with given sequence
    result_stream = Blast.qblast("blastn", "nt", sequence, format_type='JSON2')

    with open('../myzipfile.zip', 'wb') as out_stream:
        out_stream.write(result_stream.read())

    result_stream.close()


def json_data_formatter():
    # Formats hit data for use in code using JSON
    my_zip_file = zipfile.ZipFile('../myzipfile.zip')
    json_file_name = my_zip_file.namelist()[1]
    data = my_zip_file.open(json_file_name).read().decode()
    json_data = json.loads(data)['BlastOutput2']['report']['results']['search']['hits']
    return json_data


def parse_results(json_data):
    # Formats data into a result list of dictionaries using JSON data
    results = []
    for hit in json_data:
        result = {
            'organism': hit['description'][0]['sciname'],
            'taxid': hit['description'][0]['taxid'],
            'accession': hit['description'][0]['accession']
        }
        results.append(result)
    return results


def display_results(results, length):
    # Displays results in CLI
    if not length:
        length = len(results)
    for i in range(0, length):
        result = results[i]
        print(f"Organism: {result['organism']}, Taxid: {result['taxid']}, Accession: {result['accession']}")


def args_validator():
    # Parses and validates arguments input by user and returns their values for use in code
    parser = argparse.ArgumentParser(description='DNA Sequence Analysis using NCBI BLAST API')
    parser.add_argument('-s', '--sequence', help='User typed DNA sequence')
    parser.add_argument('-f', '--file', help='File containing DNA sequence')
    parser.add_argument('-l', '--length', help='Valid positive integer, defaults to all hits returned')

    args = parser.parse_args()
    length = int()

    if not args.sequence and not args.file:
        raise ValueError("You must provide a typed DNA sequence or a file containing the sequence. Try using the"
                         " -s or -f flags")
    if args.length:
        try:
            length = int(args.length)
        except ValueError:
            raise ValueError("The length property must be an integer")

        if length < 1:
            raise ValueError("The length property must be a positive valid integer higher than 0")

    sequence = args.sequence if args.sequence else read_sequence(args.file)

    # Shorten sequence to avoid CPU overload error in the API
    if len(sequence) > 80:
        sequence = sequence[0:81]

    return {sequence: sequence, length: length or 0}


def main():
    # Combines the various methods used to interact with the CLI and the BLAST API
    sequence, length = args_validator()
    print("Running BLAST, this process may take up to a few minutes...")
    # The blast_sequence call can be omitted if you already have a zipfile from a previous API call
    # for debugging purposes.
    blast_sequence(sequence)
    formatted_data = json_data_formatter()
    results = parse_results(formatted_data)
    display_results(results, length)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f'ValueError: {e}')
    except Exception as e:
        print(f'An exception has occurred: {e}')
