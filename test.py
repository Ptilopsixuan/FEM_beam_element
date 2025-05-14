from mylib import type, reader

data1 = reader.readFile("input\\1.txt")
data1.integrateKe()
data1.integratePe()
result = [float(r) for r in data1.calculateA()]

print(result)
# print(data1.Kg)

data2 = reader.readFile("input\\2.txt")
data2.integrateKe()
data2.integratePe()

result = [float(r) for r in data2.calculateA()]
# print(data1.Kg == data2.Kg)
print(result)