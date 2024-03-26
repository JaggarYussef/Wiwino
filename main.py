from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy import select, Table, text
from sqlalchemy.orm import Session
import pandas as pd

engine = create_engine("sqlite:///vivino.db", echo=True)
inspector= inspect(engine)
session = Session(engine)
metadata_obj= MetaData()

wines_table = Table("grapes", metadata_obj, autoload_with=engine)


## TOP 10 wines that have a high ranking and ratings average in vintages toplist and relatively low ratings count from wine table -> Good wines but less reviewd
top_underated= text("""

SELECT DISTINCT wines.id, wines.name, vintage_toplists_rankings.rank, wines.ratings_average, wines.ratings_count, vintages.price_euros
FROM wines 
JOIN vintages ON vintages.wine_id = wines.id
JOIN vintage_toplists_rankings ON vintage_toplists_rankings.vintage_id = vintages.id
WHERE vintages.price_euros < 50
GROUP BY wines.id
ORDER BY wines.ratings_count ASC, vintage_toplists_rankings.rank ASC
LIMIT 10

""")

## We choose the country where we have the biggest amount of users with the least amount of wine assortiment. The supply for wines is low in these country persumably
one_country = text("""
SELECT 
    DISTINCT countries.name, 
    countries.users_count, 
    countries.wines_count, 
    countries.wineries_count, 
    (CAST(countries.wines_count AS REAL) /  countries.users_count) AS wine_per_user
FROM 
    countries
GROUP BY 
    countries.name
ORDER BY 
    wine_per_user ASC,
    countries.wines_count ASC, 
    countries.users_count DESC,  
    countries.wineries_count;
""")

table_names= inspector.get_table_names()

if __name__==  '__main__':
    print('Running main script...')

    # for table in table_names: 
    #     print(table)
    with engine.connect() as conn:
        result = conn.execute(one_country)
        df= pd.DataFrame(result.fetchall())
        print(df)
