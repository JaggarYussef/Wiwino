from sqlalchemy import create_engine, inspect, MetaData
from sqlalchemy import select, Table, text
from sqlalchemy.orm import Session
import pandas as pd

engine = create_engine("sqlite:///vivino.db", echo=True)
inspector= inspect(engine)
metadata_obj= MetaData()
wines_table = Table("grapes", metadata_obj, metadata_obj,  autoload_with=engine)

#QUESTION 1
## TOP 10 wines that have a high ranking and ratings average in vintages toplist and relatively low ratings count from wine table -> Good wines but less reviewd
top_underated= text("""

SELECT DISTINCT wines.id, wines.name, vintage_toplists_rankings.rank, wines.ratings_average, wines.ratings_count, vintages.price_euros
FROM wines 
JOIN vintages ON vintages.wine_id = wines.id
JOIN vintage_toplists_rankings ON vintage_toplists_rankings.vintage_id = vintages.id
WHERE vintages.price_euros < 50
GROUP BY wines.id
ORDER BY wines.ratings_count DESC, vintage_toplists_rankings.rank DESC
LIMIT 10

""")
                    
"""
TOP UNDERATED WINES QUERY RESULT 

        id                                            name  rank  ratings_average  ratings_count  price_euros
0    11890  60 Sessantanni Old Vines Primitivo di Manduria    17              4.5          94289        24.75
1     7103             Amarone della Valpolicella Classico     4              4.3          77515        49.80
2  1139434                                           Tinto     1              4.4          65625        42.95
3    11604                                       Malleolus    18              4.3          34630        35.95
4  1174845            Sauternes (Premier Grand Cru Classé)     4              4.3          17293        49.90
5  1251730                        Reserva Ribera del Duero     1              4.3          11233        39.55
6  6331780                           Guerriero della Terra     1              4.4          10185        27.40
7  6139455                    Limited Edition 10 Vendemmie     5              4.5           9453        34.20
8  1468452                                    Lupi Rezerva    15              4.5           7604        36.55
9    16221                                        Series M     7              4.4           2995        48.00


"""                    


#QUESTION 2
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
                   
"""
COUNTRY TO INVEST QUERY RESULT 
              name  users_count  wines_count  wineries_count  wine_per_user
0       États-Unis     12273684       204060           28145       0.016626
1           Suisse      1601799        33656            3849       0.021011
2         Roumanie       228185         6841             686       0.029980
3         Portugal      1123535        39847            5834       0.035466
4           Israël       150549         5435             529       0.036101
5          Espagne      2264396       102662           18026       0.045337
6        Argentine       629532        36121            5339       0.057378
7           Italie      4270717       274658           42399       0.064312
8        Allemagne      2549989       164533           13643       0.064523
9           France      5973301       422503           67553       0.070732
10       Australie      1022965        90954           13946       0.088912
11         Croatie        64223         5880             980       0.091556
12           Grèce        95693         9581            1294       0.100122
13  Afrique du Sud       269649        30857            4227       0.114434
14           Chili       326757        41191            5785       0.126060
15         Hongrie       102235        16605            1923       0.162420
16        Moldavie        13583         5055             418       0.372156

"""
#QUESTION 3
# TOP THREE WINERIES. WE COULD ONLY RETURN THREE wineries that had enough data. Lots of missing data to corelate. WE TAKE WINERIES WITH MOST POSTIVE  REVIEW AND COUNTS 
top_three = text("""
SELECT wineries.id, wineries.name, wines.winery_id, wines.name, wines.ratings_average, wines.ratings_count
FROM wineries
JOIN wines ON wines.winery_id = wineries.id
GROUP BY wines.winery_id
ORDER BY wines.ratings_count DESC
LIMIT 10


""")
"""
TOP THREE WINERIES QUERY RESULT:
     id                                  name  winery_id                              name  ratings_average  ratings_count
0   1471                                 Siepi       1471  Lion Tamer Napa Valley Red Blend              4.3           4981
1   1651            Tenuta Tignanello 'Solaia'       1651                 The Armagh Shiraz              4.5           2472
2   1652                            Tignanello       1652                    Colheita Porto              4.4            741
3  75712  Corte di Cama Sforzato di Valtellina      75712                      Raut Lagrein              4.5             58
"""                 
                
inspect_groups= text("""
SELECT keywords_wine.group_name, keywords.name, keywords_wine.wine_id
FROM keywords_wine
JOIN keywords ON keywords.id = keywords_wine.keyword_id
WHERE keywords.name= 'citrus'
GROUP BY keywords_wine.group_name
LIMIT 15
JOIN wines ON wines.id = keywords_wine.wine_id

""")    


"""
SELECT DISTINCT 
    CASE 
        WHEN keywords.name IN ('coffee', 'toast', 'cream', 'citrus', 'green_apple') THEN 'Bold' 
    END AS Bold,
    keywords.name,
    keywords_wine.wine_id
FROM 
    keywords_wine
JOIN 
    keywords ON keywords.id = keywords_wine.keyword_id
WHERE 
    keywords.name IN ('coffee', 'toast', 'cream', 'citrus', 'green_apple') 
    AND keywords_wine.count > 10;
"""
#QUESTION 4
# WINES WITH CERTAIN KEYWORDS FOR TASTES THAT ARE CONSIDERED BOLD 
group_name= text("""
SELECT DISTINCT keywords_wine.group_name, keywords.name, keywords_wine.wine_id
FROM keywords_wine
JOIN keywords ON keywords.id = keywords_wine.keyword_id

WHERE keywords.name IN ('coffee', 'toast', 'cream', 'citrus', 'green_apple') AND keywords_wine.count > 10

""")       

#QUESTION 5
# BEST RATED WINES BY TYPE OF GRAPE AND AVAILABILITY 
best_grapes= text(
"""
SELECT DISTINCT 
most_used_grapes_per_country.grape_id, grapes.name, most_used_grapes_per_country.country_code,  most_used_grapes_per_country.wines_count, wines.ratings_average
FROM most_used_grapes_per_country
JOIN grapes ON grapes.id= most_used_grapes_per_country.grape_id
JOIN countries ON countries.code =  most_used_grapes_per_country.country_code
JOIN regions ON regions.country_code = countries.code
JOIN wines ON wines.region_id = regions.id
WHERE wines.ratings_average > 4.5
GROUP BY  most_used_grapes_per_country.grape_id
ORDER BY  wines.ratings_average DESC, most_used_grapes_per_country.wines_count DESC
"""
)

"""
BEST GRAPES RESULTS 
    grape_id                name country_code  wines_count  ratings_average
0          1        Shiraz/Syrah           au       551112              4.7
1          2  Cabernet Sauvignon           us       801751              4.6
2          5          Chardonnay           it       604208              4.6
3         14          Pinot Noir           us       572334              4.6
4         10              Merlot           it       566719              4.6
5         15            Riesling           de       262136              4.6
6          9              Malbec           ar       219735              4.6
7         19         Tempranillo           es       172842              4.6
8         16          Sangiovese           it       125094              4.6
9         67    Touriga Nacional           pt        85787              4.6
10       142            Garnacha           es        58111              4.6
11       299       Spätburgunder           de        50164              4.6
12        51           Carménère           cl        50087              4.6
13        69         Tinta Roriz           pt        41047              4.6
14        68      Touriga Franca           pt        33763              4.6
15       355      Weissburgunder           de        33464              4.6
16       394             Furmint           hu        11130              4.6
"""

#QUESTION 6
# AVERAGE WINE RATING FOR EACH COUNTRY 
leaderboard= text(
    
"""
SELECT countries.name, wines.ratings_average, avg(wines.ratings_average) AS average 
FROM countries
JOIN regions ON regions.country_code = countries.code
JOIN wines ON wines.region_id = regions.id
GROUP BY countries.name
ORDER BY average DESC
"""
)

"""
              name  ratings_average   average
0        Allemagne              4.4  4.500000
1           Israël              4.5  4.500000
2       États-Unis              4.3  4.490541
3         Moldavie              4.5  4.480000
4          Hongrie              4.6  4.472727
5   Afrique du Sud              4.5  4.459091
6        Australie              4.4  4.458333
7           France              4.4  4.447130
8          Espagne              4.2  4.443617
9         Portugal              4.4  4.435714
10           Chili              4.6  4.431250
11          Italie              4.6  4.430026
12       Argentine              4.4  4.417391
13        Roumanie              4.4  4.400000
14           Grèce              4.4  4.400000
15          Suisse              4.4  4.350000
16         Croatie              4.3  4.300000

"""
#QUESTION 7
# TOP CHOICES FOR CABERNET SAUVIGNON
top_cabernet_sauvignon= text("""

SELECT grapes.name as grape_name, wines.name, wines.ratings_average
FROM grapes
JOIN most_used_grapes_per_country ON most_used_grapes_per_country.grape_id = grapes.id
JOIN regions ON regions.country_code = most_used_grapes_per_country.country_code 
JOIN wines ON wines.region_id = regions.id
WHERE grapes.name = 'Cabernet Sauvignon'
ORDER BY wines.ratings_average DESC
LIMIT 5


""")
                             
"""
CABERNET SAUVINGION PICKED  BASED ON BEST RATING
           grape_name                                  name  ratings_average
0  Cabernet Sauvignon                    Cabernet Sauvignon              4.8
1  Cabernet Sauvignon                                Mágico              4.8
2  Cabernet Sauvignon                         IX Estate Red              4.7
3  Cabernet Sauvignon  Special Selection Cabernet Sauvignon              4.7
4  Cabernet Sauvignon        Unico Reserva Especial Edición              4.7
"""
                             

table_names= inspector.get_table_names()

if __name__==  '__main__':
    print('Running main script...')

    with engine.connect() as conn:
        top_cabernet_sauvignon_result = pd.DataFrame(conn.execute(top_cabernet_sauvignon).fetchall())
        leaderboard_result= pd.DataFrame(conn.execute(leaderboard).fetchall())
        best_grapes_result= pd.DataFrame(conn.execute(best_grapes).fetchall())
        top_three_result= pd.DataFrame(conn.execute(top_three).fetchall())
        top_underated_result= pd.DataFrame(conn.execute(top_underated).fetchall())
        one_country_result = pd.DataFrame(conn.execute(one_country).fetchall())
        group_name_result= pd.DataFrame(conn.execute(group_name).fetchall())
  
        print(top_cabernet_sauvignon_result)
