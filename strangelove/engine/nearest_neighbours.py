from strangelove.engine import base

def pearsonSimilarity(ratings, x, y ):
    #save movies that both users have been rated
    movieDict={}
    for movie in ratings[x]:
        if movie in ratings[y]:
            movieDict[movie] = 1
            N = len(movieDict)
    #could not find pair, then return
    if N == 0:
        return -1
    # sum of scores
    Ex = sum([ratings[x][movie] for movie in movieDict])
    Ey = sum([ratings[y][movie] for movie in movieDict])
    # sum of squared scores
    Ex2 = sum([pow(ratings[x][movie],2) for movie in movieDict])
    Ey2 = sum([pow(ratings[y][movie],2) for movie in movieDict])
    #sum of the products of paired scores
    Exy = sum([ratings[x][movie] * ratings[y][movie] for movie in movieDict])
    #pearson formula =
    numerator = (N*Exy - Ex*Ey)
    denom1 = Ex2 - pow(Ex,2)/N
    denom2 = Ey2 - pow(Ey,2)/N
    denominator = math.sqrt(denom1 * denom2)
    if denominator == 0: return -2 #divide by zero exception since not sure if it automatically gives error
    r = numerator / denominator
    return r