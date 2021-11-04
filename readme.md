# Tarea 1


| Código | Description |
| ------:| ----------- |
| ***Asignatura*** | Código del Trabajo o Número de Tarea | 
| **TSR-2022-I** | Tarea *01* |
| **Robotica-2022-I**  | Tarea *01* |
| **IT102321-C002** | Sistema Ciber-Físico - Proyecto - Módulo |

## Contenido

- [Objetivo](#objetivo)
- [Desarrollo](#desarrollo)
- [Conclusiones](#conclusiones)
- [Autor](#autor)
- [Referencias](#referencias)

## Objetivo

EL objetivo de este ejercicio es aplicar los temas de subscriptes y publicadores.


## Desarrollo

La soluciòn que le di a este ejercicio fue recibir los comandos por el usuario y solicitarle a que velocidad lineal/angular quiere que se este moviendo el robot. 
Para realizar lo anterior, lo que hice fue publicar en el paquete de /cmd_vel ya que este es el encargado de modificar las velocidades del robot:
self.vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

Lo siguiente que realice fue crear 3 funciones que pra mi son las màs importantes, la primera para pedirle a usuario los comandos y posteriormente digite las velocidades que se le pasaràn como paràmetros al robot, una segunda funciòn para recibir estos datos y publicarlos en el topico correspondiente y la ùltima, una funciòn para pedirle a usuario que escriba el comando "Detener" para parar al robot y asì cumplir con los objetivos de este ejercicio.

***Bloques de código***
#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
import time

class RobotControl():

    def __init__(self):
        rospy.init_node('pubnode', anonymous=True)
        self.vel_publisher = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        self.cmd = Twist()
        self.ctrl_c = False
        self.rate = rospy.Rate(10)
        rospy.on_shutdown(self.shutdownhook)

    def publish_once_in_cmd_vel(self):
        while not self.ctrl_c:
            connections = self.vel_publisher.get_num_connections()
            if connections > 0:
                self.vel_publisher.publish(self.cmd)
                break
            else:
                self.rate.sleep()

    def shutdownhook(self):
        self.stop_robot()
        self.ctrl_c = True

    def stop_robot(self):
        detener = raw_input('Escribar "Detener" para parar el robot: ')
        if(detener == "Detener"):
            rospy.loginfo("shutdown time! Stop the robot")
            self.cmd.linear.x = 0.0
            self.cmd.angular.z = 0.0
            self.publish_once_in_cmd_vel()

    def get_inputs_rotate(self):
        lectura_string = raw_input('Ingresa la entrada -> Avanzar / Girar : ')
        if lectura_string == "Girar":
            self.lineal_speed_x = 0
            clockwise_yn = raw_input('Quieres realizar el giro en sentido de las manecillas del reloj? (y/n): ')
            if clockwise_yn == "y":
                self.clockwise = True
            if clockwise_yn == "n":
                self.clockwise = False
            self.angular_speed_d = int(
                raw_input('Ingresa la velocidad angular (degrees): '))
            self.angle_d = int(raw_input('Ingresa el angulo (degrees): '))
        if lectura_string == "Avanzar":
            self.angular_speed_d = 0
            self.angle_d = 0
            self.clockwise = True
            self.lineal_speed_x = int(raw_input('Ingresa la velocidad lineal en x: '))
        return [self.angular_speed_d, self.angle_d,self.lineal_speed_x]

    def convert_degree_to_rad(self, speed_deg, angle_deg):
        self.angular_speed_r = speed_deg * 3.14 / 180
        self.angle_r = angle_deg * 3.14 / 180
        self.lineal_speed_r = 90
        return [self.angular_speed_r, self.angle_r]

    def rotate(self):
        self.cmd.linear.x = 0
        self.cmd.linear.y = 0
        self.cmd.linear.z = 0
        self.cmd.angular.x = 0
        self.cmd.angular.y = 0

        speed_d, angle_d, speed_x  = self.get_inputs_rotate()
        self.convert_degree_to_rad(speed_d, angle_d)

        if self.clockwise:
            self.cmd.angular.z = -abs(self.angular_speed_r)
        else:
            self.cmd.angular.z = abs(self.angular_speed_r)
        self.cmd.linear.x = speed_x
        rospy.loginfo(speed_x)

        t0 = rospy.Time.now().secs

        current_angle = 0

        while (current_angle < self.angle_r):

            self.vel_publisher.publish(self.cmd)
            t1 = rospy.Time.now().secs
            current_angle = self.angular_speed_r * (t1 - t0)
            self.rate.sleep()
        if(speed_x > 0):
            self.vel_publisher.publish(self.cmd)

if __name__ == '__main__':
    robotcontrol_object = RobotControl()
    try:
        res = robotcontrol_object.rotate()
    except rospy.ROSInterruptException:
        pass


## Conclusiones

Respecto al trabajo me pareciò complicado, no sentì que los conceptos estuvieron bien consolidados para dejar este trabajo pero ya al irlo desarrollando e investigando realmente fue cuando aprendì y pude avanzar con la soluciòn del programa. 
Necesito mejorar los temas de escuchar los nodos, listarlos y saber que topicos escuchar para saber que modificar que esto fue lo que màs trabajo me costo y que realmente era la clave para llegar a la soluciòn.

## Autor

**Autor** Avilez Bahena ALexander [GitHub profile](https://github.com/AlexanderAvilez)

## Referencias
https://www.youtube.com/watch?v=KPJnlRQ7Ng0