# DeepReinforcementLearning
A replica of the AlphaZero methodology in Python

See this article for a summary of the algorithm and run instructions.

https://applied-data.science/blog/how-to-build-your-own-alphazero-ai-using-python-and-keras/


## GETTING STARTED
To start the learning process, run the top two panels in the run.ipynb Jupyter notebook. Panel two does all the work, so only when it has built up enough game positions to fill its memory will the neural network begin training.

Therefore, you will need to leave the notebook running until it reaches the MEMORY_SIZE, specified in the config.py file, which defaults to "30000". The output from panel 2 will project how long it will take.

<strong>This initial training can take many hours</strong> and if you stop it before 
the MEMORY_SIZE parameter is reached, you will not get a model in run/models directory and 
the next cells in run.ipynb will not work. so... have some patience during training!
