# evaluation/imgt.py
IMGT_REGIONS = {
    "FR-H1": (1, 26),
    "CDR-H1": (27, 38),
    "FR-H2": (39, 55),
    "CDR-H2": (56, 65),
    "FR-H3": (66, 104),
    "CDR-H3": (105, 117),
    "FR-H4": (118, 129),
    # Light 鎖も必要なら追記
}

def assign_regions(anarci_output):
    """
    ANARCI出力をIMGT定義にマッピング
    anarci_output: [(pos, aa), ...]
    """
    region_map = {}
    for region, (start, end) in IMGT_REGIONS.items():
        region_map[region] = [pos for pos, aa in anarci_output if start <= int(pos) <= end]
    return region_map
