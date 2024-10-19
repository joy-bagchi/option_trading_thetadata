import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
nd = np.random.normal(0, 1, 1000)
lnd = np.random.lognormal(0, 1, 1000)

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.hist(nd, bins=20, alpha=0.5, label='Normal Distribution')
ax2.hist(lnd, bins=20, alpha=0.5, label='Log-Normal Distribution')
ax1.legend()
ax2.legend()
plt.show()
