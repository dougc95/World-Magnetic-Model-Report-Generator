def read_wmm_coefficients(file_path):
    """
    Reads WMM coefficients from the given WMM.COF file.
    Returns:
        epoch (float), and a list of tuples (n, m, gnm, hnm, dgnm, dhnm).
    """
    with open(file_path, "r") as f:
        lines = f.readlines()

    epoch = None
    coeff_data = []
    for line in lines:
        parts = [p for p in line.strip().split(" ") if p]
        if len(parts) == 3 and epoch is None:
            # Usually the line might be: "2020.0 ... ...", depending on WMM format
            try:
                epoch = float(parts[0])
            except ValueError:
                pass
        elif len(parts) >= 6:
            # This line should contain gnm, hnm, dgnm, dhnm
            # Format: n m gnm hnm dgnm dhnm
            n = int(parts[0])
            m = int(parts[1])
            gnm = float(parts[2])
            hnm = float(parts[3])
            dgnm = float(parts[4])
            dhnm = float(parts[5])
            coeff_data.append((n, m, gnm, hnm, dgnm, dhnm))

    if epoch is None:
        raise ValueError("Epoch not found in WMM file.")

    return epoch, coeff_data
