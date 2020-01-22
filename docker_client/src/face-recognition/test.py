test = {"matthew" : 5 ,"junior" :5, "alain" : 5}
test2 = {"matthew" : 10 ,"junior" :10, "alain" : 10}
best_id_moy = {k: (test[k] * (5) + test2[k]) / 2 for k in test2}
print (best_id_moy)
