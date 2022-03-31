Human behaviour while trying to escape from a room under panic is a widely studied issue in complex systems research. Many scientists have called attention to the fact that placing an obstacle on a suitable place near the exit can improve the evacuation time from the room (Helbing et al. (2000, 2005), Hughes (2003), Johansson and Helbing (2005), Piccoli and Tosin (2009), etc).

We can try to design a platform to monitor crowd density near exits and intervene in the crowd behaviour to improve the congestion situation in real-time.

1.  Place obstacles near exits based on the current crowd research model.The system uses multiple cameras to collect videos of crowds in different places near the exit in real time as the data input. 
    
2.  Use the PyTorch neural network framework to build CSRNet and export the human flow monitoring model. 
    
3.  Use KV260 to transform the exported network model and achieve inference optimization acceleration. 
    
4.  When crowd density exceeds a threshold, activate the suitable obstacles to accelerate crowd evacuation.

Artificial intelligence requires high computing speed and high energy consumption as a result. However, most of the existing artificial intelligence deployments are based on GPUs, which cannot give full play to the advantages of parallel computing in the application process and require considerably high power. With FPGA architecture, KV260 trains and deploys neural networks with faster computing speed and lower energy consumption, which is greatly suitable for edge intelligent application scenarios. 


