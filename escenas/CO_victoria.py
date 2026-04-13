def MatarTodosEnemigos(datos):
    cant_hab = datos["c_hab"]
    c = 0
    
    for i in range(1, cant_hab+1):
        print(datos["habitaciones"][i]["enemigosM"])
        if len(datos["habitaciones"][i]["enemigosM"])  == 0:
            print("Verificacion que es")
            c = c +1
    if c ==cant_hab:
        return True
    else:
        return False
     