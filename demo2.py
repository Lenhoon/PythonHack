n = raw_input("please input a number n!")
n = int(n)
count = 0
for i in range(1, n + 1):
    while i != 0:
        if i % 10 == 1:
            count = count + 1
        i = i / 10

print count
