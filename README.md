# Continuous Implicit Authentication for Smartphones

This GitHub repository contains the source code and the documentation for the thesis **"Continuous implicit authentication of a smartphone user based on gesture and sensor data"**.

Aristotle University of Thessaloniki  
Electrical & Computer Engineering Department  
Intelligent Systems & Software Engineering Labgroup  
Author : [Emmanouil Christos](https://github.com/eachristgr)  
Supervisors : [Andreas Symeonidis](https://github.com/asymeon), [Thomas Karanikiotis](https://github.com/karanikiotis)

## Abstract
Smartphones have become an important assistant to everyday life chores and the information stored in them is constantly increasing. This fact raises the issue of the security of data exchanged through these devices, which is crucial to ensure the protection of the owner from malicious users. These days, most devices offer a level of security using various authentication methods, which however have been identified as vulnerable and thus the need has arisen for the development of new, more secure, methodologies. Thus, a lot of recent approaches are targeted towards continuous – implicit authentication techniques, i.e., systems that run continuously in the background of the device, without the need to perform actions on the part of the user. These systems typically use various data from a mobile phone or other devices, model the behavior of the user and then provide a unique or complementary level of security, which examines whether the current user's behavior is in line with that of the owner. Within the context of this diploma thesis, the developed system relies on sensor data available on most smartphones, such as the accelerometer, gyroscope and touch screen. The behavior of the phone owner is modeled with these data through the use of machine learning models, which can then make appropriate decisions. The proposed system differentiates from similar approaches through the use of a set of One Class Support Vector Machines, with a range of values for the parameters for each data type, which produces the probability that a behavior is in line with that of the owner, which is then used by a confidence system to decide if the device will be locked. As it turns out, such a system is easy to develop, can be adapted to the type of data available at any time and thus can bring significant improvements in user authentication in a continuous but non-invasive way.

---

The full report (GR) can be found [here]().  
For a brief overview of the problem, methodology and results you can have a look at the presentations([GR](), [EN]()).
