def serialize_general_stats(counts, bins, mean_diff, mean_years, mean_values):
    return {
        'counts': counts,
        'bins': bins,
        'mean_diff': mean_diff,
        'mean_years': mean_years,
        'mean_values': mean_values,
    }
