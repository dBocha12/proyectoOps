variable "aws_region" {
  description = "Region donde se creara la maquina"
  type        = string
  default     = "us-east-1"
}

variable "aws_ami" {
  description = "AMI Usada para crear la maquina"
  type        = string
  default     = "ami-0e1bed4f06a3b463d"
}

variable "aws_instance_type" {
  description = "Tipo de instancia a usar para la maquina"
  type        = string
  default     = "t3.micro"
}

variable "aws_key_name" {
  description = "La llave que se utilizara para crear la maquina, la llave debe estar creada con anticipacion"
  type        = string
  default     = "test-kp"
}

variable "aws_name" {
  description = "El nombre que se utilizara para crear la maquina"
  type        = string
  default     = "nodoPrueba"
}