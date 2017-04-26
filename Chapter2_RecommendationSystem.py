__author__ = 'chaliu'
import csv
import math


class recommender:
    def __init__(self,data_file,k=1,metric='pearson',n=5):
        self.user_data=self.__get_user_data(data_file)
        self.k=k
        self.metric=metric
        self.n=n
        if self.metric=='pearson':
            self.fn=self.pearson
        elif self.metric=='cosine_similarity':
            self.fn=self.cosine_similarity

        elif self.metric=='minkowski':
            self.fn=self.compute_Minkowski

    def pearson(self,rating1,rating2):
        result1=0
        result2=[0,0]
        result3=[0,0]
        result4=[0,0]
        count=0
        for item in rating1:
            if item in rating2:
                count+=1
                result1+=rating1[item]*rating2[item]
                result2[0]+=rating1[item]
                result2[1]+=rating2[item]
                result3[0]+=rating1[item]**2
                result3[1]+=rating1[item]
                result4[0]+=rating2[item]**2
                result4[1]+=rating2[item]
        result2.append(result2[0]*result2[1]/count)
        result3.append(pow(result3[0]-result3[1]**2/count,
                           0.5))
        result4.append(pow(result4[0]-result4[1]**2/count,
                           0.5))

        return (result1-result2[2])/(result3[2]*result4[2])

    def cosine_similarity(self,rating1,rating2):
        distance=0.0
        x = 0
        y = [0.0,0.0]
        for item in rating1:
            x+=rating1[item]*rating2[item]
            y[0]+=rating1[item]**2
            y[1]+=rating2[item]**2

        distance = x/pow(y[0]*y[1],0.5)

        return distance

    def compute_Minkowski(self,rating1,rating2,r):
        distance = 0.0
        for key in rating1:
            if key in rating2:
                distance += pow(abs(rating1[key] - rating2[key]),r)
        return round(math.pow(distance,-r),3)

    def computeNearestNeighbor(self,username,users):
        distances = []
        for user in users:
            if user != username:
                # distance = (compute_manhattan(users[user], users[username]))
                if self.metric=='minkowski':
                    distance=self.fn(users[user],users[username],2)
                else:
                    distance=self.fn(users[user],users[username])
                distances.append((distance, user))
        # sort based on distance - closest first
        distances.sort()
        return distances

    def __get_user_data(self,csv_file):
        with open(csv_file) as f:
            f_csv=csv.reader(f)
            header=next(f_csv)
            names=header[1:]
            user_data={}.fromkeys(names)
            for key in user_data:
                user_data[key]=dict()
            for row in f_csv:
                for name in names:
                    user_data[name][row[0]]=row[header.index(name)]
        return user_data


    def recommend(self,users,username):
        recommendations={}

        nearest=self.computeNearestNeighbor(users,username)
        n_nearest=nearest[:self.n-1]
        weight=dict()
        total_distance=0.0
        for key in n_nearest:
            total_distance+=n_nearest[key]
        for key in n_nearest:
            weight[key]=n_nearest[key]/total_distance

        for key in user_data[username]:
            #if user don't have related record, then generate corresponding record
            if user_data[username][key]=='':
                score=0.0
                for name in n_nearest:
                    score+=weight[name]*user_data[name][key]
                recommendations[key]=score

        return recommendations

if __name__ =='__main__':
    data1=r'C:\Localdata\Study\Python\DM\Data\Movie_Ratings.csv'
    my_recommender=recommender(data1,metric='cosine')
    user_data=my_recommender.user_data
    my_recommender.recommend('Gary',user_data)