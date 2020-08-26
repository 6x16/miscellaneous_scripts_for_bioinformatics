"""
This is a Python script to run BLAST on the MEGAHIT final contigs results.
Tutorial can be found: https://www.tutorialspoint.com/biopython/biopython_overview_of_blast.htm
"""
def main():
    from Bio.Blast import NCBIWWW
    import os
    from Bio import SeqIO
    from io import StringIO

    print("Start reading FASTA files...")
    os.chdir("/home/yikylee/Desktop/megahit")
    list_dir = [i for i in os.listdir() if i.find(".fa") >= 0]
    for fasta in list_dir:
        _prefix = fasta.split(".")[0]
        print("Now " + _prefix + "...")
        sequence_data = open(fasta).read()
        result_handle = NCBIWWW.qblast("blastn", "nt", sequence_data, format_type="Text", hitlist_size=10)
        print(_prefix + " analysis completed.")
        with open("./" + _prefix + "_result.txt", "w") as save_to:
            save_to.write(result_handle.read())
# Parameters:: database (nt); internal program (blastn).
# blast_results holds the result of our search.
# #It can be saved to a file for later use and also, parsed to get the details.
# We will learn how to do it in the coming section.

# Also, the same functionality can be done using Seq object as well.
# seq_record = next(SeqIO.parse(open('megahit/337_final.contigs.fa'),'fasta'))
# # seq_record.id
# # seq_record.seq
# result_handle = NCBIWWW.qblast("blastn", "nt", seq_record.seq)
# with open('results.xml', 'w') as save_file:
#     blast_results = result_handle.read()
#     save_file.write(blast_results)

if __name__ == '__main__':
    main()
