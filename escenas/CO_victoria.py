#Todas las funciones relacionadas a verificar las condiciones de victoria


#Verifica que se hallan matado todos los enemigos del nivel para poder pasartelo
def MatarTodosEnemigos(datos):
    cant_hab = datos["c_hab"]
    c = 0
    for i in range(1, cant_hab+1):
        #Verifica que las listas de enemigos esten vacias, para que asi concluya que no hay enemigos
        if (len(datos["habitaciones"][i]["enemigosM"])  == 0) and ( len(datos["habitaciones"][i]["enemigosD"])== 0):
            c += 1
    if c ==cant_hab:
        return True
    else:
        return False
     