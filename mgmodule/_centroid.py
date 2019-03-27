def mg_centroid(image, width, height, color):
    #mgcentroid computes the centroid of an image/frame.
    if color == True:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #x = np.linspace(1,width,width); y = np.linspace(1,height,height)
    x = np.arange(width)
    y = np.arange(height)
    qom = cv2.sumElems(image)[0] #deles på width*height
    mx = np.mean(image,axis=0)
    my = np.mean(image,axis=1)
    comx = x.reshape(1,width)@mx.reshape(width,1)/np.sum(mx)
    comy = y.reshape(1,height)@my.reshape(height,1)/np.sum(my)
  
    com = np.zeros(2)
    com[0]=comx
    com[1]=comy

    return com, qom