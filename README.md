## Electrotactile feedback project
![image](https://github.com/zorgonide/Electrotactile-feedback/assets/48021258/29bbf9ec-2214-47af-b97b-ea1c35c8120d)

This is my masters project at the University of Glasgow. I am going to use a Functional Electric Stimulation machine, which has 4 electrodes connected to a person's shoulder. The nodes are -

- Left
- Right
- LeftFront
- RightFront

The nodes will be used for navigation; for example, turn left if the left shoulder buzzes. The goal is to design a pedestrian navigation system using electrotactile mode as haptic feedback. The code for the FES machine lies in [interface.py](./interface.py), and the library is [stim8updated.py](./stim8updated.py).
