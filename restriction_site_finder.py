"""Find restriction enzyme recognition sites in a DNA sequence."""


# Each enzyme is paired with the DNA sequence that it recognizes.
enzymes = {
    "1": ("SalI", "GTCGAC"),
    "2": ("BamHI", "GGATCC"),
    "3": ("HindIII", "AAGCTT"),
    "4": ("PstI", "CTGCAG"),
}


def read_fasta(filename):
    """Read a DNA sequence from a FASTA file."""
    sequence = ""

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            # FASTA header lines begin with > and are not part of the DNA.
            if not line.startswith(">"):
                sequence = sequence + line

    return sequence.upper()


def find_sites(sequence, recognition_sequence):
    """Return the 1-based positions of every recognition site."""
    positions = []
    search_from = 0

    while True:
        position = sequence.find(recognition_sequence, search_from)

        if position == -1:
            break

        # Python counts from 0, but biological sequence positions count from 1.
        positions.append(position + 1)
        search_from = position + 1

    return positions


def save_report(filename, enzyme_name, recognition_sequence, positions):
    """Save the restriction-site results in a plain-text file."""
    with open(filename, "w") as file:
        file.write("Restriction Site Finder Results\n")
        file.write("===============================\n")
        file.write("DNA record: pBR322 (J01749.1)\n")
        file.write("Enzyme: " + enzyme_name + "\n")
        file.write("Recognition sequence: " + recognition_sequence + "\n")
        file.write("Sites found: " + str(len(positions)) + "\n")

        if positions:
            position_text = ""

            for position in positions:
                if position_text != "":
                    position_text = position_text + ", "

                position_text = position_text + str(position)

            file.write("Site positions: " + position_text + "\n")
        else:
            file.write("Site positions: None\n")


def main():
    """Read pBR322, collect an enzyme choice, and report its sites."""
    print("================================")
    print("     Restriction Site Finder")
    print("================================")

    try:
        sequence = read_fasta("pbr322.fasta")
    except FileNotFoundError:
        print("The file pbr322.fasta was not found.")
        return

    if sequence == "":
        print("The FASTA file does not contain a DNA sequence.")
        return

    print("DNA record: pBR322 (J01749.1)")
    print("Sequence length:", len(sequence), "bp")
    print("\nChoose a restriction enzyme:")

    for number, enzyme in enzymes.items():
        print(number + ".", enzyme[0], "(" + enzyme[1] + ")")

    choice = input("\nEnter a choice (1 to 4): ").strip()

    if choice not in enzymes:
        print("Invalid choice. Enter a number from 1 to 4.")
        return

    enzyme_name, recognition_sequence = enzymes[choice]
    positions = find_sites(sequence, recognition_sequence)

    print("\nRestriction Site Results")
    print("------------------------")
    print("Enzyme:", enzyme_name)
    print("Recognition sequence:", recognition_sequence)
    print("Sites found:", len(positions))

    if positions:
        print("Site positions:", positions)
    else:
        print("Site positions: None")

    report_name = "restriction_sites.txt"
    save_report(
        report_name,
        enzyme_name,
        recognition_sequence,
        positions,
    )
    print("\nResults saved as:", report_name)


if __name__ == "__main__":
    main()
