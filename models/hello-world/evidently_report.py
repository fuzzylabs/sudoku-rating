

def main():
    df = pd.read_csv("../../data/sudoku-3m.csv").loc[:, ["clues"]]
    dashboard = Dashboard(tabs=[DataDriftTab(verbose_level=1)])

    dashboard.calculate(df[:100], df[100:200], column_mapping=None)
    dashboard.show()

if __name__ == "__main__":
    main()