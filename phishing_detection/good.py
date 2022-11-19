n = int(input())

output = []
for l in range(n):
    


    lis = list(map(int, input().split()))

    hotels = {}

    for i in range(lis[0]):
        z = list(input().split())

        hotels[int(z[1])] = [z[0], float(z[2])]


    for i in range(lis[1]):
        k = list(map(int, input().split()))

        max = 0


        for j in hotels.keys():
            if j < k[1] and hotels[j][1] > max:
                max = hotels[j][1]
                hotel = hotels[j][0]


        output.append(hotel)

    
for i in output:
    print(i)




        



        

