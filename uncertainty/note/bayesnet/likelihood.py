from model import model
import numpy as np
import torch


rain_values = ["none", "light", "heavy"]
maintenance_values = ["yes", "no"]
train_values = ["on time", "delayed"]
appoinment_values = ["attend", "miss"]

data = np.array([
    [rain_values.index("none"),
     maintenance_values.index("no"),
     train_values.index("on time"),
     appoinment_values.index("attend")
    ]
]
)
probability = model.probability(torch.as_tensor(data))

print(probability)
