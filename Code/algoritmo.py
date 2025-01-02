
#LIBRERIAS
import cv2

import numpy as np

def obtenerRespuesta(img):
    canny= cv2.Canny(img,20,150)
    
    kernel = np.ones((5,5),np.uint8)
    borders=cv2.dilate(canny,kernel)
    #preguntas = input("Ingrese cantidad de preguntas")
    #SEGMENTACION
    
    contourns,hierarchy=cv2.findContours(borders, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    objetos = borders.copy()
    cv2.drawContours(objetos,[max(contourns,key=cv2.contourArea)], -1,255,thickness=-1)
    
    output= cv2.connectedComponentsWithStats(objetos,4,cv2.CV_32S)
    label=output[1]
    stats=output[2]
    
    mascara=np.uint8(255*(np.argmax(stats[:,4][1:])+1==label))
    
    #suavisamos con convex hull
    contourns,hierarchy=cv2.findContours(mascara,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnt= contourns[0]
    hull=cv2.convexHull(cnt)
    puntosConvexos= hull[:,0,:]
    m,n=mascara.shape
    ar=np.zeros((m,n))
    mascaraConvex=np.uint8(cv2.fillConvexPoly(ar, puntosConvexos, 1))
    
    #CORRECION PERPESPECTIVA
    vertices = cv2.goodFeaturesToTrack(mascaraConvex, 4, 0.01, 20) #detecta vertices 
            
    x=vertices[:,0,0]
    y=vertices[:,0,1]
         
    vertices=vertices[:,0 ,:]
    
    xo=np.sort(x)
    yo = np.sort(y)
    
    xn=np.zeros((1,4))
    yn= np.zeros((1,4))
    
    xn=(x==xo[2])*n+(x==xo[3])*n
    yn= (y==yo[2])*m+(y==yo[3])*m
    
    verticesN= np.zeros((4,2))
    verticesN[:,0]=xn
    verticesN[:,1]=yn
    
    vertices =np.int64(vertices)
    verticesN- np.int64(verticesN)
    
    #hacemos la homografia es decir trasladamos la imagen desde los puntos de vertices a vertices N
    
    h,_=cv2.findHomography(vertices, verticesN)
    img2 =cv2.warpPerspective(img, h, (n,m))
    
    #DIVIDIMOS
    #buscamos el porcentaje que representan las respuestas independientemente del tam de la imagen
    # luego dividimos dicha cantidad de col y nos da el porcentual que representa
    #desde el 23% de la img hasta el 86% de la misma
    
    roi = img2[:,np.uint64(0.23*n):np.uint64(0.86*n)]
    
    
    #EVALUACION
    #dividimos la img segun la cantidad de preguntas
    opciones=['A','B',"C","D",'E','X']
    respuestas=[]
    pregunta=[]
    cantidadPreguntas = 26
    cantidadRespuestas = 5
    for i in range(0,cantidadPreguntas):
        pregunta= (roi[np.int64(i*(m/cantidadPreguntas)):np.int64((i+1)*(m/26)) ,:])
        sumI =[]
        for j in range(0,cantidadRespuestas):
            _,col=pregunta.shape
            #divido cada respuesta y lo guardo en sumI
            sumI.append(np.sum(pregunta[:,np.uint64(j*(col/cantidadRespuestas)):np.uint64((j+1)*(col/cantidadRespuestas))]))
        vmin=np.ones((1,5))*np.min(sumI)
        #0.17*col*m es el valor de umbral
        if np.linalg.norm(sumI-vmin)>0.17*col*m:
            sumI.append(float('inf'))
        else: sumI.append(-1)
        respuestas.append(opciones[np.argmin(sumI)])
    return respuestas
    


