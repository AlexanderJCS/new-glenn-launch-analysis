import pickle

import pandas
import matplotlib.pyplot as plt


def main():
    with open("rocket_data.pickle", "rb") as f:
        data = pickle.load(f)
    
    df = pandas.DataFrame(data)
    
    df.to_csv("output.csv", index=False)
    
    # plt.plot(df["time"], df["stage1_alt"])
    # plt.show()


if __name__ == "__main__":
    main()
