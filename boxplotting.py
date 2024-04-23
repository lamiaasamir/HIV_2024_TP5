import matplotlib.pyplot as plt

# Scores from different runs for the Number to Words Function
scores = [
    13.8505923555863,
    23.326334379905816,
    13.416666666666671,
    10.672396528704951,
    8.043810748999434
]

# Plotting the scores as a boxplot
plt.figure(figsize=(8, 6))
plt.boxplot([scores], patch_artist=True)  # Ensure to wrap scores in another list for boxplot
plt.title("Box Plot of Final Scores from 5 Runs for the Number to Words Function")
plt.ylabel("Score")
plt.grid(True)
plt.show()


# Scores from different runs for the password checker function
password_scores = [
    26.590699622957686,
    7.059460236381529,
    7.312169312169317,
    29.57644110275689,
    23.37566137566138
]

# Plotting the scores as a boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(password_scores, patch_artist=True)
plt.title("Box Plot of Final Scores from 5 Runs for the Password Checker Function")
plt.ylabel("Score")
plt.grid(True)
plt.show()