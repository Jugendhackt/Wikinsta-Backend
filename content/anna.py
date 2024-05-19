print("hello world!")

import pandas
dataframe = pandas.read_html("https://de.wikipedia.org/wiki/Europawahl_2024")
print(dataframe[3])
tabelle3 = dataframe[3]
tabelle3 = tabelle3.transpose()
tabelle3 = tabelle3.drop(columns = [0,2,3])
tabelle3['kategorie'] = "politics"
tabelle3 = tabelle3.rename(columns = {1:"searchterm"})
tabelle3.to_csv("Tabelle3.csv", index = False)

#MUSIk_ALBEN
dataframe = pandas.read_html("https://de.wikipedia.org/wiki/Liste_der_meistverkauften_Musikalben")
print(dataframe[0])
tabelle_musik = dataframe[0]
tabelle_musik = tabelle_musik[["Interpret","Album"]]
interpreten = list(tabelle_musik["Interpret"])
print(interpreten)
Album = list(tabelle_musik["Album"])
print(Album)
searchterms = interpreten + Album
print(searchterms)
tabelle_musik = pandas.DataFrame(searchterms)
tabelle_musik = tabelle_musik.drop_duplicates()
tabelle_musik = tabelle_musik.rename(columns = {0:"searchterm"})
tabelle_musik['kategorie'] = "music"
tabelle_musik.to_csv("tabelle_musik.csv" , index = False)
print("erfolg")
