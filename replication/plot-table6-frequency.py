from matplotlib import font_manager as fm
import matplotlib.pyplot as plt

# Caminho absoluto para o arquivo TTF da Times New Roman
path_to_times = "/usr/share/fonts/truetype/msttcorefonts/times.ttf"  # Exemplo no Linux
times_new_roman = fm.FontProperties(fname=path_to_times)
times_bold = fm.FontProperties(fname=path_to_times, weight='bold')  # Fonte negrito

def plot_frequency_table(total_count, counts_by_criteria):
    """
    Plots a frequency table based on the provided counts.

    Parameters:
        total_count (dict): A dictionary with total counts of Pulumi, Terraform, AWS CDK.
        counts_by_criteria (list of tuples): List of tuples where each tuple contains:
            - criteria name (str)
            - dictionary of counts for that criteria
    """
    # Extract total counts and format with commas
    total_pulumi = total_count.get("Pulumi", 0)
    total_terraform = total_count.get("Terraform", 0)
    total_cdk = total_count.get("AWS CDK", 0)
    total_all = total_pulumi + total_terraform + total_cdk

    # Prepare data for rows with comma-formatted values
    rows = [
        ["Initial Repo. Count", f"{total_all:,}", f"{total_pulumi:,}", f"{total_terraform:,}", f"{total_cdk:,}"],
    ]

    # Add criteria rows with formatted counts
    for name, counts in counts_by_criteria:
        pulumi = counts.get("Pulumi", 0)
        terraform = counts.get("Terraform", 0)
        cdk = counts.get("AWS CDK", 0)
        total = pulumi + terraform + cdk
        rows.append([name, f"{total:,}", f"{pulumi:,}", f"{terraform:,}", f"{cdk:,}"])

    # Add final repository count (last criteria row)
    if counts_by_criteria:
        last_criteria_name, last_counts = counts_by_criteria[-1]
        last_pulumi = last_counts.get("Pulumi", 0)
        last_terraform = last_counts.get("Terraform", 0)
        last_cdk = last_counts.get("AWS CDK", 0)
        last_total = last_pulumi + last_terraform + last_cdk
        rows.append(["Final Repo. Count", f"{last_total:,}", f"{last_pulumi:,}", f"{last_terraform:,}", f"{last_cdk:,}"])

    # Create the table
    fig, ax = plt.subplots(figsize=(10, len(rows) * 0.5))
    ax.axis("off")

    # Prepare cell colors (no specific separator rows for now)
    cell_colors = []
    for row in rows:
        cell_colors.append(["white"] * 5)

    # Create the table
    table = ax.table(
        cellText=rows,
        colLabels=["", "TOTAL", "PULUMI", "TERRAFORM", "AWS CDK"],
        loc="center",
        cellLoc="right",
        colLoc="right",
        colColours=["w"] + ["white"] * 4,
        cellColours=cell_colors,
    )

    # Adjust alignment for the first column
    for row_idx in range(len(rows) + 1):
        cell = table[(row_idx, 0)]
        cell.set_text_props(ha="left", fontproperties=times_new_roman)

    # Set bold font for specific rows
    table[(1, 0)].set_text_props(fontproperties=times_bold)  # Initial Repo. Count
    table[(len(rows), 0)].set_text_props(fontproperties=times_bold)  # Final Repo. Count

    # Apply Times New Roman to all cells
    for (row_idx, col_idx), cell in table.get_celld().items():
        if (row_idx, col_idx) not in [(1, 0), (len(rows), 0)]:
            cell.set_text_props(fontproperties=times_new_roman)

    # Style table
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.auto_set_column_width(col=list(range(5)))

    # Remove left and right borders (only keep horizontal edges)
    for (row_idx, col_idx), cell in table.get_celld().items():
        cell.visible_edges = "horizontal"  # Only keep top and bottom borders
        cell.set_edgecolor("black")
        cell.set_linewidth(1)  # Adjust line thickness

    # Remove borders for criteria rows
    for (row_idx, col_idx), cell in table.get_celld().items():
        if 1 < row_idx <= len(counts_by_criteria) + 1:  # Rows corresponding to criteria
            cell.visible_edges = ""  # Remove all borders for criteria rows

    plt.show()


# Example usage
total_count = {"Pulumi": 1214, "Terraform": 301, "AWS CDK": 5183}
counts_by_criteria = [
    ("Criteria-1 (11% IaC Scripts)", {"Pulumi": 36, "Terraform": 8, "AWS CDK": 37}),
    ("Criteria-2 (Not a Clone)", {"Pulumi": 35, "Terraform": 8, "AWS CDK": 37}),
    ("Criteria-3 (Commits/Month >= 2)", {"Pulumi": 35, "Terraform": 7, "AWS CDK": 36}),
    ("Criteria-4 (Contributors >= 10)", {"Pulumi": 10, "Terraform": 0, "AWS CDK": 13}),
]

plot_frequency_table(total_count, counts_by_criteria)
