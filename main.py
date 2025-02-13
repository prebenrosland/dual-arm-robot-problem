import numpy as np
import matplotlib.pyplot as plt

def RPosFunction(angles):
    a, b = angles
    f = 4 * np.cos(a) + 3 * np.cos(b)
    g = 4 * np.sin(a) + 3 * np.sin(b)
    return np.array([f, g])

def QPosFunction(angles):
    a, b = angles
    f = 4 * np.cos(a)
    g = 4 * np.sin(a)
    return np.array([f, g])

def JacobianMatrix(angles):
    a, b = angles
    matrix = np.array([[-4 * np.sin(a), -3 * np.sin(b)], [4 * np.cos(a), 3 * np.cos(b)]])
    return matrix

def NewtonsMethod(function, matrix, angles):
    for i in range(10):
        delta = np.linalg.solve(matrix(angles), function(angles))
        angles -= delta
    return angles

h_0 = (np.arccos(0.8) + 0.1, (-np.pi / 2) + np.arccos(0.8) + 0.1)
R_hValues = np.linspace(0, np.sqrt(24), 10)

anglesList = [None] * len(R_hValues)
for i in range(len(R_hValues)):
    def NewtonIteration(inputAngles):
        return RPosFunction(inputAngles) - np.array([5, R_hValues[i]])


    anglesList[i] = NewtonsMethod(NewtonIteration, JacobianMatrix, h_0)

#Under er kode som printer ut verdier for alpha og beta, og kode som tegner robotarmen i de forskjellige posisjonene

print("Vinkler alfa og beta for R i x=5 fra h=0 til h=H \n")

color = 0
for i, (a, b) in enumerate(anglesList):
    print(
        f"R = (5, {R_hValues[i]:.2f}): "
        f"alfa = {a:.2f}({(a * 180) / np.pi:.1f}°), "
        f"beta = {b - a:.2f}({((b - a) * 180) / np.pi:.1f}°)")
    color += 100010
    if (color > 999999):
        color = "aa00aa"
    plt.plot([QPosFunction(anglesList[i])[0], RPosFunction(np.array([anglesList[i][0], anglesList[i][1]]))[0]],
             [QPosFunction(anglesList[i])[1], RPosFunction(np.array([anglesList[i][0], anglesList[i][1]]))[1]],
             color="#"+str(color), alpha=0.5)
    plt.plot([0, QPosFunction(anglesList[i])[0]], [0, QPosFunction(anglesList[i])[1]], color="#"+str(color), alpha=0.5)
    plt.text(5.1, R_hValues[i], ("R=(5, " + str(R_hValues[i].round(2)) + "), " + "Q=(" +
                                 str((QPosFunction(anglesList[i])[0]).round(2)) + ", " +
                                 str((QPosFunction(anglesList[i])[1]).round(2)) + ")"), fontsize=7)

plt.xlabel("x")
plt.ylabel("h")
plt.axis([-0.1, 7.1, -0.1, 5.1])
plt.show()

plt.xlabel("h")
plt.ylabel("angle")
plt.axis([0, 5, -2, 2])
for i, (a, b) in enumerate(anglesList):
    anglesList[i][1] = b - a
plt.plot(R_hValues, anglesList)
plt.text(2, 1.2, "alpha")
plt.text(2, -1.2, "beta")

plt.show()