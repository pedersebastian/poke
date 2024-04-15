from helper_funs import pokevenn
import pandas as pd
import os, PIL
from tqdm import tqdm



def main():
    res = []
    paths = os.listdir("bilder")

    for file in tqdm(paths):
        try:
            poke = pokevenn(f"bilder/{file}")
            res.append(poke)
        except:
            print(f"{file} funka ikke")
            
            

    df = pd.DataFrame(res)


    df.to_csv("pokevenner2.csv")
    
    
if __name__ == "__main__":
    main()

