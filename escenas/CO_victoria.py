def MatarTodosEnemigos(datos):
    cant_hab = datos["c_hab"]
    c = 0
    
    for i in range(1, cant_hab+1):
        
        if (len(datos["habitaciones"][i]["enemigosM"])  == 0) and ( len(datos["habitaciones"][i]["enemigosD"])== 0):
            c += 1
    if c ==cant_hab:
        return True
    else:
        return False
     