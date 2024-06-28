# Preprocessing for BRAID
Simple Python class for performing text pre-processing on a CSV file.
Developed as part of the BRAID project at the University of Sheffield.

# Setting up Conda Environment for preprocessing.py

Install conda on your machine. Miniconda is recommended: https://docs.conda.io/en/latest/miniconda.html

To set up the Conda environment for running `preprocessing.py` on a unix machine, follow the steps below:

1. Navigate to the project directory:
    ```bash
    cd your-directory-where-the-code-is-stored
    ```

2. Create the Conda environment from the `environment.yml` file:
    ```bash
    conda env create -f environment.yml
    ```

3. Activate the Conda environment:
    ```bash
    conda activate braid
    ```

4. Make `preprocessing.py` executable:
    ```bash
    chmod +x preprocessing.py
    ```

5. Run `preprocessing.py`:
    ```bash
    python preprocessing.py
    ```

preprocessing.py can be run with command line arguments. The following are available:
1.  -h, --help:  Show this help message and exit
2.  --stop: Applies stopword removal to text.
3.  --stem: Applies stemming to text. Cannot be used in conjunction with --lemma.
4.  --lemma: Applies lemmatization to text. Cannot be used in conjunction with --stem.