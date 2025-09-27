# immune_buider_handling

```bash
# Run Immune Builder
$ python run_immunebuilder.py -i data/rcsb_pdb_6B9Z.fasta -o results/trastuzumab_ib.pdb -H 6B9Z_2_HC -L 6B9Z_1_LC
Sequences found: ['6B9Z_1_LC', '6B9Z_2_HC', '6B9Z_3|Chain', '6B9Z_4|Chain']
✅ Predicted Fab saved to results/trastuzumab_ib.pdb

# Extract Fab from PDB
$ python extract_fab.py -p data/6B9Z.pdb -o data/6B9Z_fab.pdb -i data/rcsb_pdb_6B9Z.fasta -H 6B9Z_2_HC -L 6B9Z_1_LC
✅ Fv extracted with number_sequences → data/6B9Z_fab.pdb
```
